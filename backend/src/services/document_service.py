import os
from typing import List
from fastapi import UploadFile, HTTPException
from config.config import settings
import PyPDF2
from .embedding_service import EmbeddingService

class DocumentService:
    def __init__(self):
        os.makedirs(settings.KNOWLEDGE_BASE_DIR, exist_ok=True)
        self.embedding_service = EmbeddingService()
        self.documents = []
        self.document_names = []
        self.load_documents()

    async def save_document(self, file: UploadFile) -> str:
        try:
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in settings.ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail="File type not allowed")

            file_size = 0
            file_location = os.path.join(settings.KNOWLEDGE_BASE_DIR, file.filename)
            with open(file_location, "wb+") as file_object:
                while chunk := await file.read(8192):
                    file_size += len(chunk)
                    if file_size > settings.MAX_DOCUMENT_SIZE:
                        raise HTTPException(status_code=400, detail="File too large")
                    file_object.write(chunk)
            
            self.load_documents()
            return file.filename

        except Exception as e:
            if os.path.exists(file_location):
                os.remove(file_location)
            raise HTTPException(status_code=500, detail=str(e))

    def list_documents(self) -> List[str]:
        return [
            f for f in os.listdir(settings.KNOWLEDGE_BASE_DIR)
            if os.path.splitext(f)[1].lower() in settings.ALLOWED_EXTENSIONS
        ]

    def delete_document(self, filename: str) -> bool:
        file_path = os.path.join(settings.KNOWLEDGE_BASE_DIR, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        try:
            os.remove(file_path)
            self.load_documents()
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def load_documents(self):
        print("\n=== DEBUG: INIZIO CARICAMENTO DOCUMENTI ===")
        self.documents = []
        self.document_names = []
        knowledge_files = ["legge.pdf", "progetto.pdf"]
        
        for filename in knowledge_files:
            file_path = os.path.join(settings.KNOWLEDGE_BASE_DIR, filename)
            print(f"Cercando file in: {file_path}")
            if os.path.exists(file_path):
                print(f"File trovato: {filename}")
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for i, page in enumerate(pdf_reader.pages):
                        page_text = page.extract_text()
                        print(f"Pagina {i+1}: {len(page_text)} caratteri")
                        text += page_text + "\n"
                    print(f"Contenuto totale estratto: {len(text)} caratteri")
                    print("Prime 100 caratteri del contenuto:")
                    print(text[:100])
                    self.documents.append(text)
                    self.document_names.append(filename)
            else:
                print(f"ERRORE: File {filename} non trovato!")
        print("=== DEBUG: FINE CARICAMENTO DOCUMENTI ===\n")
        
        if self.documents:
            self.embedding_service.index_documents(self.documents)
        else:
            print("ATTENZIONE: Nessun documento caricato!")

    def get_relevant_context(self, query: str) -> str:
        relevant_chunks = self.embedding_service.find_relevant_chunks(query)
        if not relevant_chunks:
            print("ATTENZIONE: Nessun chunk rilevante trovato!")
            return ""
        context = "\n".join(relevant_chunks)
        print(f"Contesto recuperato (primi 200 caratteri): {context[:200]}...")
        return context

document_service = DocumentService()