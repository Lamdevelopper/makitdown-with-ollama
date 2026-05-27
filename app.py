from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import io
import re
import shutil
import tempfile
import threading
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from markitdown import MarkItDown


BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
STATIC_DIR = BASE_DIR / "static"
OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_CHUNK_CHARS = 12000
MAX_MARKITDOWN_WORKERS = 4

UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="MarkItDown Local", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

JOBS: dict[str, dict[str, Any]] = {}


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem or "converted"
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip(".-")
    return stem or "converted"


def result_text(result: Any) -> str:
    return getattr(result, "text_content", None) or getattr(result, "markdown", None) or str(result)


def strip_thinking(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()


def make_markitdown() -> MarkItDown:
    return MarkItDown(enable_plugins=False)


def unique_output_path(directory: Path, filename: str) -> Path:
    path = directory / filename
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 2
    while True:
        candidate = directory / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


async def ask_ollama(markdown: str, model: str) -> str:
    prompt = (
        "Limpia y mejora este Markdown sin inventar informacion. "
        "Conserva encabezados, listas, tablas, enlaces y datos importantes. "
        "Devuelve solamente Markdown.\n\n"
        f"{markdown}"
    )
    payload = {"model": model, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()
    return strip_thinking(data.get("response", "")) or markdown


def split_markdown(markdown: str, chunk_size: int = OLLAMA_CHUNK_CHARS) -> list[str]:
    if len(markdown) <= chunk_size:
        return [markdown]

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for paragraph in re.split(r"(\n\s*\n)", markdown):
        if current_len + len(paragraph) > chunk_size and current:
            chunks.append("".join(current).strip())
            current = []
            current_len = 0
        current.append(paragraph)
        current_len += len(paragraph)

    if current:
        chunks.append("".join(current).strip())

    return [chunk for chunk in chunks if chunk]


def ask_ollama_sync(markdown: str, model: str, chunk_index: int, total_chunks: int) -> str:
    prompt = (
        "Limpia y mejora este Markdown sin inventar informacion. "
        "Conserva encabezados, listas, tablas, enlaces y datos importantes. "
        f"Estas procesando el bloque {chunk_index} de {total_chunks}; no agregues resumen global. "
        "Devuelve solamente Markdown.\n\n"
        f"{markdown}"
    )
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 8192},
    }
    with httpx.Client(timeout=180) as client:
        response = client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        if response.status_code >= 400:
            detail = response.text.strip()
            if len(detail) > 500:
                detail = detail[:500] + "..."
            raise RuntimeError(
                f"Ollama devolvio HTTP {response.status_code} usando el modelo '{model}'. "
                f"Detalle: {detail or 'sin detalle'}. "
                "Prueba con un modelo mas pequeno o convierte sin Ollama."
            )
        data = response.json()
    return strip_thinking(data.get("response", "")) or markdown


def improve_with_ollama_sync(markdown: str, model: str, job: dict[str, Any]) -> str:
    chunks = split_markdown(markdown)
    improved: list[str] = []

    for index, chunk in enumerate(chunks, start=1):
        job["phase"] = f"Procesando con Ollama ({index}/{len(chunks)})"
        improved.append(ask_ollama_sync(chunk, model, index, len(chunks)))

    return "\n\n".join(improved)


def job_snapshot(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "jobId": job["jobId"],
        "batchId": job["batchId"],
        "status": job["status"],
        "phase": job["phase"],
        "currentFile": job["currentFile"],
        "currentIndex": job["currentIndex"],
        "totalFiles": job["totalFiles"],
        "activeFiles": list(job.get("activeFiles", [])),
        "convertedFiles": job.get("convertedFiles", 0),
        "completedFiles": job["completedFiles"],
        "failedFiles": job["failedFiles"],
        "progress": job["progress"],
        "markitdownWorkers": job.get("markitdownWorkers", 1),
        "useOllama": job["useOllama"],
        "ollamaModel": job["ollamaModel"],
        "results": job["results"],
        "error": job.get("error"),
        "downloadAllUrl": f"/api/download/{job['batchId']}.zip",
    }


