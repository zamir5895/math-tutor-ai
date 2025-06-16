import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from tema import TemaCreate, NivelEnum
from db import temas_collection, progresos_collection
import hashlib
from typing import Dict, List, Optional
from uuid import UUID, uuid4  
from fastapi import HTTPException

class GPTService:
    def __init__(self):
        endpoint = "https://models.github.ai/inference"
        model = "openai/gpt-4.1"
        token = os.environ["GITHUB_TOKEN"]
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )
        self.model = model

    def _generar_hash_pregunta(self, pregunta: Dict) -> str:
        """Genera hash único para una pregunta"""
        contenido = f"{pregunta['pregunta']}_{pregunta['respuesta_correcta']}"
        return hashlib.md5(contenido.encode()).hexdigest()

    async def _verificar_tema_existente(self, tema: str) -> bool:
        """Verifica si un tema ya existe en la base de datos"""
        tema_existente = await temas_collection.find_one(
            {"nombre": {"$regex": f"^{tema}$", "$options": "i"}}
        )
        return tema_existente is not None

    async def _filtrar_ejercicios_duplicados(self, tema_nombre: str, nuevos_ejercicios: Dict) -> Dict:
        """
        Filtra ejercicios que ya existen en la base de datos para el tema dado
        
        Args:
            tema_nombre: Nombre del tema a verificar
            nuevos_ejercicios: Ejercicios generados por el LLM (formato {'facil': [...], ...})
            
        Returns:
            Dict: Ejercicios filtrados sin duplicados
        """
        tema_existente = await temas_collection.find_one(
            {"nombre": {"$regex": f"^{tema_nombre}$", "$options": "i"}},
            {"niveles.preguntas": 1}
        )
        
        if not tema_existente:
            return nuevos_ejercicios

        hashes_existentes = set()
        for nivel in tema_existente.get("niveles", []):
            for pregunta in nivel.get("preguntas", []):
                hash_pregunta = self._generar_hash_pregunta(pregunta)
                hashes_existentes.add(hash_pregunta)

        ejercicios_filtrados = {"facil": [], "medio": [], "dificil": []}
        
        for nivel, preguntas in nuevos_ejercicios.items():
            for pregunta in preguntas:
                hash_nuevo = self._generar_hash_pregunta(pregunta)
                if hash_nuevo not in hashes_existentes:
                    ejercicios_filtrados[nivel].append(pregunta)                    
                    hashes_existentes.add(hash_nuevo)  

        return ejercicios_filtrados

    async def generar_ejercicios(self, tema: str, forzar_generacion: bool = False) -> dict:
        """
        Genera ejercicios para un tema, verificando primero si no existe
        
        Args:
            tema: Nombre del tema a generar
            forzar_generacion: Si True, genera ejercicios aunque el tema exista
        
        Returns:
            dict: Resultado de la generación
            
        Raises:
            HTTPException: Si el tema ya existe y no se fuerza la generación
        """
        if not forzar_generacion and await self._verificar_tema_existente(tema):
            raise HTTPException(
                status_code=400,
                detail=f"El tema '{tema}' ya existe en la base de datos. Use forzar_generacion=True para regenerar."
            )

        PROMPT_TEMPLATE = """
            Genera 10 ejercicios de matemáticas para 2° de secundaria (Perú) sobre el tema: {tema}.

            Requisitos:
            1. Formato JSON con 3 niveles de dificultad:
            - 3 ejercicios fáciles (operaciones básicas)
            - 4 ejercicios medios (aplicación de conceptos)
            - 3 ejercicios difíciles (problemas contextualizados)

            2. Estructura cada ejercicio con:
            - pregunta: string claro
            - respuesta_correcta: string o número
            - es_multiple_choice: boolean
            - opciones: array de strings (si es multiple choice)

            3. Contexto peruano (ej. usar soles, referencias locales)

            Ejemplo de formato esperado:
            {{
            "facil": [
                {{
                "pregunta": "¿Cuánto es 2 + 3?",
                "respuesta_correcta": "5",
                "es_multiple_choice": true,
                "opciones": ["3", "4", "5", "6"]
                }}
            ],
            "medio": [...],
            "dificil": [...]
            }}

            TEMA: {tema}
            """
        
        prompt = PROMPT_TEMPLATE.format(tema=tema)
        
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
            
            resultado_filtrado = await self._filtrar_ejercicios_duplicados(tema, resultado)
            
            total_ejercicios = sum(len(p) for p in resultado_filtrado.values())
            if total_ejercicios == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Todos los ejercicios generados ya existen en la base de datos"
                )

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

        niveles = []
        for nivel_str in ["facil", "medio", "dificil"]:
            preguntas = resultado_filtrado.get(nivel_str, [])
            niveles.append({
                "nivel": NivelEnum(nivel_str),
                "preguntas": preguntas
            })

        tema_dict = {
            "nombre": tema,
            "descripcion": f"Ejercicios de {tema} generados por GPT",
            "niveles": niveles
        }

        tema_obj = TemaCreate(**tema_dict)
        
        tema_existente = await temas_collection.find_one({"nombre": tema})
        
        if tema_existente:
            await temas_collection.update_one(
                {"_id": tema_existente["_id"]}, 
                {"$set": tema_obj.dict(by_alias=True)}
            )
            operation = "actualizado"
        else:
            tema_data = tema_obj.dict(by_alias=True)
            tema_data["_id"] = uuid4()  
            await temas_collection.insert_one(tema_data)
            operation = "creado"

        return {
            "status": f"Tema {operation} exitosamente",
            "tema": tema,
            "ejercicios_nuevos": resultado_filtrado,
            "ejercicios_generados": sum(len(nivel["preguntas"]) for nivel in niveles),
            "detalle": {
                "facil": len(resultado_filtrado.get("facil", [])),
                "medio": len(resultado_filtrado.get("medio", [])),
                "dificil": len(resultado_filtrado.get("dificil", []))
            }
        }

    async def generar_ejercicios_adicionales(self, tema: str, nivel: str, cantidad: int = 5, 
                                           alumno_id: Optional[str] = None) -> List[Dict]:
        """
        Genera ejercicios adicionales basados en el nivel del alumno
        
        Args:
            tema: Tema de los ejercicios
            nivel: Nivel de dificultad (facil, medio, dificil)
            cantidad: Cantidad de ejercicios a generar
            alumno_id: ID del alumno para personalizar (opcional)
        
        Returns:
            List[Dict]: Lista de ejercicios adicionales
        """
        
        contexto_alumno = ""
        if alumno_id:
            try:
                alumno_uuid = UUID(alumno_id)
                
                progreso = await progresos_collection.find_one({
                    "alumno_id": alumno_uuid 
                })
                
                if progreso and progreso.get("respuestas"):
                    respuestas_incorrectas = [
                        r for r in progreso["respuestas"] 
                        if not r.get("correcto", True)
                    ]
                    if respuestas_incorrectas:
                        contexto_alumno = f"""
                        CONTEXTO DEL ALUMNO:
                        El alumno ha tenido dificultades con estos tipos de ejercicios:
                        {json.dumps([r["pregunta"] for r in respuestas_incorrectas[-3:]], indent=2)}
                        
                        Genera ejercicios que refuercen estos conceptos.
                        """
            except ValueError:
                print(f"Warning: alumno_id '{alumno_id}' no es un UUID válido")
            except Exception as e:
                print(f"Error al obtener contexto del alumno: {e}")
                pass  

        PROMPT_ADICIONALES = f"""
        Genera {cantidad} ejercicios adicionales de matemáticas para 2° de secundaria (Perú).
        
        **ESPECIFICACIONES:**
        - Tema: {tema}
        - Nivel: {nivel}
        - Cantidad: {cantidad}
        
        {contexto_alumno}
        
        **REQUISITOS:**
        1. Los ejercicios deben ser del nivel "{nivel}" únicamente
        2. Variedad en los tipos de problemas dentro del mismo nivel
        3. Contexto peruano (usar soles, referencias locales)
        4. Progresión gradual en complejidad dentro del nivel
        
        **FORMATO JSON:**
        [
            {{
                "pregunta": "Enunciado claro del ejercicio",
                "respuesta_correcta": "Respuesta exacta",
                "es_multiple_choice": boolean,
                "opciones": ["opcion1", "opcion2", "opcion3", "opcion4"] (si es multiple choice),
                "pista": "Pista útil para resolver el ejercicio",
                "concepto_principal": "Concepto matemático principal que evalúa"
            }}
        ]
        
        IMPORTANTE: Responde únicamente con el JSON válido, sin texto adicional.
        """

        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un generador experto de ejercicios matemáticos personalizados."),
                    UserMessage(PROMPT_ADICIONALES),
                ],
                temperature=0.8, 
                top_p=0.9,
                model=self.model
            )
            
            ejercicios = json.loads(response.choices[0].message.content)
            
            if not isinstance(ejercicios, list) or len(ejercicios) == 0:
                raise ValueError("No se generaron ejercicios válidos")
            
            return ejercicios
            
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar ejercicios adicionales: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar ejercicios adicionales: {str(e)}"
            )

    async def generar_ejercicios_personalizados(self, alumno_id: str, tema: str, 
                                              dificultades_identificadas: List[str]) -> Dict:
        """
        Genera ejercicios personalizados basados en las dificultades del alumno
        
        Args:
            alumno_id: ID del alumno
            tema: Tema de los ejercicios
            dificultades_identificadas: Lista de conceptos donde el alumno tiene dificultades
        
        Returns:
            Dict: Ejercicios personalizados organizados por tipo de dificultad
        """
        
        PROMPT_PERSONALIZADOS = f"""
        Genera ejercicios de refuerzo personalizados para un alumno de 2° de secundaria.
        
        **INFORMACIÓN DEL ALUMNO:**
        - Tema a reforzar: {tema}
        - Dificultades identificadas: {', '.join(dificultades_identificadas)}
        
        **OBJETIVO:**
        Crear ejercicios específicos que ayuden al alumno a superar estas dificultades.
        
        **FORMATO JSON:**
        {{
            "ejercicios_refuerzo": [
                {{
                    "pregunta": "Ejercicio enfocado en la dificultad específica",
                    "respuesta_correcta": "Respuesta",
                    "es_multiple_choice": boolean,
                    "opciones": [...] (si aplica),
                    "dificultad_objetivo": "¿Qué dificultad específica aborda?",
                    "estrategia_resolucion": "Estrategia recomendada para resolver",
                    "error_comun": "Error común que los estudiantes cometen aquí"
                }}
            ],
            "ejercicios_aplicacion": [
                {{
                    "pregunta": "Ejercicio de aplicación práctica",
                    "respuesta_correcta": "Respuesta",
                    "contexto_real": "Contexto de la vida real",
                    "conceptos_integrados": ["concepto1", "concepto2"]
                }}
            ]
        }}
        
        Genera 3 ejercicios de refuerzo y 2 de aplicación.
        """

        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un tutor personalizado que crea ejercicios específicos para las necesidades de cada alumno."),
                    UserMessage(PROMPT_PERSONALIZADOS),
                ],
                temperature=0.6,
                top_p=0.9,
                model=self.model
            )
            
            ejercicios = json.loads(response.choices[0].message.content)
            return ejercicios
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar ejercicios personalizados: {str(e)}"
            )

    async def analizar_patron_errores(self, respuestas_alumno: List[Dict]) -> Dict:
        """
        Analiza patrones de errores en las respuestas del alumno
        
        Args:
            respuestas_alumno: Lista de respuestas del alumno
        
        Returns:
            Dict: Análisis de patrones y recomendaciones
        """
        
        errores = [r for r in respuestas_alumno if not r.get("correcto", True)]
        
        if not errores:
            return {
                "patrones_identificados": [],
                "recomendaciones": "El alumno muestra un excelente desempeño sin errores significativos.",
                "areas_fortaleza": ["Resolución precisa", "Comprensión conceptual sólida"]
            }

        PROMPT_ANALISIS = f"""
        Analiza los patrones de errores en las respuestas de un alumno de matemáticas.
        
        **RESPUESTAS INCORRECTAS:**
        {json.dumps(errores, indent=2)}
        
        **ANÁLISIS REQUERIDO:**
        Identifica patrones comunes en los errores y proporciona recomendaciones pedagógicas.
        
        **FORMATO JSON:**
        {{
            "patrones_identificados": [
                {{
                    "patron": "Descripción del patrón de error",
                    "frecuencia": "alta/media/baja",
                    "concepto_afectado": "Concepto matemático involucrado",
                    "ejemplos": ["ejemplo1", "ejemplo2"]
                }}
            ],
            "recomendaciones": "Recomendaciones específicas para mejorar",
            "estrategias_enseñanza": [
                "Estrategia 1 específica",
                "Estrategia 2 específica"
            ],
            "ejercicios_sugeridos": [
                "Tipo de ejercicio 1",
                "Tipo de ejercicio 2"
            ],
            "areas_fortaleza": ["Fortaleza 1", "Fortaleza 2"]
        }}
        """

        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("Eres un especialista en análisis pedagógico que identifica patrones de aprendizaje."),
                    UserMessage(PROMPT_ANALISIS),
                ],
                temperature=0.3,
                top_p=0.9,
                model=self.model
            )
            
            analisis = json.loads(response.choices[0].message.content)
            return analisis
            
        except Exception as e:
            return {
                "patrones_identificados": [],
                "recomendaciones": "No se pudo completar el análisis automático. Se recomienda revisión manual.",
                "error": str(e)
            }