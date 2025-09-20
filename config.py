import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Model settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    LLM_MODEL_PATH = os.getenv("LLM_MODEL_PATH", "./models/phi-3-mini-4k-instruct-q4.gguf")
    
    # Vector database
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "cyber_forensics_docs")
    
    # RAG settings
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 100
    TOP_K_RESULTS = 3
    MAX_CONTEXT_LENGTH = 4000
    
    # File paths
    DATA_DIR = os.getenv("DATA_DIR", "./data/documents")
    
    # Supported file types
    SUPPORTED_EXTENSIONS = {
        '.txt', '.pdf', '.md', '.html', 
        '.csv', '.json', '.xml', '.yaml', '.yml'
    }