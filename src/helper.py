import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")  
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")  

os.environ['GOOGLE_API_KEY'] =  GOOGLE_API_KEY
os.environ['LANGCHAIN_API_KEY'] =  LANGCHAIN_API_KEY
os.environ['LANGCHAIN_PROJECT'] =  LANGCHAIN_PROJECT


def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks



def get_vector_store(text_chunks):
    embeddings = OllamaEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store



def get_conversational_chain(vector_store):
    llm=Ollama()
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
    return conversation_chain