def process_job(job_id: str) -> None:
    job = JOBS[job_id]
    files = job["files"]
    batch_output_dir = OUTPUTS_DIR / job["batchId"]
    total_steps = max(1, len(files) * (3 if job["useOllama"] else 2))
    completed_steps = 0
    converted: list[dict[str, Any]] = []
    lock: threading.Lock = job["lock"]
    workers = min(MAX_MARKITDOWN_WORKERS, max(1, len(files)))

    def set_progress() -> None:
        job["progress"] = min(99, round((completed_steps / total_steps) * 100))

    def convert_one(index: int, file_info: dict[str, str]) -> dict[str, Any]:
        input_path = Path(file_info["path"])
        original_name = file_info["filename"]
        with lock:
            job["activeFiles"].append(original_name)
            active_count = len(job["activeFiles"])
            job["currentFile"] = ", ".join(job["activeFiles"][:3])
            job["currentIndex"] = min(index, job["totalFiles"])
            job["phase"] = f"Convirtiendo con MarkItDown en paralelo ({active_count}/{workers} activos)"

        try:
            converter = make_markitdown()
            converted_result = converter.convert(str(input_path))
            markdown = result_text(converted_result)
            return {"ok": True, "index": index, "filename": original_name, "markdown": markdown}
        except Exception as exc:
            return {"ok": False, "index": index, "filename": original_name, "error": str(exc)}
        finally:
            with lock:
                if original_name in job["activeFiles"]:
                    job["activeFiles"].remove(original_name)
                job["currentFile"] = ", ".join(job["activeFiles"][:3])

    try:
        job["status"] = "running"
        job["phase"] = f"Convirtiendo con MarkItDown en paralelo (0/{workers} activos)"

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(convert_one, index, file_info) for index, file_info in enumerate(files, start=1)]
            for future in as_completed(futures):
                item = future.result()
                converted.append(item)
                completed_steps += 1
                job["convertedFiles"] += 1
                set_progress()

                if not item["ok"]:
                    missing_steps = 2 if job["useOllama"] else 1
                    completed_steps += missing_steps
                    job["failedFiles"] += 1
                    set_progress()
                    job["results"].append({"ok": False, "filename": item["filename"], "error": item["error"]})

        for item in sorted(converted, key=lambda result: result["index"]):
            if not item["ok"]:
                continue

            original_name = item["filename"]
            markdown = item["markdown"]
            raw_markdown = markdown
            job["currentIndex"] = item["index"]
            job["currentFile"] = original_name

            output_name = f"{safe_stem(original_name)}.md"
            output_path = unique_output_path(batch_output_dir, output_name)

            try:
                ai_applied = False
                ollama_error = ""
                if job["useOllama"]:
                    try:
                        markdown = improve_with_ollama_sync(markdown, job["ollamaModel"], job)
                        ai_applied = True
                    except Exception as exc:
                        markdown = raw_markdown
                        ollama_error = str(exc)
                        job["failedFiles"] += 1
                    finally:
                        completed_steps += 1
                        set_progress()

                job["phase"] = "Guardando Markdown crudo" if ollama_error else "Guardando Markdown"
                output_path.write_text(markdown, encoding="utf-8")
                completed_steps += 1
                set_progress()
                job["completedFiles"] += 1

                job["results"].append(
                    {
                        "ok": True,
                        "filename": original_name,
                        "outputName": output_path.name,
                        "downloadUrl": f"/api/download/{job['batchId']}/{output_path.name}",
                        "markdown": markdown,
                        "aiApplied": ai_applied,
                        "ollamaError": ollama_error,
                    }
                )
            except Exception as exc:
                job["failedFiles"] += 1
                job["results"].append({"ok": False, "filename": original_name, "error": str(exc)})

        job["status"] = "done"
        job["phase"] = "Listo"
        job["currentFile"] = ""
        job["progress"] = 100
    except Exception as exc:
        job["status"] = "error"
        job["phase"] = "Error"
        job["error"] = str(exc)
    finally:
        upload_dir = Path(job["uploadDir"])
        if upload_dir.exists():
            shutil.rmtree(upload_dir, ignore_errors=True)


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse((STATIC_DIR / "index.html").read_text(encoding="utf-8"))


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/ollama/models")
async def ollama_models() -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        return {
            "available": False,
            "models": [],
            "message": f"Ollama no responde en {OLLAMA_BASE_URL}: {exc}",
        }

    models = [item.get("name") for item in data.get("models", []) if item.get("name")]
    return {
        "available": bool(models),
        "models": models,
        "message": "Modelos encontrados." if models else "Ollama responde, pero no hay modelos instalados.",
    }


