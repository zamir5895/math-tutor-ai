import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from fastapi import HTTPException
from Repositorio.TemaRepositorio import TemaRepository
import re

class GPTService:

    def __init__(self):
        endpoint = "https://models.github.ai/inference"
        model = "openai/gpt-4.1"
        token = os.environ["GITHUB_TOKEN"]
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )
        self.tema_repository = TemaRepository()
        self.model = model

    async def gpt_connection(self, prompt:str, ):
        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un experto en educación matemática que genera ejercicios pedagógicos."),
                    UserMessage(prompt),
                ],
                temperature=1.0,
                top_p=1.0,
                model=self.model
            )
            resultado = json.loads(response.choices[0].message.content)
            print("Respuesta del LLM:", resultado)
            return resultado
        
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar respuesta del LLM: {str(e)}"
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar ejercicios con el LLM: {str(e)}"
            )
    async def generateVideoSImilarity(self, descripciones: list, tema: str):
        try:
            prompt = (
                "Dado una lista de descripciones de videos y un tema, genera un JSON con la similitud entre cada descripción y el tema. "
                "El formato de la respuesta debe ser un JSON con la similitud (del 1 al 10, donde 1 es muy poco similar y 10 es muy similar). "
                "El JSON debe estar en el mismo orden que las descripciones. "
                f"El tema es: {tema} y las descripciones son:\n{json.dumps(descripciones, indent=2)}\n"
                "Responde solo con el JSON, sin explicaciones ni texto adicional."
            )
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un experto en educación matemática que genera videos pedagógicos."),
                    UserMessage(prompt),
                ],
                temperature=1.0,
                top_p=1.0,
                model=self.model
            )
            raw_content = response.choices[0].message.content
    
            if not raw_content or not raw_content.strip():
                raise HTTPException(
                    status_code=500,
                    detail="El LLM devolvió una respuesta vacía."
                )
    
            try:
                resultado = json.loads(raw_content)
            except json.JSONDecodeError:
                match = re.search(r'(\{.*\}|\[.*\])', raw_content, re.DOTALL)
                if match:
                    resultado = json.loads(match.group(1))
                else:
                    raise
    
            return resultado
    
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar respuesta del LLM: {str(e)}. Respuesta cruda: {raw_content}"
            )
    
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar video con el LLM: {str(e)}"
            )
    async def generateExcersiceBaseOnSubtema(self, subtema:str):
        try:    
            PROMPT_TEMPLATE = """
            Genera 20 ejercicios de matemáticas para 2° de secundaria (Perú) sobre el tema: {tema}.
            
            Requisitos:
            1. Formato JSON:
            - 6 ejercicios fáciles (operaciones básicas)
            - 7 ejercicios medios (aplicación de conceptos)
            - 7 ejercicios difíciles (problemas contextualizados)
            
            2. Estructura cada ejercicio con:
            - pregunta: string claro
            - respuesta_correcta: string o número
            - es_multiple_choice: boolean
            - opciones: array de strings (si es multiple choice)
            - solucion: array de strings (pasos para resolver)
            - pistas: array de strings (sugerencias)
            - concepto_principal: string (concepto clave)
            - nivel: string (facil, medio, dificil)
            3. Contexto peruano (ej. usar soles, referencias locales)
            
            Ejemplo de formato esperado:
            [
              {{
                "pregunta": "¿Cuánto es 2 + 3?",
                "respuesta_correcta": "5",
                "es_multiple_choice": true,
                "opciones": ["3", "4", "5", "6"],
                "solucion": ["Paso 1: Identificar variables y operaciones", "Paso 2: Realizar la suma", "Paso 3: Verificar respuesta"],
                "pistas": ["Recuerda que sumar es juntar cantidades", "Piensa en objetos cotidianos para visualizar la suma"],
                "concepto_principal": "Suma de números enteros",
                "nivel": "facil"
              }}
            ]
            Responde solo con el JSON, sin explicaciones ni texto adicional.
            TEMA: {tema}
            """
            
            prompt = PROMPT_TEMPLATE.format(tema=subtema)
            try:
                response = self.client.complete(
                messages=[
                    SystemMessage("Eres un experto en educación matemática que genera ejercicios pedagógicos."),
                    UserMessage(prompt),
                ],
                temperature=1.0,
                top_p=1.0,
                model=self.model
            )
                
                resultado = json.loads(response.choices[0].message.content)
                return resultado
            
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al procesar la respuesta del LLM: {str(e)}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al formatear el prompt: {str(e)}"
            )