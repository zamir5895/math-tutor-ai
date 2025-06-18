from fastapi import FastAPI, HTTPException
from services.ai_service import ai
from services.qdrant_service import qdrant
from services.mongo_service import mongo

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

app = FastAPI()
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
            yield f"data: {json.dumps({'text': chunk_text})}\n\n"
        
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
@app.get("/conversation/{user_id}/{conversation_id}")
async def get_conversation(user_id: str, conversation_id: str):
    conversation = mongo.get_conversation(user_id, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    return conversation

@app.get("/conversations/{user_id}")
async def list_conversations(user_id: str):
    try:
        conversations = mongo.conversations.find(
            {"user_id": user_id},
            {"_id": 0, "conversation_id": 1, "messages": {"$slice": -1}, "updated_at": 1}
        ).sort("updated_at", -1)
        
        result = []
        async for conv in conversations:
            if not conv.get("messages"):
                continue
                
            last_msg = conv["messages"][-1]
            result.append({
                "id": conv["conversation_id"],
                "title": f"Conversación del {conv['updated_at'].strftime('%d/%m/%Y')}",
                "last_message": last_msg["content"],
                "timestamp": conv["updated_at"].isoformat()
            })
            
        return result
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))