import os
from typing import List
import shutil
from fastapi import UploadFile, HTTPException
from config.config import settings

class DocumentService:
    def __init__(self):
        os.makedirs(settings.KNOWLEDGE_BASE_DIR, exist_ok=True)

    async def save_document(self, file: UploadFile) -> str:
        """Salva un documento nella knowledge base"""
        try:
            # Verifica estensione
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in settings.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
                )

            # Verifica dimensione
            file_size = 0
            file_location = os.path.join(settings.KNOWLEDGE_BASE_DIR, file.filename)
            with open(file_location, "wb+") as file_object:
                while chunk := await file.read(8192):
                    file_size += len(chunk)
                    if file_size > settings.MAX_DOCUMENT_SIZE:
                        raise HTTPException(
                            status_code=400,
                            detail="File too large"
                        )
                    file_object.write(chunk)

            return file.filename

        except Exception as e:
            if os.path.exists(file_location):
                os.remove(file_location)
            raise HTTPException(status_code=500, detail=str(e))

    def list_documents(self) -> List[str]:
        """Lista tutti i documenti nella knowledge base"""
        return [
            f for f in os.listdir(settings.KNOWLEDGE_BASE_DIR)
            if os.path.splitext(f)[1].lower() in settings.ALLOWED_EXTENSIONS
        ]

    def delete_document(self, filename: str) -> bool:
        """Elimina un documento dalla knowledge base"""
        file_path = os.path.join(settings.KNOWLEDGE_BASE_DIR, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))