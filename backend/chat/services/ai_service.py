import google.generativeai as genai
from config import settings
from services.cache_service import cache

genai.configure(api_key=settings.gemini_api_key)

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.gemini_model)

    @cache.cached(ttl=3600)
    def get_embedding(self, text: str, task_type: str = "RETRIEVAL_QUERY"):
        return genai.embed_content(
            model=settings.embedding_model,
            content=text,
            task_type=task_type
        )["embedding"]

    def generate_stream(self, prompt: str):
        """Genera respuesta en streaming"""
        return self.model.generate_content(
            prompt,
            stream=True 
        )


ai = AIService()