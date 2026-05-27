# MarkItDown Local con Ollama

App web local para convertir archivos a Markdown con MarkItDown y usar Ollama de forma opcional.

<img width="2559" height="1406" alt="imagen" src="https://github.com/user-attachments/assets/09aeab04-9c24-4aea-b5cd-0602ca2a9887" />


## Uso

```powershell
.\setup.ps1
.\run.ps1
```

Abre `http://127.0.0.1:8000`, arrastra archivos y descarga los `.md`.

Durante la conversion veras una barra de progreso con:

- archivo actual
- numero de archivo dentro del lote
- conversiones activas en paralelo
- fase actual: MarkItDown, Ollama o guardado
- archivos listos y errores
- modo activo: sin Ollama o modelo de Ollama seleccionado

La app convierte hasta 4 archivos en paralelo con MarkItDown. Si activas Ollama, primero termina las conversiones paralelas y despues procesa cada Markdown con Ollama en serie.

Si Ollama falla o se queda sin tiempo, la app conserva el Markdown crudo generado por MarkItDown y lo deja descargable con una advertencia.

## Ollama

La app revisa `http://127.0.0.1:11434/api/tags`. Si Ollama esta apagado o no hay modelos, la conversion normal sigue funcionando.

Para activar IA local, instala y abre Ollama, descarga un modelo, y marca "Usar Ollama" en la interfaz.

```powershell
ollama pull llama3.2
```

Para contenido visual, usa un modelo con vision disponible en tu instalacion de Ollama.
