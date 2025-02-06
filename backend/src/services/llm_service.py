import openai
from config.config import settings
from services.document_service import document_service
import logging
from langdetect import detect, DetectorFactory

# Imposta la seed per un rilevamento della lingua consistente
DetectorFactory.seed = 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Imposta la API key OpenAI (assicurati che sia definita nella variabile d'ambiente .env)
openai.api_key = settings.OPENAI_API_KEY

def is_generic_message(message: str) -> bool:
    """
    Riconosce messaggi generici, saluti o ringraziamenti.
    Estende il controllo alle espressioni che indicano un saluto finale o formule di cortesia.
    """
    lower_msg = message.lower()
    keywords = [
        "ciao", "salve", "buongiorno", "buonasera", "grazie", "ottimo", 
        "ben fatto", "perfetto", "grazie mille", "va bene lo stesso", 
        "buona giornata", "arrivederci", "a presto"
    ]
    # Se il messaggio contiene almeno una di queste parole chiave, lo consideriamo generico.
    return any(word in lower_msg for word in keywords)

class LLMService:
    def __init__(self):
        # Utilizziamo il modello ChatGPT (ad esempio, gpt-3.5-turbo)
        self.model = "gpt-3.5-turbo"  # o "gpt-4" se preferisci

    async def get_response(self, user_message: str) -> str:
        logger.info(f"\n=== DEBUG: NUOVA RICHIESTA: {user_message} ===")
        
        # Rilevamento della lingua
        try:
            detected_language = detect(user_message)
        except Exception as e:
            logger.error(f"Errore nel rilevamento della lingua: {e}")
            detected_language = "it"
        logger.info(f"Lingua rilevata: {detected_language}")
        
        # Se il messaggio è generico, usiamo un prompt dedicato per interazioni di cortesia
        if is_generic_message(user_message):
            generic_prompt = (
                "Sei un assistente virtuale educato, amichevole e umano. "
                "Rispondi in modo cordiale e naturale a questo messaggio, senza utilizzare dati di contesto. "
                "Mantieni la risposta breve e genuina. "
                f"Utilizza esclusivamente la lingua {detected_language}."
            )
            messages = [
                {"role": "system", "content": generic_prompt},
                {"role": "user", "content": user_message}
            ]
        else:
            # Recupera il contesto informativo
            relevant_context = document_service.get_relevant_context(user_message)
            logger.info(f"Lunghezza contesto trovato: {len(relevant_context)} caratteri")
            if not relevant_context:
                fallback = ("Mi dispiace, questa informazione non è presente nei documenti a mia disposizione." 
                            if detected_language == "it" else 
                            "I'm sorry, this information is not available in my documents.")
                return fallback

            info_prompt = (
                "Sei un assistente virtuale educato, amichevole e umano. "
                "Rispondi esclusivamente utilizzando le informazioni fornite nel contesto sottostante. "
                "Non utilizzare conoscenze esterne, non inventare dati e non formulare domande aggiuntive. "
                "Fornisci una risposta unica, completa e discorsiva, concisa (massimo 100 parole), "
                "senza introdurla con saluti, titoli, prefissi o commenti meta. "
                "Se l'informazione richiesta non è presente, rispondi esattamente: "
                "\"Mi dispiace, questa informazione non è presente nei documenti a mia disposizione.\" "
                f"Utilizza esclusivamente la lingua {detected_language}."
            )
            messages = [
                {"role": "system", "content": info_prompt},
                {"role": "system", "content": f"Contesto:\n{relevant_context}"},
                {"role": "user", "content": f"Domanda:\n{user_message}"}
            ]
        
        logger.info("=== MESSAGGI INVIATI ===")
        for msg in messages:
            logger.info(f"{msg['role']}: {msg['content'][:200]}")  # mostra solo i primi 200 caratteri
        logger.info("=========================")
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=512,           # Sufficiente per una risposta completa
                temperature=0.1,          # Bassa per maggiore aderenza alle istruzioni
                top_p=0.7,
                frequency_penalty=0,
                presence_penalty=0
            )
            logger.info(f"Risposta completa: {response}")
            
            answer = response['choices'][0]['message']['content'].strip()
            # Pulizia finale: rimuovi eventuali prefissi indesiderati
            for prefix in ["Risposta:", "Resposta:", "[INST]", "</s>"]:
                answer = answer.replace(prefix, "").strip()
            return answer if answer else (
                "Mi dispiace, si è verificato un errore nella generazione della risposta."
            )
        except Exception as e:
            logger.error(f"Errore durante la generazione della risposta: {e}")
            return (
                "Mi dispiace, si è verificato un errore durante l'elaborazione della risposta." 
                if detected_language == "it" else 
                "I'm sorry, there was an error processing the response."
            )
