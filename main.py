import re
import streamlit as st
from utils import procesar_pdf, crear_base_vectorial,crear_qa_funcion, chat_stream

st.set_page_config(
    page_title="Goat",
    page_icon="🐐",
)

st.title("Chat con PDF 🐐")

archivo = st.file_uploader("Cargar PDF", type="pdf")

if archivo:

    documentos = procesar_pdf(archivo)
    retriever = crear_base_vectorial(documentos)
    qa_funcion = crear_qa_funcion(retriever)

    if prompt := st.chat_input("Escribir pregunta"):
        with st.chat_message("usuario"):
            st.write(prompt)
        with st.chat_message("asistente"):
            response = st.write_stream(chat_stream(re.search(r"</think>\s*(.*)", qa_funcion(prompt)["result"], re.DOTALL).group(0) ))
        

