from fastapi import FastAPI, HTTPException
from services.ai_service import ai
from services.qdrant_service import qdrant
from services.mongo_service import mongo
from fastapi.middleware.cors import CORSMiddleware

from schemas import UserMessage, AIResponse
from datetime import datetime
import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from schemas import UserMessage
import uuid
import logging
import json

app = FastAPI(
    title="Matemix Chat Service",
    description="Microservicio para gestionar conversaciones de chat con AI",
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

async def generate_context_prompt(user_id: str, message: str) -> str:
    """Genera el prompt con contexto (igual que antes)"""
    query_embedding = ai.get_embedding(message)
    similar_contexts = qdrant.search_context(user_id, query_embedding)
    context_texts = [hit.payload["text"] for hit in similar_contexts]
    
    return f"""
    Eres un tutor AI. Responde en markdown y en tiempo real.
    Contexto relevante:
    {chr(10).join(context_texts)}
    
    Pregunta:
    {message}
    
    Respuesta (streaming):
    """

@app.post("/chat-stream")
async def chat_stream(message: UserMessage):
    """Endpoint para streaming"""
    conversation_id = message.conversation_id or str(uuid.uuid4())
    
    mongo.save_message(message.user_id, conversation_id, "user", message.message)
    
    prompt = await generate_context_prompt(message.user_id, message.message)
    
    def event_stream():
        response = ai.model.generate_content(
            prompt,
            stream=True 
        )
        
        full_response = ""
        for chunk in response:
            chunk_text = chunk.text
            full_response += chunk_text
            yield f"data: {json.dumps({'text': chunk_text,
                                       'conversation_id': conversation_id})}\n\n"

        mongo.save_message(message.user_id, conversation_id, "assistant", full_response)
        
        interaction_text = f"P: {message.message}\nR: {full_response}"
        qdrant.upsert_context(
            user_id=message.user_id,
            text=interaction_text,
            embedding=ai.get_embedding(interaction_text),
            metadata={"type": "interaction"}
        )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )


from bson import ObjectId

@app.get("/conversation/{user_id}/{conversation_id}")
async def get_conversation(user_id: str, conversation_id: str):
    conversation = mongo.get_conversation(user_id, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    # Convierte _id a string si existe
    if "_id" in conversation and isinstance(conversation["_id"], ObjectId):
        conversation["_id"] = str(conversation["_id"])
    logger.info(f"Retrieved conversation for user {user_id} with ID {conversation_id}")
    print(f"Conversation data: {conversation}")
    return conversation

@app.get("/conversations/{user_id}")
async def list_conversations(user_id: str):
    try:
        conversations_cursor = mongo.conversations.find(
            {"user_id": user_id},
            {"_id": 0, "conversation_id": 1, "messages": {"$slice": -1}, "updated_at": 1}
        ).sort("updated_at", -1)
        
        conversations = list(conversations_cursor)
        print(f"Conversations found for user {user_id}: {len(conversations)}")
        result = []
        for conv in conversations:
            if not conv.get("messages"):
                continue
            last_msg = conv["messages"][-1]
            # Usa updated_at si existe, si no usa la fecha del último mensaje, si no None
            updated_at = conv.get("updated_at")
            if not updated_at and "timestamp" in last_msg:
                try:
                    updated_at = last_msg["timestamp"]
                except Exception:
                    updated_at = None
            if not updated_at:
                updated_at_str = "Sin fecha"
            else:
                # Si es string, intenta parsear a datetime
                if isinstance(updated_at, str):
                    try:
                        from dateutil.parser import parse
                        updated_at = parse(updated_at)
                    except Exception:
                        pass
                updated_at_str = updated_at.strftime('%d/%m/%Y') if hasattr(updated_at, "strftime") else str(updated_at)
            result.append({
                "id": conv.get("conversation_id"),
                "title": f"Conversación del {updated_at_str}",
                "last_message": last_msg.get("content", ""),
            })
        print(f"Conversations found: {len(result)}")
        print(f"Conversations data: {result}")
        
        return result
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
async def root():
    return {"message": "Bienvenido al servicio de chat Matemix AI. Usa el endpoint /chat-stream para interactuar."}