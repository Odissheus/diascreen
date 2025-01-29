from fastapi import APIRouter, UploadFile, File
from services.document_service import DocumentService
from typing import List

router = APIRouter()
document_service = DocumentService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = await document_service.save_document(file)
    return {"filename": filename}

@router.get("/list", response_model=List[str])
async def list_documents():
    return document_service.list_documents()

@router.delete("/{filename}")
async def delete_document(filename: str):
    document_service.delete_document(filename)
    return {"status": "success"}