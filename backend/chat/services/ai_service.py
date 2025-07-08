import google.generativeai as genai
from config import settings
from services.cache_service import cache
from typing import List, Dict
import re
import json

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
        """Determina si el mensaje está relacionado con matemáticas usando IA + palabras clave + lógica avanzada"""
        # Primero verifica si el mensaje está vacío o es muy corto
        if not message or len(message.strip()) < 3:
            return False

        # Limpieza del mensaje
        clean_msg = message.lower().strip()
        
        # 1. Detección rápida con palabras clave mejoradas
        math_keywords = {
            'álgebra', 'algebra', 'geometría', 'geometria', 'cálculo', 'calculo', 
            'trigonometría', 'trigonometria', 'estadística', 'estadistica', 
            'ecuación', 'ecuacion', 'función', 'funcion', 'derivada', 'integral', 
            'límite', 'limite', 'suma', 'resta', 'multiplicación', 'multiplicacion', 
            'división', 'division', 'fracción', 'fraccion', 'decimal', 'porcentaje', 
            'probabilidad', 'matriz', 'vector', 'gráfica', 'grafica', 'número', 'numero',
            'matemática', 'matematica', 'matemáticas', 'matematicas', 'resolver', 
            'calcular', 'problema', 'ejercicio', 'fórmula', 'formula', 'teorema', 
            'demostración', 'demostracion', 'polinomio', 'binomio', 'triángulo',
            'triangulo', 'seno', 'coseno', 'tangente', 'logaritmo', 'exponencial',
            'raíz', 'raiz', 'cuadrática', 'cuadratica', 'aritmética', 'aritmetica'
        }
        
        # Símbolos matemáticos y expresiones comunes
        math_symbols = {'+', '-', '*', '/', '=', '²', '³', '√', '∫', '∑', 'π', '^', '∞', '≈', '≠', '≤', '≥'}
        
        # Verificación rápida con palabras clave
        if any(keyword in clean_msg for keyword in math_keywords):
            return True
        
        # Verificación de símbolos matemáticos
        if any(symbol in message for symbol in math_symbols):
            return True
        
        # Patrones numéricos (ecuaciones simples, operaciones)
        if re.search(r'\d+[\+\-\*\/]\d+', message):  # Ej: "5+3", "10/2"
            return True
        
        # 2. Si no se detectó nada claro, usar IA para análisis semántico
        try:
            classification_prompt = f"""
            Eres un clasificador experto en identificar mensajes relacionados con matemáticas.
            Responde únicamente con "SÍ" o "NO" sin comentarios adicionales.

            Considera como matemáticas:
            - Cualquier tema de matemáticas puras o aplicadas
            - Problemas numéricos o lógicos
            - Solicitudes de ayuda con ejercicios matemáticos
            - Conceptos teóricos matemáticos
            - Preguntas sobre procedimientos o fórmulas

            Excluye:
            - Matemáticas muy básicas como contar objetos
            - Números mencionados sin contexto matemático
            - Referencias casuales a números

            Mensaje: "{message}"
            """
            
            response = self.model.generate_content(classification_prompt)
            result = response.text.strip().upper()
            
            # Múltiples variantes de respuesta afirmativa
            positive_responses = {"SÍ", "SI", "YES", "Y", "1", "VERDADERO", "TRUE"}
            return any(pos_res in result for pos_res in positive_responses)
            
        except Exception as e:
            print(f"Error en clasificación por IA: {str(e)}")
            # Fallback: Buscar números con contexto matemático
            if len(re.findall(r'\d+', message)) > 2:  # Si hay varios números
                context_words = {'problema', 'ejercicio', 'resolver', 'calcular', 'hallar', 'encontrar'}
                return any(word in clean_msg for word in context_words)
            return False

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

    def generate_teaching_plan(self, topic: str, level: str = "basico") -> List[str]:
        """Genera un plan de enseñanza paso a paso para un tema"""
        try:
            prompt = f"""
            Crea un plan de enseñanza estructurado para el tema "{topic}" en nivel {level}.
            
            Divide el tema en conceptos específicos que se deben enseñar paso a paso.
            Cada concepto debe ser claro y específico.
            
            Responde con una lista numerada de conceptos, uno por línea.
            Ejemplo:
            1. Definición básica de fracciones
            2. Partes de una fracción: numerador y denominador
            3. Representación visual de fracciones
            4. Fracciones equivalentes
            5. Comparación de fracciones
            
            Tema: {topic}
            Nivel: {level}
            """
            
            response = self.model.generate_content(prompt)
            concepts = []
            for line in response.text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Limpiar numeración
                    concept = line.split('. ', 1)[-1] if '. ' in line else line.lstrip('- •')
                    concepts.append(concept.strip())
            
            return concepts
        except Exception:
            return [f"Conceptos básicos de {topic}", f"Aplicaciones de {topic}", f"Ejercicios de {topic}"]

    def explain_concept(self, concept: str, topic: str, user_context: str = "") -> str:
        """Explica un concepto específico de manera didáctica"""
        try:
            prompt = f"""
            Eres un tutor de matemáticas. Explica el siguiente concepto de manera clara y didáctica:
            
            Concepto: {concept}
            Tema general: {topic}
            Contexto del estudiante: {user_context if user_context else "Estudiante sin experiencia previa"}
            
            La explicación debe:
            1. Ser clara y fácil de entender
            2. Incluir ejemplos prácticos
            3. Usar analogías cuando sea útil
            4. Incluir ejercicios simples para practicar
            5. Estar formateada en markdown
            
            Respuesta:
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            return f"Explicación del concepto: {concept}"

    def generate_exercises(self, topic: str, subtopic: str = None, nivel: str = "facil", cantidad: int = 5) -> List[Dict]:
        """Genera ejercicios para un tema específico"""
        try:
            prompt = f"""
            Genera {cantidad} ejercicios de matemáticas para el tema "{topic}" {f"subtema {subtopic}" if subtopic else ""} de nivel {nivel}.
            
            Cada ejercicio debe seguir EXACTAMENTE este formato JSON:
            {{
                "pregunta": "¿Cuánto es 2 + 3?",
                "respuesta_correcta": "5",
                "tema": "{topic}",
                "subtema": "{subtopic or topic}",
                "es_multiple_choice": true,
                "opciones": ["3", "4", "5", "6"],
                "solucion": ["Paso 1: Identificar variables y operaciones", "Paso 2: Realizar la suma", "Paso 3: Verificar respuesta"],
                "pistas": ["Recuerda que sumar es juntar cantidades", "Piensa en objetos cotidianos para visualizar la suma"],
                "concepto_principal": "Suma de números enteros",
                "nivel": "{nivel}"
            }}
            
            Responde SOLO con un array JSON válido de {cantidad} ejercicios.
            """
            
            response = self.model.generate_content(prompt)
            # Intentar parsear JSON
            import json
            try:
                exercises = json.loads(response.text)
                # Agregar IDs únicos
                for i, ex in enumerate(exercises):
                    ex["exercise_id"] = f"{topic}_{nivel}_{i}_{hash(ex['pregunta']) % 10000}"
                return exercises
            except json.JSONDecodeError:
                # Fallback si el JSON no es válido
                return self._generate_fallback_exercises(topic, subtopic, nivel, cantidad)
                
        except Exception:
            return self._generate_fallback_exercises(topic, subtopic, nivel, cantidad)

    def _generate_fallback_exercises(self, topic: str, subtopic: str, nivel: str, cantidad: int) -> List[Dict]:
        """Genera ejercicios de respaldo si falla la generación por IA"""
        exercises = []
        for i in range(cantidad):
            exercises.append({
                "exercise_id": f"{topic}_{nivel}_{i}_fallback",
                "pregunta": f"Ejercicio {i+1} de {topic}",
                "respuesta_correcta": "Respuesta correcta",
                "tema": topic,
                "subtema": subtopic or topic,
                "es_multiple_choice": False,
                "opciones": None,
                "solucion": [f"Resolver paso a paso el problema de {topic}"],
                "pistas": [f"Recuerda los conceptos básicos de {topic}"],
                "concepto_principal": topic,
                "nivel": nivel
            })
        return exercises

    def is_learning_session_active(self, user_id: str) -> dict:
        """Verifica si el usuario tiene una sesión de aprendizaje activa"""
        from services.learning_service import learning_service
        sessions = learning_service.get_user_sessions(user_id, status="active")
        return sessions[0] if sessions else None

    def generate_contextual_response(self, message: str, session_context: dict = None) -> str:
        """Genera respuesta contextual considerando la sesión de aprendizaje activa"""
        try:
            if session_context:
                topic = session_context.get("topic")
                concepts_covered = session_context.get("concepts_covered", [])
                level = session_context.get("level", "basico")
                
                prompt = f"""
                Eres un tutor de matemáticas especializado. El estudiante está en una sesión de aprendizaje del tema "{topic}" nivel {level}.
                
                Conceptos ya cubiertos en esta sesión:
                {chr(10).join(f"- {concept}" for concept in concepts_covered) if concepts_covered else "Ninguno aún"}
                
                INSTRUCCIONES:
                1. Si pregunta sobre el tema actual, responde de manera didáctica y clara
                2. Si pide ejercicios, ofrece crear ejercicios del tema actual
                3. Si pregunta algo fuera del tema, sugiere amablemente volver al tema de estudio
                4. Si pide explicar un concepto, hazlo paso a paso con ejemplos
                5. Si pide continuar con el siguiente concepto, guíalo al siguiente paso
                6. Usa un tono motivador y educativo
                
                Pregunta del estudiante: "{message}"
                
                Respuesta (en markdown):
                """
            else:
                # Chat normal sin sesión activa
                prompt = f"""
                Eres un tutor de matemáticas. El estudiante no tiene una sesión de aprendizaje activa.
                
                INSTRUCCIONES:
                1. Si pregunta sobre matemáticas, responde de manera clara y educativa
                2. Si quiere aprender un tema específico, sugiere crear una sesión de aprendizaje
                3. Puedes ofrecer explicaciones, ejemplos y ejercicios puntuales
                4. Mantén un tono amigable y motivador
                
                Pregunta: "{message}"
                
                Respuesta (en markdown):
                """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            return "Lo siento, hubo un error procesando tu pregunta. ¿Podrías reformularla?"

    def analyze_student_intent(self, message: str) -> dict:
        """Analiza la intención del estudiante en su mensaje"""
        try:
            prompt = f"""
            Analiza el siguiente mensaje de un estudiante y determina su intención principal.
            
            Mensaje: "{message}"
            
            Responde con un JSON con esta estructura:
            {{
                "intent": "pregunta_concepto|pedir_ejercicios|continuar_leccion|duda_especifica|crear_sesion|otro",
                "topic_mentioned": "tema mencionado o null",
                "needs_explanation": true/false,
                "wants_practice": true/false,
                "confidence": 0.8
            }}
            """
            
            response = self.model.generate_content(prompt)
            import json
            try:
                return json.loads(response.text)
            except:
                return {"intent": "otro", "confidence": 0.5}
        except Exception:
            return {"intent": "otro", "confidence": 0.5}

    def analyze_student_progress(self, user_id: str, session_data: dict = None) -> dict:
        """Analiza el progreso del estudiante basado en su historial"""
        try:
            from services.learning_service import learning_service
            
            # Obtener todas las sesiones del usuario
            all_sessions = learning_service.get_user_sessions(user_id)
            
            # Obtener contexto de Qdrant para análisis avanzado
            from services.qdrant_service import qdrant
            user_contexts = qdrant.get_user_learning_progress(user_id)
            
            # Datos de análisis
            total_sessions = len(all_sessions)
            completed_sessions = len([s for s in all_sessions if s.get('status') == 'completed'])
            topics_studied = list(set([s.get('topic') for s in all_sessions if s.get('topic')]))
            
            # Calcular estadísticas de ejercicios
            total_exercises = 0
            correct_exercises = 0
            difficulty_performance = {"facil": {"total": 0, "correct": 0}, 
                                   "intermedio": {"total": 0, "correct": 0}, 
                                   "dificil": {"total": 0, "correct": 0}}
            
            for session in all_sessions:
                exercises = session.get('exercises_completed', [])
                for ex in exercises:
                    total_exercises += 1
                    if ex.get('is_correct'):
                        correct_exercises += 1
                    
                    diff = ex.get('difficulty', 'facil')
                    if diff in difficulty_performance:
                        difficulty_performance[diff]['total'] += 1
                        if ex.get('is_correct'):
                            difficulty_performance[diff]['correct'] += 1
            
            # Análisis con IA
            progress_prompt = f"""
            Analiza el progreso de aprendizaje de este estudiante:
            
            DATOS:
            - Sesiones totales: {total_sessions}
            - Sesiones completadas: {completed_sessions}
            - Temas estudiados: {', '.join(topics_studied)}
            - Ejercicios totales: {total_exercises}
            - Respuestas correctas: {correct_exercises}
            - Precisión general: {(correct_exercises/total_exercises*100) if total_exercises > 0 else 0:.1f}%
            - Rendimiento por dificultad: {difficulty_performance}
            
            Responde con un JSON:
            {{
                "nivel_actual": "principiante|basico|intermedio|avanzado",
                "areas_fuertes": ["tema1", "tema2"],
                "areas_debiles": ["tema1", "tema2"],
                "siguiente_tema_recomendado": "tema",
                "dificultad_recomendada": "facil|intermedio|dificil",
                "consejos_mejora": ["consejo1", "consejo2", "consejo3"],
                "motivacion": "mensaje motivacional personalizado",
                "tiempo_estudio_sugerido": "15-30 minutos diarios"
            }}
            """
            
            response = self.model.generate_content(progress_prompt)
            analysis = json.loads(response.text)
            
            # Combinar con datos reales
            return {
                **analysis,
                "estadisticas_reales": {
                    "total_sessions": total_sessions,
                    "completed_sessions": completed_sessions,
                    "topics_studied": topics_studied,
                    "total_exercises": total_exercises,
                    "correct_exercises": correct_exercises,
                    "overall_accuracy": (correct_exercises/total_exercises*100) if total_exercises > 0 else 0,
                    "difficulty_performance": difficulty_performance
                }
            }
            
        except Exception as e:
            print(f"Error en análisis de progreso: {e}")
            return {
                "nivel_actual": "principiante",
                "consejos_mejora": ["Practica regularmente", "No te rindas", "Pide ayuda cuando lo necesites"],
                "motivacion": "¡Sigue adelante! Cada problema resuelto te acerca más a dominar las matemáticas.",
                "estadisticas_reales": {"total_sessions": 0, "total_exercises": 0}
            }

    def generate_adaptive_exercises(self, user_id: str, topic: str, cantidad: int = 5) -> List[Dict]:
        """Genera ejercicios adaptativos basados en el rendimiento del estudiante"""
        try:
            # Analizar progreso para determinar dificultad apropiada
            progress = self.analyze_student_progress(user_id)
            
            # Determinar nivel de dificultad basado en rendimiento
            overall_accuracy = progress.get('estadisticas_reales', {}).get('overall_accuracy', 0)
            
            if overall_accuracy >= 80:
                nivel = "intermedio"
            elif overall_accuracy >= 60:
                nivel = "facil"
            elif overall_accuracy >= 40:
                nivel = "facil"
            else:
                nivel = "facil"  # Mantener fácil para construir confianza
            
            # Si ha mostrado dominio en fácil, subir a intermedio
            diff_perf = progress.get('estadisticas_reales', {}).get('difficulty_performance', {})
            facil_accuracy = 0
            if diff_perf.get('facil', {}).get('total', 0) > 0:
                facil_accuracy = (diff_perf['facil']['correct'] / diff_perf['facil']['total']) * 100
            
            if facil_accuracy >= 85 and diff_perf.get('facil', {}).get('total', 0) >= 5:
                nivel = "intermedio"
            
            # Generar ejercicios con el nivel adaptado
            prompt = f"""
            Genera {cantidad} ejercicios adaptativos de matemáticas para el tema "{topic}" nivel {nivel}.
            
            CONTEXTO DEL ESTUDIANTE:
            - Nivel actual: {progress.get('nivel_actual', 'principiante')}
            - Precisión general: {overall_accuracy:.1f}%
            - Áreas fuertes: {', '.join(progress.get('areas_fuertes', []))}
            - Áreas débiles: {', '.join(progress.get('areas_debiles', []))}
            
            INSTRUCCIONES:
            1. Adapta la dificultad al nivel del estudiante
            2. Si tiene áreas débiles relacionadas, inclúyelas sutilmente
            3. Proporciona pistas más detalladas si tiene baja precisión
            4. Incluye variedad en tipos de problemas
            
            Cada ejercicio debe seguir este formato JSON:
            {{
                "pregunta": "pregunta clara y específica",
                "respuesta_correcta": "respuesta",
                "tema": "{topic}",
                "subtema": "subtema específico",
                "es_multiple_choice": true/false,
                "opciones": ["op1", "op2", "op3", "op4"] o null,
                "solucion": ["paso 1", "paso 2", "paso 3"],
                "pistas": ["pista progresiva 1", "pista progresiva 2"],
                "concepto_principal": "concepto clave",
                "nivel": "{nivel}",
                "tipo_adaptacion": "refuerzo|desafio|revision",
                "tiempo_estimado": "2-5 minutos"
            }}
            
            Responde SOLO con un array JSON de {cantidad} ejercicios.
            """
            
            response = self.model.generate_content(prompt)
            exercises = json.loads(response.text)
            
            # Agregar IDs únicos y metadatos de adaptación
            for i, ex in enumerate(exercises):
                ex["exercise_id"] = f"adaptive_{topic}_{nivel}_{i}_{hash(ex['pregunta']) % 10000}"
                ex["generated_for_user"] = user_id
                ex["adaptation_level"] = nivel
                ex["user_accuracy_when_generated"] = overall_accuracy
            
            return exercises
            
        except Exception as e:
            print(f"Error generando ejercicios adaptativos: {e}")
            # Fallback a ejercicios normales
            return self.generate_exercises(topic, nivel="facil", cantidad=cantidad)

    def generate_personalized_advice(self, user_id: str, recent_performance: dict = None) -> dict:
        """Genera consejos personalizados basados en el rendimiento reciente"""
        try:
            progress = self.analyze_student_progress(user_id)
            
            advice_prompt = f"""
            Eres un tutor experto en matemáticas. Genera consejos personalizados para este estudiante:
            
            PERFIL DEL ESTUDIANTE:
            - Nivel: {progress.get('nivel_actual', 'principiante')}
            - Temas estudiados: {', '.join(progress.get('estadisticas_reales', {}).get('topics_studied', []))}
            - Precisión general: {progress.get('estadisticas_reales', {}).get('overall_accuracy', 0):.1f}%
            - Áreas fuertes: {', '.join(progress.get('areas_fuertes', []))}
            - Áreas débiles: {', '.join(progress.get('areas_debiles', []))}
            
            Genera consejos específicos y accionables en este formato JSON:
            {{
                "consejo_principal": "consejo más importante",
                "estrategias_estudio": ["estrategia 1", "estrategia 2", "estrategia 3"],
                "ejercicios_recomendados": ["tipo de ejercicio 1", "tipo de ejercicio 2"],
                "habitos_sugeridos": ["hábito 1", "hábito 2"],
                "mensaje_motivacional": "mensaje personalizado y motivador",
                "proximos_pasos": ["paso 1", "paso 2", "paso 3"],
                "tiempo_estudio_diario": "15-30 minutos",
                "frecuencia_recomendada": "3-4 veces por semana"
            }}
            """
            
            response = self.model.generate_content(advice_prompt)
            return json.loads(response.text)
            
        except Exception as e:
            print(f"Error generando consejos: {e}")
            return {
                "consejo_principal": "Practica un poco cada día, la constancia es clave en matemáticas",
                "mensaje_motivacional": "¡Cada problema que resuelves te hace más fuerte en matemáticas!",
                "proximos_pasos": ["Repasa conceptos básicos", "Practica ejercicios", "Pide ayuda cuando la necesites"]
            }

    def update_user_progress_context(self, user_id: str, session_id: str, activity_data: dict):
        """Actualiza el contexto de progreso del usuario en Qdrant"""
        try:
            from services.qdrant_service import qdrant
            
            # Crear texto de contexto de progreso
            activity_type = activity_data.get('type', 'unknown')
            topic = activity_data.get('topic', 'matemáticas')
            
            if activity_type == 'exercise_completed':
                is_correct = activity_data.get('is_correct', False)
                difficulty = activity_data.get('difficulty', 'facil')
                context_text = f"Ejercicio de {topic} nivel {difficulty}: {'CORRECTO' if is_correct else 'INCORRECTO'}"
                
            elif activity_type == 'concept_learned':
                concept = activity_data.get('concept', 'concepto')
                context_text = f"Concepto aprendido en {topic}: {concept}"
                
            elif activity_type == 'session_completed':
                duration = activity_data.get('duration_minutes', 0)
                concepts_count = activity_data.get('concepts_count', 0)
                context_text = f"Sesión de {topic} completada: {concepts_count} conceptos en {duration} minutos"
                
            elif activity_type == 'question_asked':
                question = activity_data.get('question', 'pregunta')[:100]
                context_text = f"Pregunta sobre {topic}: {question}"
                
            else:
                context_text = f"Actividad en {topic}: {activity_data.get('description', 'actividad de aprendizaje')}"
            
            # Guardar en Qdrant con metadatos de progreso
            qdrant.upsert_context(
                user_id=user_id,
                text=context_text,
                embedding=self.get_embedding(context_text),
                conversation_id=f"progress_{user_id}",
                context_type="learning_progress",
                metadata={
                    "session_id": session_id,
                    "activity_type": activity_type,
                    "topic": topic,
                    "timestamp": activity_data.get('timestamp'),
                    **activity_data
                }
            )
            
        except Exception as e:
            print(f"Error actualizando contexto de progreso: {e}")

    def get_next_recommended_topic(self, user_id: str) -> dict:
        """Recomienda el siguiente tema a estudiar basado en el progreso"""
        try:
            progress = self.analyze_student_progress(user_id)
            
            recommendation_prompt = f"""
            Basado en el progreso del estudiante, recomienda el siguiente tema a estudiar:
            
            ESTUDIANTE:
            - Nivel actual: {progress.get('nivel_actual')}
            - Temas estudiados: {', '.join(progress.get('estadisticas_reales', {}).get('topics_studied', []))}
            - Áreas fuertes: {', '.join(progress.get('areas_fuertes', []))}
            - Áreas débiles: {', '.join(progress.get('areas_debiles', []))}
            - Precisión: {progress.get('estadisticas_reales', {}).get('overall_accuracy', 0):.1f}%
            
            Responde con JSON:
            {{
                "tema_recomendado": "tema específico",
                "razon": "por qué este tema es el siguiente lógico",
                "prerequisitos": ["prerrequisito1", "prerrequisito2"],
                "dificultad_estimada": "facil|intermedio|dificil",
                "tiempo_estimado": "2-3 semanas",
                "conceptos_clave": ["concepto1", "concepto2", "concepto3"]
            }}
            """
            
            response = self.model.generate_content(recommendation_prompt)
            return json.loads(response.text)
            
        except Exception as e:
            print(f"Error en recomendación de tema: {e}")
            return {
                "tema_recomendado": "Aritmética básica",
                "razon": "Es fundamental para construir una base sólida",
                "dificultad_estimada": "facil"
            }

ai = AIService()