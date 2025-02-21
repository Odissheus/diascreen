from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import settings
from routes import chat, documents
import uvicorn

app = FastAPI(title="Diascreen API")

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:5173"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])

@app.get("/")
async def health_check():
   return {"status": "healthy", "service": "Diascreen API"}

if __name__ == "__main__":
   uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)