@app.post("/api/convert")
async def convert(
    files: list[UploadFile] = File(...),
    use_ollama: bool = Form(False),
    ollama_model: str = Form(""),
    ) -> JSONResponse:
    if use_ollama and not ollama_model:
        raise HTTPException(status_code=400, detail="Selecciona un modelo de Ollama.")

    batch_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid4().hex[:8]
    batch_output_dir = OUTPUTS_DIR / batch_id
    batch_output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(dir=UPLOADS_DIR) as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        for upload in files:
            original_name = upload.filename or "archivo"
            saved_path = temp_dir / original_name

            try:
                with saved_path.open("wb") as handle:
                    shutil.copyfileobj(upload.file, handle)

                converter = make_markitdown()
                converted = converter.convert(str(saved_path))
                markdown = result_text(converted)

                ai_applied = False
                if use_ollama:
                    markdown = await ask_ollama(markdown, ollama_model)
                    ai_applied = True

                output_name = f"{safe_stem(original_name)}.md"
                output_path = batch_output_dir / output_name
                output_path.write_text(markdown, encoding="utf-8")

                results.append(
                    {
                        "ok": True,
                        "filename": original_name,
                        "outputName": output_name,
                        "downloadUrl": f"/api/download/{batch_id}/{output_name}",
                        "markdown": markdown,
                        "aiApplied": ai_applied,
                    }
                )
            except Exception as exc:
                results.append({"ok": False, "filename": original_name, "error": str(exc)})
            finally:
                await upload.close()

    return JSONResponse(
        {
            "batchId": batch_id,
            "downloadAllUrl": f"/api/download/{batch_id}.zip",
            "results": results,
        }
    )


@app.post("/api/jobs")
async def create_job(
    files: list[UploadFile] = File(...),
    use_ollama: bool = Form(False),
    ollama_model: str = Form(""),
) -> JSONResponse:
    if use_ollama and not ollama_model:
        raise HTTPException(status_code=400, detail="Selecciona un modelo de Ollama.")

    batch_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid4().hex[:8]
    upload_dir = UPLOADS_DIR / batch_id
    batch_output_dir = OUTPUTS_DIR / batch_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    batch_output_dir.mkdir(parents=True, exist_ok=True)

    saved_files: list[dict[str, str]] = []
    for index, upload in enumerate(files, start=1):
        original_name = Path(upload.filename or f"archivo-{index}").name
        saved_name = f"{index:03d}-{safe_stem(original_name)}{Path(original_name).suffix}"
        saved_path = upload_dir / saved_name
        try:
            with saved_path.open("wb") as handle:
                shutil.copyfileobj(upload.file, handle)
            saved_files.append({"filename": original_name, "path": str(saved_path)})
        finally:
            await upload.close()

    job_id = uuid4().hex
    JOBS[job_id] = {
        "jobId": job_id,
        "batchId": batch_id,
        "status": "queued",
        "phase": "En cola",
        "currentFile": "",
        "currentIndex": 0,
        "totalFiles": len(saved_files),
        "activeFiles": [],
        "convertedFiles": 0,
        "completedFiles": 0,
        "failedFiles": 0,
        "progress": 0,
        "markitdownWorkers": min(MAX_MARKITDOWN_WORKERS, max(1, len(saved_files))),
        "useOllama": use_ollama,
        "ollamaModel": ollama_model,
        "results": [],
        "files": saved_files,
        "uploadDir": str(upload_dir),
        "lock": threading.Lock(),
    }
    threading.Thread(target=process_job, args=(job_id,), daemon=True).start()
    return JSONResponse(job_snapshot(JOBS[job_id]))


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str) -> JSONResponse:
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado.")
    return JSONResponse(job_snapshot(job))


@app.get("/api/download/{batch_id}.zip")
async def download_zip(batch_id: str) -> StreamingResponse:
    batch_dir = OUTPUTS_DIR / batch_id
    if not batch_dir.is_dir():
        raise HTTPException(status_code=404, detail="Lote no encontrado.")

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(batch_dir.glob("*.md")):
            archive.write(path, arcname=path.name)
    buffer.seek(0)

    headers = {"Content-Disposition": f'attachment; filename="{batch_id}.zip"'}
    return StreamingResponse(buffer, media_type="application/zip", headers=headers)


@app.get("/api/download/{batch_id}/{filename}")
async def download_file(batch_id: str, filename: str) -> FileResponse:
    path = OUTPUTS_DIR / batch_id / filename
    if not path.is_file() or path.suffix.lower() != ".md":
        raise HTTPException(status_code=404, detail="Archivo no encontrado.")
    return FileResponse(path, media_type="text/markdown", filename=filename)
