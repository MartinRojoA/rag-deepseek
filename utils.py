from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import time

def procesar_pdf(archivo):
    """Procesa un archivo PDF cargado en Streamlit."""

    with open("temp.pdf", "wb") as f:  # Cuando se carga el archivo, se guarda como un archivo temporal
        f.write(archivo.getvalue())

    loader = PDFPlumberLoader("temp.pdf")
    docs = loader.load()
    text_splitter = SemanticChunker(HuggingFaceEmbeddings()) 

    return text_splitter.split_documents(docs)

def crear_base_vectorial(documents):
    """Crea una base de datos vectorial a partir de los documentos."""

    embedder = HuggingFaceEmbeddings() # modelo opensoruce
    vector_db = FAISS.from_documents(documents, embedder)
    retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    return retriever

def crear_qa_funcion(retriever):
    """Crea una función de QA basada en un retriever."""
    llm = Ollama(model="deepseek-r1:1.5b")  # Modelo de lenguaje open source

    # Template del prompt
    prompt_template  = """
    Eres un asistente inteligente que responde preguntas basadas únicamente en el contexto proporcionado.
    Sigue estas instrucciones:
    1. Lee cuidadosamente el contexto y la pregunta.
    2. Responde de manera clara, concisa y en español.
    3. Si la pregunta no puede responderse con el contexto, di: "No tengo suficiente información para responder esta pregunta".
    4. Si la pregunta es ambigua o no está relacionada con el contexto, pide más detalles o aclara que no puedes ayudar.

    Contexto: {context}
    Pregunta: {question}
    Respuesta:"""

    QA_PROMPT = PromptTemplate.from_template(prompt_template)  
    llm_chain = LLMChain(llm=llm, prompt=QA_PROMPT)
    combine_documents_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="context")
    retQA = RetrievalQA(combine_documents_chain=combine_documents_chain, retriever=retriever)

    return retQA

def chat_stream(prompt):
    response = prompt
    for char in response:
        yield char
        time.sleep(0.02)