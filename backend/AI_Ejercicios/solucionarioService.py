import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from typing import Dict, List, Any
from fastapi import HTTPException
from uuid import UUID 

class SolucionarioService:
    def __init__(self):
        endpoint = "https://models.github.ai/inference"
        model = "openai/gpt-4.1"
        token = os.environ["GITHUB_TOKEN"]
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )
        self.model = model

    async def resolver_ejercicio(self, pregunta: str, tema: str, nivel: str = "medio") -> Dict[str, Any]:
        """
        Resuelve un ejercicio paso a paso con explicación detallada estilo GPT
        """
        PROMPT_SOLUCION = f"""
        Actúa como un tutor de matemáticas experto. Resuelve el siguiente ejercicio paso a paso con el estilo característico de ChatGPT:

        **EJERCICIO:** {pregunta}
        **TEMA:** {tema}
        **NIVEL:** {nivel}

        Proporciona la solución en el siguiente formato JSON:
        {{
            "ejercicio": "{pregunta}",
            "solucion_paso_a_paso": [
                {{
                    "paso": 1,
                    "titulo": "Identificar datos y incógnita",
                    "contenido": "Explicación del primer paso...",
                    "formula_o_concepto": "Fórmula o concepto aplicado (si aplica)"
                }},
                {{
                    "paso": 2,
                    "titulo": "Aplicar fórmula/método",
                    "contenido": "Desarrollo matemático...",
                    "calculo": "2x + 3 = 7"
                }}
            ],
            "respuesta_final": "Valor numérico o respuesta completa",
            "verificacion": "Cómo verificar que la respuesta es correcta",
            "conceptos_clave": ["concepto1", "concepto2"],
            "dificultad_estimada": "facil/medio/dificil",
            "tiempo_estimado": "3-5 minutos",
            "consejos_adicionales": "Consejos para resolver ejercicios similares"
        }}

        IMPORTANTE:
        - Usa un lenguaje claro y pedagógico
        - Explica cada paso detalladamente
        - Incluye cálculos intermedios
        - Proporciona contexto del porqué de cada paso
        - Usa notación matemática apropiada
        """

        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un tutor experto en matemáticas que explica de manera clara y detallada."),
                    UserMessage(PROMPT_SOLUCION),
                ],
                temperature=0.3,  # Más determinista para matemáticas
                top_p=0.9,
                model=self.model
            )
            
            resultado = json.loads(response.choices[0].message.content)
            return {
                "status": "success",
                "solucion": resultado
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al resolver ejercicio: {str(e)}"
            )

    async def evaluar_respuesta(self, pregunta: str, respuesta_correcta: str, 
                              respuesta_alumno: str, tema: str) -> Dict[str, Any]:
        """
        Evalúa la respuesta del alumno y proporciona retroalimentación
        """
        PROMPT_EVALUACION = f"""
        Evalúa la respuesta del estudiante y proporciona retroalimentación constructiva.

        **PREGUNTA:** {pregunta}
        **RESPUESTA CORRECTA:** {respuesta_correcta}
        **RESPUESTA DEL ALUMNO:** {respuesta_alumno}
        **TEMA:** {tema}

        Responde en el siguiente formato JSON:
        {{
            "correcto": true/false,
            "puntuacion": 0-100,
            "explicacion": "Explicación detallada de por qué está correcto/incorrecto",
            "errores_identificados": ["error1", "error2"] o [],
            "sugerencias": "Sugerencias específicas para mejorar",
            "concepto_a_reforzar": "Concepto principal que necesita refuerzo",
            "ejercicios_similares_recomendados": true/false,
            "nivel_comprension": "excelente/bueno/regular/deficiente"
        }}

        CRITERIOS DE EVALUACIÓN:
        - Si la respuesta es matemáticamente correcta: 100 puntos
        - Si tiene el enfoque correcto pero errores menores: 70-90 puntos
        - Si muestra comprensión parcial: 40-60 puntos
        - Si está completamente incorrecta: 0-30 puntos

        Sé constructivo y alentador en tu feedback.
        """

        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un evaluador educativo que proporciona retroalimentación constructiva."),
                    UserMessage(PROMPT_EVALUACION),
                ],
                temperature=0.2,
                top_p=0.9,
                model=self.model
            )
            
            resultado = json.loads(response.choices[0].message.content)
            return resultado
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al evaluar respuesta: {str(e)}"
            )

    async def generar_observaciones_reporte(self, respuestas: List[Dict], 
                                          porcentaje: float, nivel_maximo: int) -> str:
        """
        Genera observaciones inteligentes para el reporte del alumno
        """
        PROMPT_OBSERVACIONES = f"""
        Genera observaciones pedagógicas para un reporte de rendimiento estudiantil.

        **DATOS DEL ALUMNO:**
        - Porcentaje de aciertos: {porcentaje}%
        - Nivel máximo alcanzado: {nivel_maximo}
        - Total de ejercicios: {len(respuestas)}

        **DETALLE DE RESPUESTAS:**
        {json.dumps(respuestas, indent=2)}

        Genera observaciones en formato de texto que incluyan:
        1. Fortalezas identificadas
        2. Áreas de mejora
        3. Recomendaciones específicas
        4. Próximos pasos sugeridos

        El tono debe ser:
        - Constructivo y motivador
        - Específico y basado en evidencia
        - Orientado a la mejora
        - Apropiado para estudiantes de secundaria

        Máximo 300 palabras.
        """

        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un pedagogo experto que analiza el rendimiento estudiantil."),
                    UserMessage(PROMPT_OBSERVACIONES),
                ],
                temperature=0.4,
                top_p=0.9,
                model=self.model
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error al generar observaciones: Se recomienda revisar el progreso con un tutor."
