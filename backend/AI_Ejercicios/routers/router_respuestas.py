from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
from uuid import UUID
import logging
from db import respuestas_collection, alumnos_collection, temas_collection
from utils.authorization import verify_student_token_and_id
from datetime import datetime, timezone
from bson import ObjectId

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/respuestas",
    tags=["Respuestas"]
)

# Función para convertir ObjectId en cadena
def objectid_to_str(obj: Any) -> Any:
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not serializable")

# Lógica para verificar si la respuesta es correcta
async def verificar_respuesta(pregunta_id: UUID, respuesta_usuario: str) -> bool:
    tema = await temas_collection.find_one({"niveles.preguntas.id": pregunta_id})
    if not tema:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    
    for nivel in tema["niveles"]:
        for pregunta in nivel["preguntas"]:
            if pregunta["id"] == pregunta_id:
                return pregunta["respuesta_correcta"] == respuesta_usuario
    return False

# Función para serializar los ObjectId a cadenas
def serialize_objectid(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
    return data

@router.post("/guardar_respuesta", response_model=Dict[str, Any])
async def guardar_respuesta(
    alumno_id: str = Body(...),  # alumno_id como string
    tema_id: str = Body(...),    # tema_id como string
    pregunta_id: str = Body(...),  # pregunta_id como string
    respuesta: str = Body(...),  # Respuesta del alumno
    token: str = Body(...)  # Token de autorización
):
    try:
        # Convertir los UUIDs desde strings a objetos UUID dentro del router
        alumno_id_uuid = UUID(alumno_id)
        tema_id_uuid = UUID(tema_id)
        pregunta_id_uuid = UUID(pregunta_id)

        # Verificar si el alumno tiene permisos para guardar respuestas
        owner = await verify_student_token_and_id(token, alumno_id)
        if not owner:
            raise HTTPException(status_code=403, detail="No autorizado para guardar respuestas")
        
        # Verificar existencia del alumno
        alumno = await alumnos_collection.find_one({"_id": alumno_id_uuid})
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        # Verificar si ya existe una respuesta para esta pregunta del alumno
        existing_response = await respuestas_collection.find_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if existing_response:
            raise HTTPException(status_code=400, detail="Ya has respondido esta pregunta.")

        # Verificar si la respuesta es correcta
        respuesta_correcta = await verificar_respuesta(pregunta_id_uuid, respuesta)
        
        # Crear el registro de la respuesta
        respuesta_data = {
            "alumno_id": alumno_id_uuid,
            "tema_id": tema_id_uuid,
            "pregunta_id": pregunta_id_uuid,
            "respuesta": respuesta,
            "respuesta_correcta": respuesta_correcta,
            "fecha_respuesta": str(datetime.now(timezone.utc))
        }
        
        # Insertar la respuesta en la colección de respuestas
        result = await respuestas_collection.insert_one(respuesta_data)
        
        # Convertir el _id de MongoDB a str para evitar problemas de serialización
        respuesta_data["id"] = str(result.inserted_id)
        
        # Convertir todos los UUIDs a str para evitar problemas de serialización
        respuesta_data["alumno_id"] = str(respuesta_data["alumno_id"])
        respuesta_data["tema_id"] = str(respuesta_data["tema_id"])
        respuesta_data["pregunta_id"] = str(respuesta_data["pregunta_id"])
        
        # Serializar ObjectId a string si está presente
        respuesta_data = serialize_objectid(respuesta_data)
        
        return respuesta_data

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error en guardar_respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# **GET**: Obtener una respuesta específica de un alumno
@router.get("/respuesta", response_model=Dict[str, Any])
async def obtener_respuesta(
    alumno_id: str = Body(...),
    pregunta_id: str = Body(...),
    token: str = Body(...)
):
    try:
        # Convertir los UUIDs desde strings a objetos UUID dentro del router
        alumno_id_uuid = UUID(alumno_id)
        pregunta_id_uuid = UUID(pregunta_id)

        # Verificar si el alumno tiene permisos para acceder a la respuesta
        owner = await verify_student_token_and_id(token, alumno_id)
        if not owner:
            raise HTTPException(status_code=403, detail="No autorizado para ver esta respuesta")

        # Buscar la respuesta en la colección
        respuesta = await respuestas_collection.find_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if not respuesta:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")

        # Convertir ObjectId a string
        respuesta = serialize_objectid(respuesta)
        respuesta["id"] = respuesta.pop("_id")  # Convertir el _id a id

        return respuesta
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error en obtener_respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# **PUT**: Actualizar una respuesta existente
@router.put("/actualizar_respuesta", response_model=Dict[str, Any])
async def actualizar_respuesta(
    alumno_id: str = Body(...),  # alumno_id como string
    pregunta_id: str = Body(...),  # pregunta_id como string
    nueva_respuesta: str = Body(...),  # Nueva respuesta del alumno
    token: str = Body(...)  # Token de autorización
):
    try:
        # Convertir los UUIDs desde strings a objetos UUID dentro del router
        alumno_id_uuid = UUID(alumno_id)
        pregunta_id_uuid = UUID(pregunta_id)

        # Verificar si el alumno tiene permisos para actualizar la respuesta
        owner = await verify_student_token_and_id(token, alumno_id)
        if not owner:
            raise HTTPException(status_code=403, detail="No autorizado para actualizar esta respuesta")
        
        # Buscar la respuesta existente
        respuesta_existente = await respuestas_collection.find_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if not respuesta_existente:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")

        # Verificar si la respuesta es correcta
        respuesta_correcta = await verificar_respuesta(pregunta_id_uuid, nueva_respuesta)

        # Actualizar la respuesta
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

        # Convertir UUIDs a str para evitar problemas de serialización
        updated_data["alumno_id"] = str(alumno_id_uuid)
        updated_data["pregunta_id"] = str(pregunta_id_uuid)

        # Serializar ObjectId a string
        updated_data = serialize_objectid(updated_data)

        return updated_data

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error en actualizar_respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# **DELETE**: Eliminar una respuesta existente
@router.delete("/eliminar_respuesta", response_model=Dict[str, Any])
async def eliminar_respuesta(
    alumno_id: str = Body(...),  # alumno_id como string
    pregunta_id: str = Body(...),  # pregunta_id como string
    token: str = Body(...)  # Token de autorización
):
    try:
        # Convertir los UUIDs desde strings a objetos UUID dentro del router
        alumno_id_uuid = UUID(alumno_id)
        pregunta_id_uuid = UUID(pregunta_id)

        # Verificar si el alumno tiene permisos para eliminar la respuesta
        owner = await verify_student_token_and_id(token, alumno_id)
        if not owner:
            raise HTTPException(status_code=403, detail="No autorizado para eliminar esta respuesta")
        
        # Buscar la respuesta existente
        respuesta_existente = await respuestas_collection.find_one({
            "alumno_id": alumno_id_uuid,
            "pregunta_id": pregunta_id_uuid
        })

        if not respuesta_existente:
            raise HTTPException(status_code=404, detail="Respuesta no encontrada")

        # Eliminar la respuesta
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
