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
    ExerciseCompletion, SessionExercisesResponse, ConversationExercisesResponse
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
    """Chat general de matemáticas para consultas, explicaciones y orientación - SIN generación de ejercicios ni lógica de sesiones"""
    conversation_id = message.conversation_id or str(uuid.uuid4())
    is_first_message = message.conversation_id is None
    
    if not ai.is_math_related(message.message):
        non_math_response = """Lo siento, soy un tutor especializado en matemáticas y solo puedo ayudarte con temas relacionados a esta materia. 

¿Te gustaría que te ayude con alguno de estos temas?
- Álgebra básica
- Geometría 
- Fracciones
- Ecuaciones
- O cualquier otro tema de matemáticas"""
        
        mongo.save_message(message.user_id, conversation_id, "user", message.message)
        mongo.save_message(message.user_id, conversation_id, "assistant", non_math_response)
        
        def non_math_stream():
            yield f"data: {json.dumps({'text': non_math_response, 'conversation_id': conversation_id})}\n\n"
        
        return StreamingResponse(non_math_stream(), media_type="text/event-stream")
    
    mongo.save_message(message.user_id, conversation_id, "user", message.message)
    
    if is_first_message:
        title = ai.generate_title(message.message)
        mongo.set_conversation_title(message.user_id, conversation_id, title)
    
    context_prompt = await generate_context_prompt(message.user_id, message.message, conversation_id)
    
    def event_stream():
        response = ai.model.generate_content(context_prompt, stream=True)
        
        full_response = ""
        for chunk in response:
            chunk_text = chunk.text
            full_response += chunk_text
            yield f"data: {json.dumps({'text': chunk_text, 'conversation_id': conversation_id})}\n\n"

        mongo.save_message(message.user_id, conversation_id, "assistant", full_response)
        
        interaction_text = f"P: {message.message}\nR: {full_response}"
        qdrant.upsert_context(
            user_id=message.user_id,
            text=interaction_text,
            embedding=ai.get_embedding(interaction_text),
            conversation_id=conversation_id,
            context_type="conversation",
            metadata={
                "type": "general_math_chat",
                "topic": "conversacion_general"
            }
        )

    return StreamingResponse(event_stream(), media_type="text/event-stream")

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
            "   Chat general para consultas y orientación matemática",
            "   Sesiones de aprendizaje especializadas con chat propio", 
            "   Generación de ejercicios SOLO en sesiones: 10 por set (3 fáciles, 4 intermedios, 3 difíciles)",
            "   Análisis completo de progreso y debilidades",
            "   Recomendaciones personalizadas con IA",
            "   Seguimiento continuo en Qdrant Vector DB",
            "   Dashboard completo para estudiantes",
            "   Separación clara: chat general vs chat de sesión",
            "   Reportes PDF detallados de aprendizaje",
            "⚡ API bien estructurada con responsabilidades claras"
        ],
        "api_sections": {
            " Tutor IA Completo": {
                "dashboard": "/tutor/dashboard/{user_id}",
                "analisis_progreso": "/tutor/progress/{user_id}",
                "recomendaciones": "/tutor/recommendations/{user_id}",
                "ejercicios_adaptativos": "/tutor/exercises/adaptive",
                "siguiente_lote": "/tutor/exercises/{user_id}/next-batch",
                "completar_ejercicio": "/tutor/exercise/complete"
            },
            " Sesiones de Aprendizaje": {
                "crear_sesion": "/learning/session/create",
                "chat_en_sesion": "/learning/session/{session_id}/chat",
                "historial_completo": "/learning/session/{session_id}/history",
                "estadisticas": "/learning/session/{session_id}/stats",
                "reactivar": "/learning/session/{session_id}/reactivate",
                "sesiones_activas": "/learning/sessions/{user_id}/active"
            },
            " Reportes y Análisis": {
                "reporte_pdf": "/learning/session/{session_id}/pdf-report",
                "ejercicios_pdf": "/learning/session/{session_id}/pdf-exercises",
                "conversaciones": "/conversations/{user_id}"
            },
            " Chat General": {
                "chat_consultas": "/chat-stream (solo consultas y orientación)",
                "eliminar_conversacion": "/conversation/{user_id}/{conversation_id}"
            },
            " Chat de Sesiones": {
                "chat_con_ejercicios": "/learning/session/{session_id}/chat (genera ejercicios)",
                "obtener_ejercicios": "/learning/session/{session_id}/exercises"
            }
        },
        "frontend_integration": {
            "flujo_completo": [
                "1.  Obtener dashboard: GET /tutor/dashboard/{user_id}",
                "2.  Ver recomendaciones: GET /tutor/recommendations/{user_id}",
                "3.  Crear/reactivar sesión según recomendación",
                "4.  Chatear en la sesión libremente", 
                "5.  Solicitar ejercicios adaptativos",
                "6.  Completar ejercicios con tracking automático",
                "7.  Ver progreso actualizado en tiempo real",
                "8.  Generar reportes PDF cuando se desee"
            ],
            "llamadas_principales": {
                "obtener_ejercicios": "POST /tutor/exercises/adaptive",
                "completar_ejercicio": "POST /tutor/exercise/complete", 
                "dashboard_estudiante": "GET /tutor/dashboard/{user_id}",
                "chat_inteligente": "POST /chat-stream"
            }
        },
        "ai_capabilities": [
            " Detección automática de intenciones en el chat de sesiones",
            " Extracción automática de conceptos matemáticos de las conversaciones",
            " Análisis de patrones de aprendizaje individualizados",
            " Generación inteligente de sets de 10 ejercicios (3-4-3 por dificultad)",
            " Consejos adaptativos basados en errores y progreso",
            " Seguimiento automático de progreso en vector database",
            " Recomendaciones de temas siguientes personalizadas",
            " Registro inteligente de conceptos aprendidos sin intervención manual",
            " Motivación y retroalimentación personalizada"
        ],
        "documentation": "/docs", 
        "ejemplo_uso_simplificado": {
            "descripcion": "Responsabilidades separadas: Chat general vs Sesiones",
            "chat_general": "POST /chat-stream con 'explícame álgebra' → Solo explica conceptos y orienta",
            "crear_sesion": "POST /learning/session/create → Crear sesión para generar ejercicios",
            "chat_sesion": "POST /learning/session/{id}/chat con 'quiero ejercicios' → Genera 10 ejercicios",
            "obtener_ejercicios": "GET /learning/session/{id}/exercises → Ver ejercicios generados"
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
    """Crea una nueva sesión de aprendizaje estructurada"""
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

        return {
            "session_id": session_id,
            "topic": request.topic,
            "subtopic": request.subtopic,
            "level": request.level,
            "teaching_plan": teaching_plan,
            "status": "active",
            "message": f"Sesión de aprendizaje creada para {request.topic}. Comenzaremos con {len(teaching_plan)} conceptos.",
            "chat_endpoint": f"/learning/session/{session_id}/chat"
        }

    except Exception as e:
        logger.error(f"Error creating learning session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
            "status": "completed",
            "next_steps": "Puedes generar ejercicios o un reporte de tu aprendizaje"
        }
    except Exception as e:
        logger.error(f"Error completing session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learning/session/{session_id}/pause")
async def pause_session(session_id: str):
    """Pausa una sesión activa"""
    try:
        learning_service.pause_session(session_id)
        return {
            "message": "Sesión pausada exitosamente", 
            "session_id": session_id,
            "status": "paused"
        }
    except Exception as e:
        logger.error(f"Error pausing session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learning/session/{session_id}/reactivate")
async def reactivate_session(session_id: str):
    """Reactiva una sesión pausada o completada"""
    try:
        success = learning_service.reactivate_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        return {
            "message": "Sesión reactivada exitosamente", 
            "session_id": session_id,
            "status": "active"
        }
    except Exception as e:
        logger.error(f"Error reactivating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))





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
    """Chat interactivo dentro de una sesión de aprendizaje con generación inteligente de ejercicios"""
    try:
        session = learning_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        if session["user_id"] != message.user_id:
            raise HTTPException(status_code=403, detail="Acceso denegado a esta sesión")
        
        conversation_id = f"learning_{session_id}"
        
        # SIEMPRE guardar el mensaje del usuario
        mongo.save_message(message.user_id, conversation_id, "user", message.message)
        
        intent = ai.analyze_student_intent(message.message)
        
        def event_stream():
            exercises_generated = []
            
            if intent.get("intent") == "pedir_ejercicios":
                # Generar ejercicios inteligentemente basados en la sesión
                topic = session["topic"]
                subtopic = session.get("subtopic")
                level = session.get("level", "basico")
                
                # Mapear nivel de sesión a dificultades
                difficulty_map = {"basico": "facil", "intermedio": "intermedio", "avanzado": "dificil"}
                
                # Generar 10 ejercicios: 3 fáciles, 4 intermedios, 3 difíciles
                all_exercises = []
                
                # 3 ejercicios fáciles
                easy_exercises = ai.generate_exercises(
                    topic=topic,
                    subtopic=subtopic,
                    nivel="facil",
                    cantidad=3
                )
                all_exercises.extend(easy_exercises)
                
                # 4 ejercicios intermedios
                medium_exercises = ai.generate_exercises(
                    topic=topic,
                    subtopic=subtopic,
                    nivel="intermedio",
                    cantidad=4
                )
                all_exercises.extend(medium_exercises)
                
                # 3 ejercicios difíciles
                hard_exercises = ai.generate_exercises(
                    topic=topic,
                    subtopic=subtopic,
                    nivel="dificil",
                    cantidad=3
                )
                all_exercises.extend(hard_exercises)
                
                # Guardar todos los ejercicios en la base de datos con metadatos de la sesión
                for ex in all_exercises:
                    ex["session_id"] = session_id
                    ex["conversation_id"] = conversation_id
                    ex["generated_at"] = datetime.utcnow()
                    exercise_id = learning_service.save_exercise(ex)
                    ex["exercise_id"] = exercise_id
                    exercises_generated.append(ex)
                
                # Respuesta del chat SIN mostrar los ejercicios
                response_text = f"""¡Perfecto! He generado un set completo de ejercicios de **{topic}** para ti.

**Detalles del set generado:**
- Tema: {topic}
- Subtema: {subtopic if subtopic else "General"}
- **Total: 10 ejercicios**
  - 🟢 3 ejercicios fáciles
  - 🟡 4 ejercicios intermedios  
  - 🔴 3 ejercicios difíciles

Los ejercicios están listos y organizados por dificultad. Puedes verlos usando el endpoint `/learning/session/{session_id}/exercises` y empezar con los que prefieras.

¿Te gustaría que te explique algún concepto antes de empezar, o prefieres ir directo a practicar?"""
                
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
                    response_text = "¡Excelente! Has completado todos los conceptos de esta sesión. ¿Te gustaría que genere algunos ejercicios de práctica o prefieres generar un reporte de tu aprendizaje?"
            
            elif intent.get("intent") == "aprender_mas" or intent.get("intent") == "ampliar_conocimiento":
                # El usuario quiere aprender más sobre el tema actual o explorar subtemas
                topic = session["topic"]
                current_subtopic = session.get("subtopic")
                
                # Generar temas relacionados y conceptos avanzados
                related_topics = ai.get_related_topics(topic, current_subtopic)
                advanced_concepts = ai.get_advanced_concepts(topic, current_subtopic)
                
                response_text = f"""¡Perfecto! Te ayudo a expandir tus conocimientos en **{topic}**.

**Conceptos avanzados que puedes explorar:**
{chr(10).join([f"• {concept}" for concept in advanced_concepts[:4]])}

**Temas relacionados interesantes:**
{chr(10).join([f"• {related}" for related in related_topics[:4]])}

**¿Qué te gustaría hacer?**
1. 📚 Aprender un concepto avanzado específico
2. 🎯 Generar ejercicios del tema actual pero más difíciles  
3. 🔄 Explorar un tema relacionado
4. 📈 Ver mi progreso y recomendaciones personalizadas

Solo dime qué prefieres y profundizaremos en ello."""
                
                # Actualizar conceptos de la sesión con temas explorados
                learning_service.update_session_concepts(
                    session_id,
                    [f"Exploración: Temas relacionados con {topic}"]
                )
            
            else:
                response_text = ai.generate_contextual_response(message.message, session)
            
            mongo.save_message(message.user_id, conversation_id, "assistant", response_text)
            
            yield f"data: {json.dumps({'text': response_text, 'session_id': session_id, 'topic': session['topic'], 'exercises_generated': len(exercises_generated)})}\n\n"
            
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
                {"response_type": intent.get("intent", "general"), "exercises_count": len(exercises_generated)}
            )
            
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
                    "topic": session["topic"],
                    "exercises_generated": len(exercises_generated)
                }
            )
            
            if exercises_generated:
                for ex in exercises_generated:
                    learning_service.add_session_interaction(
                        session_id,
                        "exercise_generated",
                        f"Ejercicio generado: {ex['pregunta'][:100]}...",
                        {
                            "exercise_id": ex.get('exercise_id'), 
                            "difficulty": ex.get('nivel'),
                            "topic": ex.get('tema'),
                            "subtopic": ex.get('subtema')
                        }
                    )
            
            # Registro automático e inteligente de conceptos aprendidos
            if len(message.message) > 10:  # Solo si es una pregunta sustancial
                # Extraer conceptos clave de la pregunta usando IA
                key_concepts = ai.extract_math_concepts(message.message, session["topic"])
                
                if key_concepts:
                    # Registrar conceptos específicos identificados
                    learning_service.update_session_concepts(
                        session_id,
                        [f"Concepto aprendido: {concept}" for concept in key_concepts]
                    )
                else:
                    # Fallback: registrar como discusión general
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
    """Endpoint de demostración del flujo simplificado con chat inteligente"""
    try:
        demo_results = {}
        
        # 1. Crear sesión de aprendizaje
        session_id = learning_service.create_learning_session(
            user_id=user_id,
            topic="Álgebra básica",
            level="basico"
        )
        demo_results["session_created"] = session_id
        
        # 2. Simular flujo correcto: Chat general NO genera ejercicios
        demo_results["chat_general_simulation"] = {
            "user_message": "Quiero ejercicios de álgebra básica", 
            "chat_response": "Te oriento a crear una sesión de aprendizaje",
            "no_exercises_generated": "El chat general solo orienta, no genera ejercicios"
        }
        
        # 3. Simular chat de sesión que SÍ genera ejercicios
        demo_results["session_chat_simulation"] = {
            "endpoint": f"/learning/session/{session_id}/chat",
            "user_message": "Quiero ejercicios de álgebra básica",
            "detected_intent": "pedir_ejercicios", 
            "auto_generated": "10 ejercicios (3 fáciles, 4 intermedios, 3 difíciles)",
            "storage": "automático en la base de datos vinculado a la sesión"
        }
        
        # 4. Simular generación de ejercicios EN LA SESIÓN (no en chat general)
        topic = "Álgebra básica"
        all_exercises = []
        
        # Generar el set completo
        easy_exercises = ai.generate_exercises(topic, nivel="facil", cantidad=3)
        medium_exercises = ai.generate_exercises(topic, nivel="intermedio", cantidad=4) 
        hard_exercises = ai.generate_exercises(topic, nivel="dificil", cantidad=3)
        
        all_exercises.extend(easy_exercises)
        all_exercises.extend(medium_exercises)
        all_exercises.extend(hard_exercises)
        
        # Guardar ejercicios
        exercise_ids = []
        for ex in all_exercises:
            ex["session_id"] = session_id
            ex["generated_via"] = "demo_auto_detection"
            ex["generated_at"] = datetime.utcnow()
            exercise_id = learning_service.save_exercise(ex)
            exercise_ids.append(exercise_id)
        
        demo_results["exercises_generated"] = {
            "total": len(all_exercises),
            "faciles": len(easy_exercises),
            "intermedios": len(medium_exercises), 
            "dificiles": len(hard_exercises),
            "exercise_ids": exercise_ids[:3]  # Solo mostrar algunos IDs
        }
        
        # 4. Obtener análisis de progreso
        progress = learning_service.get_user_progress_analysis(user_id)
        demo_results["progress_analysis"] = {
            "nivel": progress.get("nivel_actual"),
            "areas_fuertes": len(progress.get("areas_fuertes", [])),
            "areas_debiles": len(progress.get("areas_debiles", []))
        }
        
        # 5. Obtener recomendaciones
        recommendations = learning_service.get_personalized_recommendations(user_id)
        demo_results["recommendations"] = {
            "next_topic": recommendations.get("next_topic_recommendation", {}).get("tema_recomendado"),
            "advice": recommendations.get("personalized_advice", {}).get("consejo_principal")
        }
        
        return {
            "message": "🎓 Demo del Flujo Correcto: Separación Chat General vs Sesiones",
            "user_id": user_id,
            "demo_results": demo_results,
            "flujo_correcto": {
                "1_chat_general": f"POST /chat-stream → 'Quiero ejercicios' → Solo orienta, NO genera ejercicios",
                "2_crear_sesion": f"POST /learning/session/create → Crear sesión para ejercicios",
                "3_chat_sesion": f"POST /learning/session/{session_id}/chat → 'Quiero ejercicios' → SÍ genera 10 ejercicios",
                "4_ver_ejercicios": f"GET /learning/session/{session_id}/exercises → Ver ejercicios generados",
                "5_dashboard": f"GET /tutor/dashboard/{user_id} → Ver progreso actualizado"
            },
            "responsabilidades": {
                "chat_general": "Consultas, explicaciones, orientación (NO ejercicios)",
                "chat_sesion": "Aprendizaje estructurado + generación de ejercicios", 
                "separacion_clara": "Cada endpoint tiene su propósito específico"
            },
            "ventajas": [
                "✅ Responsabilidades claras y separadas",
                "✅ Chat general para consultas rápidas",
                "✅ Sesiones para aprendizaje estructurado con ejercicios", 
                "✅ Mejor organización del código",
                "✅ Más fácil de mantener y escalar"
            ],
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error in simplified tutor demo: {str(e)}")
        return {
            "message": "Error en demo del flujo simplificado",
            "error": str(e),
            "status": "error"
        }
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/learning/session/{session_id}/exercises", response_model=SessionExercisesResponse)
async def get_session_exercises(session_id: str):
    """Obtiene todos los ejercicios generados en una sesión específica"""
    try:
        session = learning_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        
        # Buscar ejercicios generados en esta sesión
        exercises = learning_service.get_exercises_by_session(session_id)
        
        return {
            "session_id": session_id,
            "topic": session["topic"],
            "subtopic": session.get("subtopic"),
            "level": session.get("level"),
            "exercises": exercises,
            "count": len(exercises),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting session exercises: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning/conversation/{conversation_id}/exercises", response_model=ConversationExercisesResponse)
async def get_conversation_exercises(conversation_id: str):
    """Obtiene todos los ejercicios generados en una conversación específica - DEPRECATED: El chat general ya no genera ejercicios"""
    try:
        # Buscar ejercicios generados en esta conversación
        exercises = learning_service.get_exercises_by_conversation(conversation_id)
        
        # Mensaje informativo sobre el cambio de arquitectura
        if not exercises:
            return {
                "conversation_id": conversation_id,
                "exercises": [],
                "count": 0,
                "generated_at": datetime.utcnow().isoformat(),
                "notice": "El chat general ya no genera ejercicios. Usa sesiones de aprendizaje para generar ejercicios."
            }
        
        return {
            "conversation_id": conversation_id,
            "exercises": exercises,
            "count": len(exercises),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting conversation exercises: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
