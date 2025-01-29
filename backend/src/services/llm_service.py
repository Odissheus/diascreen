from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from config.config import settings
import os

class LLMService:
    def __init__(self):
        self.client = MistralClient(api_key=settings.MISTRAL_API_KEY)
        self.model = "mistral-large-latest"
        self.context = self._load_context()

    def _load_context(self):
        """Carica il contesto dai documenti nella knowledge base"""
        context = []
        for filename in os.listdir(settings.KNOWLEDGE_BASE_DIR):
            if os.path.splitext(filename)[1].lower() in settings.ALLOWED_EXTENSIONS:
                file_path = os.path.join(settings.KNOWLEDGE_BASE_DIR, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    context.append(f.read())
        return "\n\n".join(context)

    async def get_response(self, user_message: str) -> str:
        """Ottiene una risposta dal modello"""
        messages = [
            ChatMessage(role="system", content=f"Sei un assistente esperto di diabete. Rispondi alle domande basandoti su queste informazioni: {self.context}"),
            ChatMessage(role="user", content=user_message)
        ]
        
        response = self.client.chat(
            model=self.model,
            messages=messages
        )
        
        return response.choices[0].message.content