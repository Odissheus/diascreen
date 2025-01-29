from fastapi import APIRouter, Depends
from services.llm_service import LLMService
from pydantic import BaseModel

router = APIRouter()
llm_service = LLMService()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await llm_service.get_response(request.message)
    return ChatResponse(response=response)