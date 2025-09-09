import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"


CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "rag_documents"

# Server Configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000


EMBEDDING_MODEL = "text-embedding-004"
