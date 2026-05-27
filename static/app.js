const fileInput = document.querySelector("#fileInput");
const dropzone = document.querySelector("#dropzone");
const fileList = document.querySelector("#fileList");
const convertForm = document.querySelector("#convertForm");
const convertButton = document.querySelector("#convertButton");
const results = document.querySelector("#results");
const preview = document.querySelector("#preview");
const previewTitle = document.querySelector("#previewTitle");
const copyButton = document.querySelector("#copyButton");
const useOllama = document.querySelector("#useOllama");
const modelSelect = document.querySelector("#modelSelect");
const ollamaBadge = document.querySelector("#ollamaBadge");
const progressPanel = document.querySelector("#progressPanel");
const progressTitle = document.querySelector("#progressTitle");
const progressPercent = document.querySelector("#progressPercent");
const progressBar = document.querySelector("#progressBar");
const progressMeta = document.querySelector("#progressMeta");

let selectedFiles = [];
let currentMarkdown = "";
let pollTimer = null;

function renderFiles() {
  fileList.innerHTML = "";
  selectedFiles.forEach((file) => {
    const item = document.createElement("div");
    item.className = "fileItem";
    item.textContent = `${file.name} (${Math.ceil(file.size / 1024)} KB)`;
    fileList.appendChild(item);
  });
}

function setFiles(files) {
  selectedFiles = Array.from(files);
  renderFiles();
}

async function loadOllamaModels() {
  try {
    const response = await fetch("/api/ollama/models");
    const data = await response.json();
    modelSelect.innerHTML = "";

    if (!data.available) {
      ollamaBadge.className = "badge warn";
      ollamaBadge.textContent = data.message;
      modelSelect.disabled = true;
      useOllama.checked = false;
      useOllama.disabled = true;
      modelSelect.append(new Option("Sin modelos detectados", ""));
      return;
    }

    data.models.forEach((model) => modelSelect.append(new Option(model, model)));
    ollamaBadge.className = "badge ok";
    ollamaBadge.textContent = `${data.models.length} modelo(s) de Ollama detectado(s).`;
    useOllama.disabled = false;
    modelSelect.disabled = !useOllama.checked;
  } catch (error) {
    ollamaBadge.className = "badge warn";
    ollamaBadge.textContent = `No se pudo revisar Ollama: ${error}`;
  }
}

function showPreview(title, markdown) {
  currentMarkdown = markdown;
  previewTitle.textContent = title;
  preview.textContent = markdown || "Sin contenido.";
  copyButton.disabled = !markdown;
}

function updateProgress(job) {
  progressPanel.hidden = false;
  const percent = Math.max(0, Math.min(100, job.progress || 0));
  progressTitle.textContent = job.phase || "Procesando";
  progressPercent.textContent = `${percent}%`;
  progressBar.style.width = `${percent}%`;

  const mode = job.useOllama ? `Ollama: ${job.ollamaModel}` : "Sin Ollama";
  const activeFiles = job.activeFiles || [];
  const current = activeFiles.length
    ? `Activos (${activeFiles.length}/${job.markitdownWorkers}): ${activeFiles.join(", ")}`
    : job.currentFile
      ? `Archivo ${job.currentIndex}/${job.totalFiles}: ${job.currentFile}`
      : "Esperando archivo";
  progressMeta.textContent = `${current} | Convertidos: ${job.convertedFiles || 0}/${job.totalFiles} | Listos: ${job.completedFiles}/${job.totalFiles} | Errores: ${job.failedFiles} | ${mode}`;
}

