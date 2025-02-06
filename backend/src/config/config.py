import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

class Settings:
    # Configurazione per l'API OpenAI (ChatGPT)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")
  
    # Configurazione del server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
  
    # Configurazione dei percorsi
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "knowledge_base")

    # Configurazione dell'applicazione
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB in bytes
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt'}

settings = Settings()
