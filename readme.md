# Cómo usar el proyecto
Clona el repositorio (si es aplicable):

```
git clone https://github.com/tu-usuario/rag-deepseek.git
cd rag-deepseek
```
Ejecuta la aplicación:

```
python3 streamlit run app.py
```

Interactúa con la aplicación:

- Sube un archivo PDF usando el botón de carga.

- Una vez procesado el PDF, escribe tu pregunta en el campo de chat.

- La aplicación generará una respuesta basada en el contenido del PDF.

# Requisitos
Para ejecutar este proyecto, necesitas instalar las siguientes dependencias:

```
pip install streamlit langchain pdfplumber faiss-cpu huggingface-hub ollama sentence-transformers
```

Además, asegúrate de tener configurado y en ejecución el servicio de Ollama con el modelo deepseek-r1:1.5b.
