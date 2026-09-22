import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load API keys
load_dotenv()

DB_DIR = "./faiss_db"

def get_embeddings():
    # Use Google's embedding model
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")

def get_vector_store():
    """Loads and returns the existing FAISS vector store."""
    if not os.path.exists(DB_DIR):
        raise ValueError(f"Vector store not found at {DB_DIR}. Please run ingest_data first.")
    
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
    return vector_store

def ingest_data(file_path: str):
    """Loads a document, chunks it, and creates a FAISS index."""
    print(f"Loading data from {file_path}...")
    loader = TextLoader(file_path, encoding='utf-8')
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    
    print(f"Split document into {len(chunks)} chunks. Generating embeddings...")
    embeddings = get_embeddings()
    
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(DB_DIR)
    
    print("Data successfully ingested and saved to FAISS!")

if __name__ == "__main__":
    sample_file = "./data/sample.txt"
    if os.path.exists(sample_file):
        ingest_data(sample_file)
    else:
        print(f"Sample file not found at {sample_file}")
