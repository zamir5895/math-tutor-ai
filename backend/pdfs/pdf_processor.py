
# pdf_processor.py
import PyPDF2
import re
from typing import List, Dict, Any
import openai
import os
from models import Exercise, MultipleChoiceAnswer
import json
class PDFProcessor:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extrae texto del PDF"""
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    async def process_with_ai(self, text: str) -> List[Exercise]:
        """Procesa el texto usando IA para extraer ejercicios estructurados"""
        prompt = f"""
        Analiza el siguiente texto que contiene ejercicios académicos y extrae cada ejercicio con la siguiente estructura:
        
        Para cada ejercicio identifica:
        1. Tema del ejercicio
        2. Problema/pregunta
        3. Si es de opción múltiple (múltiple choice) o respuesta abierta
        4. Si es múltiple choice: las opciones disponibles (A, B, C, D, etc.)
        5. La respuesta correcta
        
        Devuelve la información en formato JSON con esta estructura:
        {{
            "exercises": [
                {{
                    "tema": "string",
                    "problema": "string", 
                    "is_multiple_choice": boolean,
                    "respuestas": [
                        {{"option": "A", "text": "texto opción A"}},
                        {{"option": "B", "text": "texto opción B"}}
                    ] // solo si es multiple choice,
                    "respuesta_correcta": "A" // o la respuesta completa si no es multiple choice
                }}
            ]
        }}
        
        Texto a analizar:
        {text}
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            
            exercises = []
            for ex_data in result["exercises"]:
                respuestas = None
                if ex_data["is_multiple_choice"] and "respuestas" in ex_data:
                    respuestas = [
                        MultipleChoiceAnswer(option=r["option"], text=r["text"]) 
                        for r in ex_data["respuestas"]
                    ]
                
                exercise = Exercise(
                    tema=ex_data["tema"],
                    problema=ex_data["problema"],
                    is_multiple_choice=ex_data["is_multiple_choice"],
                    respuestas=respuestas,
                    respuesta_correcta=ex_data["respuesta_correcta"]
                )
                exercises.append(exercise)
            
            return exercises
            
        except Exception as e:
            # Fallback: procesamiento básico con regex
            return self.basic_text_processing(text)
    
    def basic_text_processing(self, text: str) -> List[Exercise]:
        """Procesamiento básico cuando la IA no está disponible"""
        exercises = []
        
        # Patrones básicos para detectar ejercicios
        exercise_pattern = r'(\d+\.?\s*)(.*?)(?=\d+\.?\s*|$)'
        matches = re.findall(exercise_pattern, text, re.DOTALL)
        
        for i, (num, content) in enumerate(matches):
            if len(content.strip()) < 10:  # Filtrar contenido muy corto
                continue
                
            # Detectar si es multiple choice
            is_mc = bool(re.search(r'[A-D]\)', content) or re.search(r'[a-d]\)', content))
            
            exercise = Exercise(
                tema=f"Tema {i+1}",  # Tema genérico
                problema=content.strip(),
                is_multiple_choice=is_mc,
                respuestas=None,  # Se necesitaría procesamiento más avanzado
                respuesta_correcta="No procesada automáticamente"
            )
            exercises.append(exercise)
        
        return exercises