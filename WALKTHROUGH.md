# Como correr MarkItDown Local con Ollama

Esta app convierte archivos a Markdown usando MarkItDown en tu PC. Ollama es opcional y se usa solo de forma local.

## 1. Abrir PowerShell

Abre una ventana de PowerShell.

## 2. Entrar a la carpeta del proyecto

```powershell
cd C:\Users\lamoy\Desktop\proyectos_coding\markitdown-local-ollama
```

## 3. Hacer setup inicial

Solo necesitas correr esto la primera vez:

```powershell
.\setup.ps1
```

Esto crea el entorno virtual `.venv` e instala las dependencias:

- MarkItDown
- FastAPI
- Uvicorn
- httpx
- python-multipart

Tambien revisa si Ollama responde en `http://127.0.0.1:11434`.

## 4. Iniciar la app

```powershell
.\run.ps1
```

La app quedara disponible en:

```text
http://127.0.0.1:8000
```

Si no se abre sola, copia esa URL en tu navegador.

## 5. Convertir archivos

En la pagina:

1. Arrastra archivos al recuadro o haz clic para seleccionarlos.
2. Deja `Usar Ollama` apagado para una conversion normal.
3. Activa `Usar Ollama` si quieres procesar el Markdown con un modelo local.
4. Haz clic en `Convertir`.
5. Mira la barra de progreso para ver archivos activos, fase, avance del lote y si esta usando Ollama.
6. Usa `Ver`, `Copiar`, `Descargar .md` o `Descargar todo .zip`.

La barra muestra fases como:

- `Convirtiendo con MarkItDown en paralelo`
- `Procesando con Ollama`
- `Guardando Markdown`
- `Listo`

La app convierte hasta 4 archivos a la vez con MarkItDown. Si activas Ollama, primero convierte los archivos en paralelo y luego manda los Markdown a Ollama uno por uno.

Si Ollama falla, la app guarda y muestra el Markdown crudo generado por MarkItDown para que no pierdas la conversion.

## 6. Usar Ollama

Ollama es opcional. Si esta apagado o no tiene modelos, la app sigue convirtiendo archivos sin IA.

Para usar Ollama:

```powershell
ollama pull llama3.2
```

Luego abre Ollama y recarga la app. Si hay modelos disponibles, apareceran en el selector.

## 7. Cerrar la app

En la ventana de PowerShell donde corre el servidor, presiona:

```text
Ctrl + C
```

## 8. Si PowerShell bloquea scripts

Ejecuta esto en la misma ventana:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego vuelve a iniciar:

```powershell
.\run.ps1
```
