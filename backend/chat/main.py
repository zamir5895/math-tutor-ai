from fastapi import FastAPI, HTTPException
from services.ai_service import ai
from services.qdrant_service import qdrant
from services.mongo_service import mongo
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schemas import UserMessage, AIResponse
from datetime import datetime
import uuid
import logging
import json
from bson import ObjectId

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
    
    # Buscar contexto específico de la conversación
    conversation_contexts = qdrant.search_context(user_id, query_embedding, conversation_id, limit=3)
    
    # Buscar contexto general del usuario
    general_contexts = qdrant.search_general_context(user_id, query_embedding, limit=2)
    
    # Combinar contextos
    context_texts = []
    
    # Agregar contexto de la conversación actual
    for hit in conversation_contexts:
        context_texts.append(f"Contexto de conversación: {hit.payload['text']}")
    
    # Agregar contexto general del usuario
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
    """Endpoint para streaming con filtro matemático"""
    conversation_id = message.conversation_id or str(uuid.uuid4())
    
    # Verificar si es la primera pregunta para generar título
    is_first_message = message.conversation_id is None
    
    # Verificar si es tema matemático
    if not ai.is_math_related(message.message):
        # Respuesta rápida para temas no matemáticos
        non_math_response = "Lo siento, soy un tutor especializado en matemáticas y solo puedo ayudarte con temas relacionados a esta materia. ¿Tienes alguna pregunta de matemáticas en la que pueda ayudarte?"
        
        mongo.save_message(message.user_id, conversation_id, "user", message.message)
        mongo.save_message(message.user_id, conversation_id, "assistant", non_math_response)
        
        def non_math_stream():
            yield f"data: {json.dumps({'text': non_math_response, 'conversation_id': conversation_id})}\n\n"
        
        return StreamingResponse(non_math_stream(), media_type="text/event-stream")
    
    # Guardar mensaje del usuario
    mongo.save_message(message.user_id, conversation_id, "user", message.message)
    
    # Generar título si es la primera pregunta
    if is_first_message:
        title = ai.generate_title(message.message)
        mongo.set_conversation_title(message.user_id, conversation_id, title)
    
    # Generar prompt con contexto
    prompt = await generate_context_prompt(message.user_id, message.message, conversation_id)
    
    def event_stream():
        response = ai.model.generate_content(
            prompt,
            stream=True 
        )
        
        full_response = ""
        for chunk in response:
            chunk_text = chunk.text
            full_response += chunk_text
            yield f"data: {json.dumps({'text': chunk_text, 'conversation_id': conversation_id})}\n\n"

        # Guardar respuesta del asistente
        mongo.save_message(message.user_id, conversation_id, "assistant", full_response)
        
        # Guardar contexto específico de la conversación
        interaction_text = f"P: {message.message}\nR: {full_response}"
        qdrant.upsert_context(
            user_id=message.user_id,
            text=interaction_text,
            embedding=ai.get_embedding(interaction_text),
            conversation_id=conversation_id,
            context_type="conversation",
            metadata={"type": "interaction"}
        )
        
        # Guardar contexto general del usuario (solo conceptos importantes)
        if len(full_response) > 100:  # Solo si es una respuesta sustancial
            qdrant.upsert_context(
                user_id=message.user_id,
                text=f"Concepto aprendido: {message.message[:100]}...",
                embedding=ai.get_embedding(message.message),
                context_type="general",
                metadata={"type": "concept"}
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
    
    # Limpiar ObjectId si existe
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
    return {"message": "Bienvenido al servicio de chat Matemix AI. Microservicio especializado en tutorías de matemáticas."}

@app.delete("/conversation/{user_id}/{conversation_id}")
async def delete_conversation(user_id: str, conversation_id: str):
    try:
        # Eliminar conversación de MongoDB
        deleted = mongo.delete_conversation(user_id, conversation_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
        
        # Eliminar contexto de Qdrant
        qdrant.delete_conversation_context(user_id, conversation_id)
        
        logger.info(f"Deleted conversation {conversation_id} for user {user_id}")
        return {"message": "Conversación eliminada correctamente"}
    
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))