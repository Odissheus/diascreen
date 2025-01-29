import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

class Settings:
    # Configurazione API Mistral
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
    
    # Configurazione del server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Configurazione paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))  # Risale di due livelli
    KNOWLEDGE_BASE_DIR = os.path.join(PROJECT_ROOT, "data", "knowledge_base")

    # Configurazione dell'applicazione
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB in bytes
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt'}

settings = Settings()