function renderResults(data) {
  results.innerHTML = "";

  if (data.results.length) {
    const downloadAll = document.createElement("a");
    downloadAll.href = data.downloadAllUrl;
    downloadAll.textContent = "Descargar todo .zip";
    downloadAll.className = "resultItem";
    results.appendChild(downloadAll);
  }

  data.results.forEach((result) => {
    const item = document.createElement("div");
    item.className = `resultItem${result.ok ? "" : " error"}`;

    const title = document.createElement("strong");
    title.textContent = result.filename;
    item.appendChild(title);

    if (!result.ok) {
      const error = document.createElement("span");
      error.textContent = result.error;
      item.appendChild(error);
    } else {
      const note = document.createElement("span");
      if (result.ollamaError) {
        note.textContent = `Ollama fallo; se guardo el Markdown crudo. ${result.ollamaError}`;
      } else {
        note.textContent = result.aiApplied ? "Convertido y procesado con Ollama." : "Convertido con MarkItDown.";
      }
      item.appendChild(note);

      const actions = document.createElement("div");
      actions.className = "actions";

      const view = document.createElement("button");
      view.type = "button";
      view.textContent = "Ver";
      view.addEventListener("click", () => showPreview(result.outputName, result.markdown));

      const download = document.createElement("a");
      download.href = result.downloadUrl;
      download.textContent = "Descargar .md";

      actions.append(view, download);
      item.appendChild(actions);
    }

    results.appendChild(item);
  });

  const firstOk = data.results.find((result) => result.ok);
  if (firstOk && !currentMarkdown) {
    showPreview(firstOk.outputName, firstOk.markdown);
  }
}

async function pollJob(jobId) {
  const response = await fetch(`/api/jobs/${jobId}`);
  const job = await response.json();
  if (!response.ok) {
    throw new Error(job.detail || "No se pudo leer el progreso.");
  }

  updateProgress(job);
  renderResults(job);

  if (job.status === "done" || job.status === "error") {
    clearInterval(pollTimer);
    pollTimer = null;
    convertButton.disabled = false;
    convertButton.textContent = "Convertir";

    const firstOk = job.results.find((result) => result.ok);
    if (firstOk) {
      showPreview(firstOk.outputName, firstOk.markdown);
    } else if (job.error) {
      showPreview("Error", job.error);
    }
  }
}

dropzone.addEventListener("dragover", (event) => {
  event.preventDefault();
  dropzone.classList.add("dragging");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragging");
});

dropzone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropzone.classList.remove("dragging");
  setFiles(event.dataTransfer.files);
});

fileInput.addEventListener("change", () => setFiles(fileInput.files));

useOllama.addEventListener("change", () => {
  modelSelect.disabled = !useOllama.checked;
});

copyButton.addEventListener("click", async () => {
  await navigator.clipboard.writeText(currentMarkdown);
  copyButton.textContent = "Copiado";
  setTimeout(() => {
    copyButton.textContent = "Copiar";
  }, 1200);
});

convertForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!selectedFiles.length) {
    alert("Selecciona al menos un archivo.");
    return;
  }

  const form = new FormData();
  selectedFiles.forEach((file) => form.append("files", file));
  form.append("use_ollama", useOllama.checked ? "true" : "false");
  form.append("ollama_model", modelSelect.value || "");

  convertButton.disabled = true;
  convertButton.textContent = "Procesando...";
  results.innerHTML = "";
  currentMarkdown = "";
  showPreview("Preview Markdown", "Creando trabajo de conversion...");
  updateProgress({
    progress: 0,
    phase: "Subiendo archivos",
    currentFile: "",
    currentIndex: 0,
    totalFiles: selectedFiles.length,
    activeFiles: [],
    convertedFiles: 0,
    completedFiles: 0,
    failedFiles: 0,
    markitdownWorkers: Math.min(4, selectedFiles.length),
    useOllama: useOllama.checked,
    ollamaModel: modelSelect.value || "",
  });

  try {
    if (pollTimer) {
      clearInterval(pollTimer);
    }

    const response = await fetch("/api/jobs", { method: "POST", body: form });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "No se pudo crear el trabajo.");
    }

    updateProgress(data);
    pollTimer = setInterval(() => {
      pollJob(data.jobId).catch((error) => {
        clearInterval(pollTimer);
        pollTimer = null;
        convertButton.disabled = false;
        convertButton.textContent = "Convertir";
        showPreview("Error", String(error));
      });
    }, 1000);
  } catch (error) {
    convertButton.disabled = false;
    convertButton.textContent = "Convertir";
    showPreview("Error", String(error));
  }
});

loadOllamaModels();
