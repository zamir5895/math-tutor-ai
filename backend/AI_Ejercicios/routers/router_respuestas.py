from fastapi import APIRouter, HTTPException, Body, Query
from typing import Dict, Any, List
from uuid import UUID
import logging
from db import respuestas_collection, alumnos_collection, temas_collection
from utils.authorization import verify_student_token_and_id
from datetime import datetime, timezone
from bson import ObjectId
from uuid import UUID as UUIDType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/respuestas",
    tags=["Respuestas"]
)

def objectid_to_str(obj: Any) -> Any:
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not serializable")

async def verificar_respuesta(pregunta_id: UUID, respuesta_usuario: str) -> bool:
    tema = await temas_collection.find_one({"niveles.preguntas.id": pregunta_id})
    if not tema:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    
    for nivel in tema["niveles"]:
        for pregunta in nivel["preguntas"]:
            if pregunta["id"] == pregunta_id:
                return pregunta["respuesta_correcta"] == respuesta_usuario
    return False

def serialize_objectid(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
    return data

@router.post("/guardar_respuesta", response_model=Dict[str, Any])
async def guardar_respuesta(
    alumno_id: str = Body(...),  
    tema_id: str = Body(...),   
    pregunta_id: str = Body(...),  
    respuesta: str = Body(...),  
    token: str = Body(...)  
):
    try:
        alumno_id_uuid = UUID(alumno_id)
        tema_id_uuid = UUID(tema_id)
        pregunta_id_uuid = UUID(pregunta_id)

        owner = await verify_student_token_and_id(token, alumno_id)
        if not owner:
            raise HTTPException(status_code=403, detail="No autorizado para guardar respuestas")
        
        alumno = await alumnos_collection.find_one({"_id": alumno_id_uuid})
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        existing_response = await respuestas_collection.find_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if existing_response:
            raise HTTPException(status_code=400, detail="Ya has respondido esta pregunta.")

        respuesta_correcta = await verificar_respuesta(pregunta_id_uuid, respuesta)
        
        respuesta_data = {
            "alumno_id": alumno_id_uuid,
            "tema_id": tema_id_uuid,
            "pregunta_id": pregunta_id_uuid,
            "respuesta": respuesta,
            "respuesta_correcta": respuesta_correcta,
            "fecha_respuesta": str(datetime.now(timezone.utc))
        }
        
        result = await respuestas_collection.insert_one(respuesta_data)
        
        respuesta_data["id"] = str(result.inserted_id)
        
        respuesta_data["alumno_id"] = str(respuesta_data["alumno_id"])
        respuesta_data["tema_id"] = str(respuesta_data["tema_id"])
        respuesta_data["pregunta_id"] = str(respuesta_data["pregunta_id"])
        
        respuesta_data = serialize_objectid(respuesta_data)
        
        return respuesta_data

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error en guardar_respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/respuesta", response_model=Dict[str, Any])
async def obtener_respuesta(
    alumno_id: str = Body(...),
    pregunta_id: str = Body(...),
    token: str = Body(...)
):
    try:
        alumno_id_uuid = UUID(alumno_id)
        pregunta_id_uuid = UUID(pregunta_id)

        owner = await verify_student_token_and_id(token, alumno_id)
        if not owner:
            raise HTTPException(status_code=403, detail="No autorizado para ver esta respuesta")

        respuesta = await respuestas_collection.find_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if not respuesta:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")

        respuesta = serialize_objectid(respuesta)
        respuesta["id"] = respuesta.pop("_id") 

        return respuesta
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error en obtener_respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/actualizar_respuesta", response_model=Dict[str, Any])
async def actualizar_respuesta(
    alumno_id: str = Body(...),  
    pregunta_id: str = Body(...),  
    nueva_respuesta: str = Body(...), 
    token: str = Body(...)  
):
    try:
        alumno_id_uuid = UUID(alumno_id)
        pregunta_id_uuid = UUID(pregunta_id)

        owner = await verify_student_token_and_id(token, alumno_id)
        if not owner:
            raise HTTPException(status_code=403, detail="No autorizado para actualizar esta respuesta")
        
        respuesta_existente = await respuestas_collection.find_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if not respuesta_existente:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")

        respuesta_correcta = await verificar_respuesta(pregunta_id_uuid, nueva_respuesta)

        updated_data = {
            "respuesta": nueva_respuesta,
            "respuesta_correcta": respuesta_correcta,
            "fecha_respuesta": str(datetime.now(timezone.utc))
        }

        result = await respuestas_collection.update_one(
            {"_id": respuesta_existente["_id"]},
            {"$set": updated_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la respuesta")

        updated_data["id"] = str(respuesta_existente["_id"])

        updated_data["alumno_id"] = str(alumno_id_uuid)
        updated_data["pregunta_id"] = str(pregunta_id_uuid)

        updated_data = serialize_objectid(updated_data)

        return updated_data

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error en actualizar_respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.delete("/eliminar_respuesta", response_model=Dict[str, Any])
async def eliminar_respuesta(
    alumno_id: str = Body(...), 
    pregunta_id: str = Body(...),  
    token: str = Body(...) 
):
    try:
        alumno_id_uuid = UUID(alumno_id)
        pregunta_id_uuid = UUID(pregunta_id)

        owner = await verify_student_token_and_id(token, alumno_id)
        if not owner:
            raise HTTPException(status_code=403, detail="No autorizado para eliminar esta respuesta")
        
        respuesta_existente = await respuestas_collection.find_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if not respuesta_existente:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")

        result = await respuestas_collection.delete_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if result.deleted_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo eliminar la respuesta")

        return {"message": "Respuesta eliminada exitosamente"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error en eliminar_respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

@router.get("/respuestas_correctas", response_model=List[Dict[str, Any]])
async def obtener_respuestas_correctas(
        tema_id: UUID = Query(..., description="ID del tema para filtrar las respuestas"),
        nivel: str = Query(None, description="Nivel para filtrar las respuestas (facil, medio, dificil)")
    ):
        try:
            tema = await temas_collection.find_one({"_id": tema_id})
            if not tema:
                raise HTTPException(status_code=404, detail="Tema no encontrado")

            if nivel:
                if nivel not in ["facil", "medio", "dificil"]:
                    raise HTTPException(status_code=400, detail="Nivel inválido, debe ser 'facil', 'medio' o 'dificil'")
                niveles = [niv for niv in tema["niveles"] if niv["nivel"] == nivel]
            else:
                niveles = tema["niveles"]  # Si no se especifica un nivel, tomamos todos
            pregunta_ids = [pregunta["id"] for nivel in niveles for pregunta in nivel["preguntas"]]

            respuestas_correctas = await respuestas_collection.find({
                "pregunta_id": {"$in": pregunta_ids},
                "respuesta_correcta": True  
            }).to_list(length=None)

            if not respuestas_correctas:
                raise HTTPException(status_code=404, detail="No se encontraron respuestas correctas para este tema o nivel")

            def serialize_item(item):
                item = {k: (str(v) if isinstance(v, (ObjectId, UUIDType)) else v) for k, v in item.items()}
                if "_id" in item:
                    item["id"] = item.pop("_id")
                return item

            return [serialize_item(resp) for resp in respuestas_correctas]

        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener las respuestas correctas: {str(e)}")
