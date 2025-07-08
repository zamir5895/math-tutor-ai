from fastapi import FastAPI, HTTPException
from services.ai_service import ai
from services.qdrant_service import qdrant
from services.mongo_service import mongo
from services.learning_service import learning_service
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from schemas import (
    UserMessage, AIResponse, CreateLearningSessionRequest, LearningSession, Exercise, 
    ExerciseRequest, ExerciseResponse, DifficultyLevel, SessionHistoryResponse, 
    SessionSummaryStats, ReactivateSessionRequest, SessionChatMessage, ProgressAnalysis,
    PersonalizedAdvice, TopicRecommendation, UserRecommendations, AdaptiveExerciseRequest,
    ExerciseCompletion, ConceptLearning
)
from datetime import datetime
import uuid
import logging
import json
from bson import ObjectId
import tempfile

app = FastAPI(
    title="Matemix Chat Service",
    description="Microservicio especializado en tutorías de matemáticas con IA",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_context_prompt(user_id: str, message: str, conversation_id: str) -> str:
    """Genera el prompt con contexto específico del usuario y conversación"""
    query_embedding = ai.get_embedding(message)
    
    conversation_contexts = qdrant.search_context(user_id, query_embedding, conversation_id, limit=3)
    
    general_contexts = qdrant.search_general_context(user_id, query_embedding, limit=2)
    
    context_texts = []
    
    for hit in conversation_contexts:
        context_texts.append(f"Contexto de conversación: {hit.payload['text']}")
    
    for hit in general_contexts:
        context_texts.append(f"Contexto general: {hit.payload['text']}")
    
    return f"""
    Eres un tutor especializado en matemáticas. SOLO responde preguntas relacionadas con matemáticas.
    
    Si la pregunta NO es sobre matemáticas, responde: "Lo siento, soy un tutor especializado en matemáticas y solo puedo ayudarte con temas relacionados a esta materia. ¿Tienes alguna pregunta de matemáticas en la que pueda ayudarte?"
    
    Contexto relevante del usuario:
    {chr(10).join(context_texts) if context_texts else "Sin contexto previo"}
    
    Pregunta del usuario:
    {message}
    
    Respuesta (en markdown):
    """

@app.post("/chat-stream")
async def chat_stream(message: UserMessage):
    """Endpoint de chat inteligente con soporte para sesiones de aprendizaje"""
    conversation_id = message.conversation_id or str(uuid.uuid4())
    
    is_first_message = message.conversation_id is None
    
    active_session = ai.is_learning_session_active(message.user_id)
    
    student_intent = ai.analyze_student_intent(message.message)
    
    if not ai.is_math_related(message.message) and not active_session:
        non_math_response = """Lo siento, soy un tutor especializado en matemáticas y solo puedo ayudarte con temas relacionados a esta materia. 

¿Te gustaría que te ayude con alguno de estos temas?
- Álgebra básica
- Geometría 
- Fracciones
- Ecuaciones
- O cualquier otro tema de matemáticas

También puedo crear una sesión de aprendizaje personalizada para ti. ¿Qué te interesa aprender?"""
        
        mongo.save_message(message.user_id, conversation_id, "user", message.message)
        mongo.save_message(message.user_id, conversation_id, "assistant", non_math_response)
        
        def non_math_stream():
            yield f"data: {json.dumps({'text': non_math_response, 'conversation_id': conversation_id})}\n\n"
        
        return StreamingResponse(non_math_stream(), media_type="text/event-stream")
    
    mongo.save_message(message.user_id, conversation_id, "user", message.message)
    
    if is_first_message:
        title = ai.generate_title(message.message)
        mongo.set_conversation_title(message.user_id, conversation_id, title)
    
    special_response = None
    if student_intent.get("intent") == "pedir_ejercicios":
        topic = student_intent.get("topic_mentioned") or (active_session.get("topic") if active_session else None)
        if topic:
            if active_session:
                exercises = learning_service.get_adaptive_exercises_for_user(message.user_id, topic, 3)
                difficulty_note = "adaptativos basados en tu progreso"
            else:
                exercises = ai.generate_exercises(topic, nivel="facil", cantidad=3)
                difficulty_note = "nivel básico"
            
            special_response = f"""¡Perfecto! He generado ejercicios {difficulty_note} de {topic} para ti.
            
Tienes varias opciones:
1. **Usar el endpoint `/tutor/exercises/{message.user_id}/next-batch?topic={topic}`** para ejercicios personalizados
2. **Crear una sesión de aprendizaje** con `/learning/session/create` para un seguimiento completo
3. **Ver tu dashboard** en `/tutor/dashboard/{message.user_id}` para análisis de progreso

¿Prefieres que te explique algún concepto primero o quieres empezar directamente con los ejercicios?"""
            
    elif student_intent.get("intent") == "crear_sesion":
        topic = student_intent.get("topic_mentioned", "matemáticas")
        special_response = f"""¡Excelente idea crear una sesión de aprendizaje de {topic}! 

**Para el frontend, usa estos endpoints:**
- `POST /learning/session/create` - Crear la sesión
- `GET /tutor/progress/{message.user_id}` - Ver tu progreso actual
- `GET /tutor/recommendations/{message.user_id}` - Obtener recomendaciones personalizadas

Una vez creada la sesión, podrás:
✅ Chatear libremente dentro de la sesión
✅ Generar ejercicios adaptativos automáticamente  
✅ Recibir consejos personalizados basados en tu progreso
✅ Exportar reportes PDF completos

¿Quieres que te recomiende el mejor tema para empezar basado en tu nivel?"""
    
    elif active_session and student_intent.get("intent") == "pregunta_concepto":
        topic = active_session.get("topic")
        progress = learning_service.get_user_progress_analysis(message.user_id)
        
        special_response = f"""Perfecto, estás en tu sesión de {topic}. 

**Tu progreso actual:**
- Nivel: {progress.get('nivel_actual', 'principiante')}
- Precisión: {progress.get('estadisticas_reales', {}).get('overall_accuracy', 0):.1f}%

Basándome en tu progreso, voy a explicarte esto de manera personalizada..."""
    
    if special_response:
        response_text = special_response
    else:
        response_text = ai.generate_contextual_response(message.message, active_session)
    
    def event_stream():
        if special_response:
            full_response = response_text
            yield f"data: {json.dumps({'text': response_text, 'conversation_id': conversation_id, 'session_active': bool(active_session)})}\n\n"
        else:
            response = ai.model.generate_content(
                response_text,
                stream=True 
            )
            
            full_response = ""
            for chunk in response:
                chunk_text = chunk.text
                full_response += chunk_text
                yield f"data: {json.dumps({'text': chunk_text, 'conversation_id': conversation_id, 'session_active': bool(active_session)})}\n\n"

        mongo.save_message(message.user_id, conversation_id, "assistant", full_response)
        
        interaction_text = f"P: {message.message}\nR: {full_response}"
        qdrant.upsert_context(
            user_id=message.user_id,
            text=interaction_text,
            embedding=ai.get_embedding(interaction_text),
            conversation_id=conversation_id,
            context_type="conversation",
            metadata={
                "type": "interaction", 
                "session_id": active_session.get("session_id") if active_session else None,
                "topic": active_session.get("topic") if active_session else None
            }
        )
        
        if active_session and len(full_response) > 50:
            learning_service.update_session_concepts(
                active_session["session_id"], 
                [f"Concepto discutido: {message.message[:100]}"]
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )

@app.get("/conversation/{user_id}/{conversation_id}")
async def get_conversation(user_id: str, conversation_id: str):
    conversation = mongo.get_conversation(user_id, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    conversation.pop("_id", None)
    
    logger.info(f"Retrieved conversation for user {user_id} with ID {conversation_id}")
    return conversation

@app.get("/conversations/{user_id}")
async def list_conversations(user_id: str):
    try:
        conversations_cursor = mongo.get_conversations_list(user_id)
        conversations = list(conversations_cursor)
        
        result = []
        for conv in conversations:
            if not conv.get("messages"):
                continue
            
            last_msg = conv["messages"][-1]
            updated_at = conv.get("updated_at", datetime.utcnow())
            
            result.append({
                "id": conv.get("conversation_id"),
                "title": conv.get("title", "Conversación sin título"),
                "last_message": last_msg.get("content", "")[:100] + "..." if len(last_msg.get("content", "")) > 100 else last_msg.get("content", ""),
                "updated_at": updated_at.isoformat() if hasattr(updated_at, 'isoformat') else str(updated_at)
            })
        
        return result
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
async def root():
    return {
        "message": "🎓 Matemix AI - Tutor Completo de Matemáticas con IA Avanzada",
        "version": "4.0.0",
        "description": "Sistema completo de tutoría matemática con IA que adapta ejercicios, analiza progreso y proporciona recomendaciones personalizadas",
        "features": [
            "🧠 Chat inteligente con filtro matemático avanzado",
            "📚 Sesiones de aprendizaje persistentes y contextuales",
            "🎯 Ejercicios adaptativos basados en progreso individual",
            "📊 Análisis completo de progreso y debilidades",
            "� Recomendaciones personalizadas con IA",
            "🔄 Seguimiento continuo en Qdrant Vector DB",
            "� Dashboard completo para estudiantes",
            "🎨 Consejos y motivación personalizada",
            "📄 Reportes PDF detallados de aprendizaje",
            "⚡ API completa para integración frontend"
        ],
        "api_sections": {
            "🎯 Tutor IA Completo": {
                "dashboard": "/tutor/dashboard/{user_id}",
                "analisis_progreso": "/tutor/progress/{user_id}",
                "recomendaciones": "/tutor/recommendations/{user_id}",
                "ejercicios_adaptativos": "/tutor/exercises/adaptive",
                "siguiente_lote": "/tutor/exercises/{user_id}/next-batch",
                "completar_ejercicio": "/tutor/exercise/complete",
                "aprender_concepto": "/tutor/concept/learn"
            },
            "📚 Sesiones de Aprendizaje": {
                "crear_sesion": "/learning/session/create",
                "chat_en_sesion": "/learning/session/{session_id}/chat",
                "historial_completo": "/learning/session/{session_id}/history",
                "estadisticas": "/learning/session/{session_id}/stats",
                "reactivar": "/learning/session/{session_id}/reactivate",
                "sesiones_activas": "/learning/sessions/{user_id}/active"
            },
            "📄 Reportes y Análisis": {
                "reporte_pdf": "/learning/session/{session_id}/pdf-report",
                "ejercicios_pdf": "/learning/session/{session_id}/pdf-exercises",
                "conversaciones": "/conversations/{user_id}"
            },
            "💬 Chat General": {
                "chat_libre": "/chat-stream",
                "eliminar_conversacion": "/conversation/{user_id}/{conversation_id}"
            }
        },
        "frontend_integration": {
            "flujo_completo": [
                "1. 📊 Obtener dashboard: GET /tutor/dashboard/{user_id}",
                "2. 🎯 Ver recomendaciones: GET /tutor/recommendations/{user_id}",
                "3. 📚 Crear/reactivar sesión según recomendación",
                "4. 💬 Chatear en la sesión libremente", 
                "5. 📝 Solicitar ejercicios adaptativos",
                "6. ✅ Completar ejercicios con tracking automático",
                "7. 📈 Ver progreso actualizado en tiempo real",
                "8. 📄 Generar reportes PDF cuando se desee"
            ],
            "llamadas_principales": {
                "obtener_ejercicios": "POST /tutor/exercises/adaptive",
                "completar_ejercicio": "POST /tutor/exercise/complete", 
                "dashboard_estudiante": "GET /tutor/dashboard/{user_id}",
                "chat_inteligente": "POST /chat-stream"
            }
        },
        "ai_capabilities": [
            "🎯 Detección automática de nivel de estudiante",
            "📊 Análisis de patrones de aprendizaje",
            "🎨 Generación de ejercicios personalizados",
            "💡 Consejos adaptativos basados en errores",
            "🔄 Seguimiento de progreso en vector database",
            "🎓 Recomendaciones de temas siguientes",
            "❤️ Motivación personalizada"
        ],
        "documentation": "/docs",
        "ejemplo_uso": {
            "descripcion": "Ejemplo de flujo para el frontend",
            "paso_1": "GET /tutor/dashboard/user123 - Obtener estado actual",
            "paso_2": "POST /tutor/exercises/adaptive - Generar ejercicios personalizados",
            "paso_3": "POST /tutor/exercise/complete - Enviar respuesta con tracking",
            "paso_4": "GET /tutor/recommendations/user123 - Ver nuevas recomendaciones"
        }
    }

@app.delete("/conversation/{user_id}/{conversation_id}")
async def delete_conversation(user_id: str, conversation_id: str):
    try:
        deleted = mongo.delete_conversation(user_id, conversation_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
        
        qdrant.delete_conversation_context(user_id, conversation_id)
        
        logger.info(f"Deleted conversation {conversation_id} for user {user_id}")
        return {"message": "Conversación eliminada correctamente"}
    
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/learning/session/create")
async def create_learning_session(request: CreateLearningSessionRequest):
    """Crea una nueva sesión de aprendizaje estructurada (compatible con EventSource/SSE)"""
    try:
        session_id = learning_service.create_learning_session(
            user_id=request.user_id,
            topic=request.topic,
            subtopic=request.subtopic,
            level=request.level
        )
        
        teaching_plan = ai.generate_teaching_plan(request.topic, request.level)
        learning_service.update_session_concepts(session_id, teaching_plan)
        logger.info(f"Created learning session {session_id} for user {request.user_id}")

        def event_stream():
            # Puedes emitir varios eventos si quieres mostrar progreso paso a paso
            yield f"data: {json.dumps({'status': 'created', 'session_id': session_id})}\n\n"
            yield f"data: {json.dumps({'status': 'teaching_plan', 'teaching_plan': teaching_plan})}\n\n"
            yield f"data: {json.dumps({'status': 'done', 'session_id': session_id, 'topic': request.topic, 'subtopic': request.subtopic, 'level': request.level, 'teaching_plan': teaching_plan, 'message': f'Sesión de aprendizaje creada para {request.topic}. Comenzaremos con {len(teaching_plan)} conceptos.'})}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Error creating learning session: {str(e)}")
        def error_stream():
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

@app.get("/learning/session/{session_id}")
async def get_learning_session(session_id: str):
    """Obtiene información de una sesión de aprendizaje"""
    session = learning_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    session.pop("_id", None)
    return session

@app.post("/learning/session/{session_id}/teach/{concept_index}")
async def teach_concept(session_id: str, concept_index: int):
    """Enseña un concepto específico de la sesión"""
    try:
        session = learning_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        concepts = session.get("concepts_covered", [])
        if concept_index >= len(concepts):
            raise HTTPException(status_code=400, detail="Índice de concepto inválido")
        
        concept = concepts[concept_index]
        
        explanation = ai.explain_concept(
            concept=concept,
            topic=session["topic"],
            user_context=f"Sesión de aprendizaje de {session['topic']}"
        )
        
        return {
            "session_id": session_id,
            "concept_index": concept_index,
            "concept": concept,
            "explanation": explanation,
            "progress": f"{concept_index + 1}/{len(concepts)}"
        }
    except Exception as e:
        logger.error(f"Error teaching concept: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learning/session/{session_id}/complete")
async def complete_learning_session(session_id: str):
    """Marca una sesión como completada"""
    try:
        session = learning_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        learning_service.complete_session(session_id)
        
        return {
            "session_id": session_id,
            "message": "Sesión completada exitosamente",
            "concepts_learned": len(session.get("concepts_covered", [])),
            "next_steps": "Puedes generar ejercicios o un reporte de tu aprendizaje"
        }
    except Exception as e:
        logger.error(f"Error completing session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/exercises/generate")
async def generate_exercises(request: ExerciseRequest):
    """Genera ejercicios para un tema específico"""
    try:
        exercises = ai.generate_exercises(
            topic=request.topic,
            subtopic=request.subtopic,
            nivel=request.nivel.value,
            cantidad=request.cantidad
        )
        
        exercise_ids = []
        for exercise in exercises:
            exercise_id = learning_service.save_exercise(exercise)
            exercise_ids.append(exercise_id)
        
        logger.info(f"Generated {len(exercises)} exercises for topic {request.topic}")
        
        return {
            "topic": request.topic,
            "subtopic": request.subtopic,
            "nivel": request.nivel,
            "exercises": exercises,
            "message": f"Se generaron {len(exercises)} ejercicios de {request.topic}"
        }
    except Exception as e:
        logger.error(f"Error generating exercises: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exercises/topic/{topic}")
async def get_exercises_by_topic(topic: str, nivel: str = None, limit: int = 5):
    """Obtiene ejercicios guardados por tema"""
    exercises = learning_service.get_exercises_by_topic(topic, nivel, limit)
    return {
        "topic": topic,
        "nivel": nivel,
        "exercises": exercises,
        "count": len(exercises)
    }

@app.post("/exercises/submit")
async def submit_exercise_response(response: ExerciseResponse):
    """Envía respuesta a un ejercicio"""
    try:
        exercise = learning_service.exercises.find_one({"exercise_id": response.exercise_id})
        if not exercise:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
        
        es_correcto = response.respuesta_usuario.strip().lower() == exercise["respuesta_correcta"].strip().lower()
        
        learning_service.save_exercise_response(
            user_id=response.user_id,
            exercise_id=response.exercise_id,
            respuesta_usuario=response.respuesta_usuario,
            es_correcto=es_correcto,
            tiempo_respuesta=response.tiempo_respuesta
        )
        
        feedback = "¡Correcto! Excelente trabajo." if es_correcto else f"Incorrecto. La respuesta correcta es: {exercise['respuesta_correcta']}"
        
        return {
            "exercise_id": response.exercise_id,
            "es_correcto": es_correcto,
            "respuesta_correcta": exercise["respuesta_correcta"],
            "feedback": feedback,
            "solucion": exercise.get("solucion", []),
            "pistas": exercise.get("pistas", []) if not es_correcto else []
        }
    except Exception as e:
        logger.error(f"Error submitting exercise response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exercises/stats/{user_id}")
async def get_exercise_stats(user_id: str, topic: str = None):
    """Obtiene estadísticas de ejercicios del usuario"""
    stats = learning_service.get_user_exercise_stats(user_id, topic)
    return {
        "user_id": user_id,
        "topic": topic,
        "stats": stats
    }


@app.get("/learning/report/{session_id}")
async def generate_learning_report(session_id: str):
    """Genera reporte PDF de una sesión de aprendizaje"""
    try:
        session = learning_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        exercise_stats = learning_service.get_user_exercise_stats(session["user_id"])
        
        
        report_data = {
            "session_id": session_id,
            "user_id": session["user_id"],
            "topic": session["topic"],
            "subtopic": session.get("subtopic"),
            "concepts_learned": session.get("concepts_covered", []),
            "level": session.get("level"),
            "status": session.get("status"),
            "created_at": session.get("created_at"),
            "updated_at": session.get("updated_at"),
            "exercise_stats": exercise_stats,
            "message": "Reporte generado exitosamente"
        }
        
        logger.info(f"Generated report for session {session_id}")
        return report_data
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/sessions/{user_id}")
async def get_user_learning_sessions(user_id: str, status: str = None):
    """Obtiene todas las sesiones de aprendizaje de un usuario"""
    sessions = learning_service.get_user_sessions(user_id, status)
    for session in sessions:
        session.pop("_id", None)
    
    return {
        "user_id": user_id,
        "status_filter": status,
        "sessions": sessions,
        "count": len(sessions)
    }


@app.post("/learning/session/{session_id}/chat")
async def learning_session_chat(session_id: str, message: UserMessage):
    """Chat interactivo dentro de una sesión de aprendizaje"""
    try:
        session = learning_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        if session["user_id"] != message.user_id:
            raise HTTPException(status_code=403, detail="Acceso denegado a esta sesión")
        
        conversation_id = f"learning_{session_id}"
        
        mongo.save_message(message.user_id, conversation_id, "user", message.message)
        
        intent = ai.analyze_student_intent(message.message)
        
        def event_stream():
            if intent.get("intent") == "pedir_ejercicios":
                exercises = ai.generate_exercises(
                    topic=session["topic"],
                    subtopic=session.get("subtopic"),
                    nivel="facil",
                    cantidad=3
                )
                
                response_text = f"""¡Perfecto! He generado algunos ejercicios de {session['topic']} para ti:

"""
                for i, ex in enumerate(exercises, 1):
                    response_text += f"""**Ejercicio {i}:**
{ex['pregunta']}

"""
                    if ex.get('opciones'):
                        for j, opcion in enumerate(ex['opciones'], 1):
                            response_text += f"{j}. {opcion}\n"
                    response_text += "\n"
                
                response_text += "¿Quieres intentar resolverlos? Puedes escribir tus respuestas y te ayudo a verificarlas."
                
                for ex in exercises:
                    learning_service.save_exercise(ex)
                
            elif intent.get("intent") == "continuar_leccion":
                concepts = session.get("concepts_covered", [])
                current_progress = len([c for c in concepts if "Concepto discutido:" not in c])
                
                if current_progress < len(concepts):
                    next_concept = concepts[current_progress]
                    explanation = ai.explain_concept(
                        concept=next_concept,
                        topic=session["topic"],
                        user_context=f"Sesión de aprendizaje - ya vimos: {', '.join(concepts[:current_progress])}"
                    )
                    response_text = f"**Siguiente concepto: {next_concept}**\n\n{explanation}"
                else:
                    response_text = "¡Excelente! Has completado todos los conceptos de esta sesión. ¿Te gustaría hacer algunos ejercicios de práctica o generar un reporte de tu aprendizaje?"
            
            else:
                response_text = ai.generate_contextual_response(message.message, session)
            mongo.save_message(message.user_id, conversation_id, "assistant", response_text)
            yield f"data: {json.dumps({'text': response_text, 'session_id': session_id, 'topic': session['topic']})}\n\n"
            
            learning_service.add_session_interaction(
                session_id, 
                "question", 
                message.message,
                {"intent": intent.get("intent", "unknown")}
            )
            
            learning_service.add_session_interaction(
                session_id, 
                "answer", 
                response_text,
                {"response_type": intent.get("intent", "general")}
            )
            
            # Actualizar contexto de la sesión
            interaction_text = f"P: {message.message}\nR: {response_text}"
            qdrant.upsert_context(
                user_id=message.user_id,
                text=interaction_text,
                embedding=ai.get_embedding(interaction_text),
                conversation_id=conversation_id,
                context_type="conversation",
                metadata={
                    "type": "learning_interaction",
                    "session_id": session_id,
                    "topic": session["topic"]
                }
            )
            
            if intent.get("intent") == "pedir_ejercicios" and 'exercises' in locals():
                for ex in exercises:
                    learning_service.add_session_interaction(
                        session_id,
                        "exercise",
                        f"Ejercicio generado: {ex['pregunta']}",
                        {"exercise_id": ex.get('exercise_id'), "difficulty": ex.get('nivel')}
                    )
            
            learning_service.update_session_concepts(
                session_id,
                [f"Discusión: {message.message[:50]}..."]
            )

        return StreamingResponse(event_stream(), media_type="text/event-stream")
        
    except Exception as e:
        logger.error(f"Error in learning session chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/session/{session_id}/history", response_model=SessionHistoryResponse)
async def get_session_history(session_id: str):
    """Obtiene el historial completo de una sesión de aprendizaje"""
    try:
        history = learning_service.get_session_full_history(session_id)
        if not history:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        return history
    except Exception as e:
        logger.error(f"Error getting session history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/session/{session_id}/stats", response_model=SessionSummaryStats)
async def get_session_stats(session_id: str):
    """Obtiene estadísticas resumidas de una sesión"""
    try:
        stats = learning_service.get_session_summary_stats(session_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        return stats
    except Exception as e:
        logger.error(f"Error getting session stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learning/session/{session_id}/reactivate")
async def reactivate_session(session_id: str):
    """Reactiva una sesión pausada o completada para continuar el aprendizaje"""
    try:
        success = learning_service.reactivate_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        return {"message": "Sesión reactivada exitosamente", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error reactivating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learning/session/{session_id}/pause")
async def pause_session(session_id: str):
    """Pausa una sesión activa"""
    try:
        learning_service.pause_session(session_id)
        return {"message": "Sesión pausada exitosamente", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error pausing session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/sessions/{user_id}/active")
async def get_active_sessions(user_id: str):
    """Obtiene las sesiones activas o pausadas de un usuario"""
    try:
        sessions = learning_service.get_active_sessions(user_id)
        return {
            "user_id": user_id,
            "active_sessions": sessions,
            "count": len(sessions)
        }
    except Exception as e:
        logger.error(f"Error getting active sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/session/{session_id}/pdf-report")
async def get_session_pdf_report(session_id: str):
    """Genera y descarga el reporte PDF completo de una sesión"""
    try:
        session_data = learning_service.get_session_full_history(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        from services.pdf_service import pdf_service
        pdf_buffer = pdf_service.generate_learning_report(session_data)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_buffer.read())
            tmp_file_path = tmp_file.name
        
        session_info = session_data.get('session_info', {})
        filename = f"reporte_aprendizaje_{session_info.get('topic', 'sesion')}_{session_id[:8]}.pdf"
        
        return FileResponse(
            path=tmp_file_path,
            filename=filename,
            media_type='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/session/{session_id}/pdf-exercises")
async def get_session_exercises_pdf(session_id: str):
    """Genera y descarga un PDF solo con los ejercicios de una sesión"""
    try:
        session_data = learning_service.get_session_full_history(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        from services.pdf_service import pdf_service
        pdf_buffer = pdf_service.generate_exercises_pdf(session_data)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_buffer.read())
            tmp_file_path = tmp_file.name
        
        session_info = session_data.get('session_info', {})
        filename = f"ejercicios_{session_info.get('topic', 'sesion')}_{session_id[:8]}.pdf"
        
        return FileResponse(
            path=tmp_file_path,
            filename=filename,
            media_type='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Error generating exercises PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learning/session/{session_id}/interaction")
async def add_session_interaction(session_id: str, interaction_type: str, content: str, metadata: dict = None):
    """Agrega una interacción manual al historial de la sesión"""
    try:
        learning_service.add_session_interaction(session_id, interaction_type, content, metadata)
        return {"message": "Interacción agregada exitosamente", "session_id": session_id}
    except Exception as e:
        logger.error(f"Error adding session interaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tutor/progress/{user_id}", response_model=ProgressAnalysis)
async def get_user_progress_analysis(user_id: str):
    """Obtiene análisis completo del progreso del usuario"""
    try:
        analysis = learning_service.get_user_progress_analysis(user_id)
        return analysis
    except Exception as e:
        logger.error(f"Error getting progress analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tutor/recommendations/{user_id}", response_model=UserRecommendations)
async def get_personalized_recommendations(user_id: str):
    """Obtiene recomendaciones personalizadas completas para el usuario"""
    try:
        recommendations = learning_service.get_personalized_recommendations(user_id)
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tutor/exercises/adaptive")
async def generate_adaptive_exercises(request: AdaptiveExerciseRequest):
    """Genera ejercicios adaptativos basados en el progreso del usuario"""
    try:
        exercises = learning_service.get_adaptive_exercises_for_user(
            request.user_id, 
            request.topic, 
            request.cantidad
        )
        
        for exercise in exercises:
            learning_service.save_exercise(exercise)
        
        return {
            "user_id": request.user_id,
            "topic": request.topic,
            "exercises": exercises,
            "adaptation_info": "Ejercicios generados basados en tu progreso personal",
            "count": len(exercises)
        }
    except Exception as e:
        logger.error(f"Error generating adaptive exercises: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tutor/exercise/complete")
async def complete_exercise_with_tracking(completion: ExerciseCompletion):
    """Completa un ejercicio con seguimiento de progreso"""
    try:
        exercise_data = learning_service.exercises.find_one({"exercise_id": completion.exercise_id})
        if not exercise_data:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
        
        learning_service.complete_exercise_with_analysis(
            completion.user_id,
            completion.session_id,
            exercise_data,
            completion.user_answer,
            completion.is_correct,
            completion.time_taken
        )
        
        if not completion.is_correct:
            recommendations = ai.generate_personalized_advice(completion.user_id)
            return {
                "message": "Ejercicio completado",
                "result": "incorrecto",
                "advice": recommendations.get("consejo_principal", ""),
                "motivation": recommendations.get("mensaje_motivacional", ""),
                "next_steps": recommendations.get("proximos_pasos", [])
            }
        else:
            return {
                "message": "¡Excelente! Ejercicio completado correctamente",
                "result": "correcto",
                "motivation": "¡Sigue así! Estás progresando muy bien."
            }
            
    except Exception as e:
        logger.error(f"Error completing exercise: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tutor/concept/learn")
async def learn_concept_with_tracking(learning: ConceptLearning):
    """Aprende un concepto con seguimiento de progreso"""
    try:
        learning_service.learn_concept_with_tracking(
            learning.user_id,
            learning.session_id,
            learning.concept,
            learning.explanation
        )
        
        return {
            "message": f"Concepto '{learning.concept}' aprendido y registrado",
            "session_id": learning.session_id,
            "progress_updated": True
        }
    except Exception as e:
        logger.error(f"Error learning concept: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tutor/dashboard/{user_id}")
async def get_student_dashboard(user_id: str):
    """Obtiene un dashboard completo del estudiante para el frontend"""
    try:
        active_sessions = learning_service.get_active_sessions(user_id)
        
        progress = learning_service.get_user_progress_analysis(user_id)
        
        recommendations = learning_service.get_personalized_recommendations(user_id)
        
        all_sessions = learning_service.get_user_sessions(user_id)
        total_time = 0
        total_concepts = 0
        
        for session in all_sessions:
            if session.get('created_at') and session.get('last_accessed'):
                duration = session['last_accessed'] - session['created_at']
                total_time += duration.total_seconds() / 60  # en minutos
            total_concepts += len(session.get('concepts_covered', []))
        
        return {
            "user_id": user_id,
            "active_sessions": active_sessions,
            "progress_summary": {
                "nivel_actual": progress.get("nivel_actual", "principiante"),
                "total_sessions": len(all_sessions),
                "total_study_time_minutes": total_time,
                "total_concepts_learned": total_concepts,
                "accuracy_percentage": progress.get("estadisticas_reales", {}).get("overall_accuracy", 0)
            },
            "quick_recommendations": {
                "next_topic": recommendations.get("next_topic_recommendation", {}).get("tema_recomendado", ""),
                "daily_advice": recommendations.get("personalized_advice", {}).get("consejo_principal", ""),
                "motivation": recommendations.get("personalized_advice", {}).get("mensaje_motivacional", "")
            },
            "areas_to_improve": progress.get("areas_debiles", []),
            "strong_areas": progress.get("areas_fuertes", []),
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting student dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tutor/exercises/{user_id}/next-batch")
async def get_next_exercise_batch(user_id: str, topic: str, count: int = 3):
    """Obtiene el siguiente lote de ejercicios recomendados"""
    try:
        progress = learning_service.get_user_progress_analysis(user_id)
        exercises = learning_service.get_adaptive_exercises_for_user(user_id, topic, count)
        
        return {
            "user_id": user_id,
            "topic": topic,
            "exercises": exercises,
            "difficulty_level": progress.get("dificultad_recomendada", "facil"),
            "personalized_note": f"Estos ejercicios están adaptados a tu nivel actual: {progress.get('nivel_actual', 'principiante')}",
            "tips": progress.get("consejos_mejora", [])[:2]
        }
        
    except Exception as e:
        logger.error(f"Error getting next exercise batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/tutor-demo/{user_id}")
async def demo_tutor_completo(user_id: str):
    """Endpoint de demostración para probar todas las funcionalidades del tutor"""
    try:
        demo_results = {}
        
        session_id = learning_service.create_learning_session(
            user_id=user_id,
            topic="Álgebra básica",
            level="basico"
        )
        demo_results["session_created"] = session_id
        
        learning_service.learn_concept_with_tracking(
            user_id, session_id, 
            "Variables y constantes", 
            "Las variables son símbolos que representan números desconocidos"
        )
        
        exercises = learning_service.get_adaptive_exercises_for_user(user_id, "Álgebra básica", 2)
        demo_results["adaptive_exercises"] = len(exercises)
        
        if exercises:
            learning_service.complete_exercise_with_analysis(
                user_id, session_id, exercises[0], "x = 5", True, 120
            )
        
        progress = learning_service.get_user_progress_analysis(user_id)
        demo_results["progress_analysis"] = {
            "nivel": progress.get("nivel_actual"),
            "consejos": len(progress.get("consejos_mejora", []))
        }
        
        recommendations = learning_service.get_personalized_recommendations(user_id)
        demo_results["recommendations"] = {
            "next_topic": recommendations.get("next_topic_recommendation", {}).get("tema_recomendado"),
            "advice": recommendations.get("personalized_advice", {}).get("consejo_principal")
        }
        
        return {
            "message": "🎓 Demo del Tutor Completo ejecutada exitosamente",
            "user_id": user_id,
            "demo_results": demo_results,
            "next_steps": [
                f"Ver dashboard: GET /tutor/dashboard/{user_id}",
                f"Chatear en sesión: POST /learning/session/{session_id}/chat",
                f"Obtener más ejercicios: GET /tutor/exercises/{user_id}/next-batch?topic=Álgebra básica",
                f"Generar PDF: GET /learning/session/{session_id}/pdf-report"
            ],
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error in tutor demo: {str(e)}")
        return {
            "message": "Error en demo del tutor",
            "error": str(e),
            "status": "error"
        }
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
