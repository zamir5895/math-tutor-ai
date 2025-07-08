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

    def is_math_related(self, message: str) -> bool:
        """Usa IA para determinar si el mensaje está relacionado con matemáticas"""
        try:
            classification_prompt = f"""
            Determina si el siguiente mensaje está relacionado con matemáticas, incluyendo:
            - Álgebra, geometría, cálculo, estadística, trigonometría
            - Problemas numéricos, ecuaciones, funciones
            - Conceptos matemáticos en general
            - Ejercicios o tareas de matemáticas
            - Dudas sobre procedimientos matemáticos
            
            Mensaje: "{message}"
            
            Responde únicamente con "SÍ" si es sobre matemáticas o "NO" si no lo es.
            """
            
            response = self.model.generate_content(classification_prompt)
            result = response.text.strip().upper()
            return "SÍ" in result or "SI" in result or "YES" in result
        except Exception:
            # Si hay error, usar palabras clave como fallback
            math_keywords = [
                'algebra', 'geometría', 'cálculo', 'trigonometría', 'estadística',
                'ecuación', 'función', 'derivada', 'integral', 'límite', 'suma',
                'resta', 'multiplicación', 'división', 'fracción', 'decimal',
                'porcentaje', 'probabilidad', 'matriz', 'vector', 'gráfica',
                'número', 'matemática', 'matemáticas', 'resolver', 'calcular',
                'problema', 'ejercicio', 'fórmula', 'teorema', 'demostración',
                '+', '-', '*', '/', '=', '²', '³', '√', '∫', '∑', 'π'
            ]
            message_lower = message.lower()
            return any(keyword in message_lower for keyword in math_keywords)

    def generate_title(self, first_message: str) -> str:
        """Genera un título para la conversación basado en el primer mensaje"""
        try:
            prompt = f"""
            Genera un título corto y descriptivo (máximo 50 caracteres) para una conversación de matemáticas que inicia con:
            "{first_message}"
            
            El título debe ser claro y específico al tema matemático.
            Responde solo con el título, sin comillas ni explicaciones.
            """
            
            response = self.model.generate_content(prompt)
            title = response.text.strip()
            return title[:50] if len(title) > 50 else title
        except Exception:
            return "Conversación de Matemáticas"

    def generate_response(self, prompt: str):
        response = self.model.generate_content(prompt)
        return response.text


ai = AIService()