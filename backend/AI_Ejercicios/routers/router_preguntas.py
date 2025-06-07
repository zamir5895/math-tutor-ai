from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json
import os
from motor.motor_asyncio import AsyncIOMotorClient
import httpx  # Para realizar las solicitudes HTTP al endpoint de verificación del token
import logging
from uuid import UUID, uuid4  # Usamos UUID en lugar de ObjectId

# Modelos
from alumno import Alumno
from tema import NivelEnum, Tema, TemaCreate, TemaUpdate, Pregunta, PreguntaCreate, PreguntaUpdate, Nivel
from progreso import Progreso, ProgresoCreate, RespuestaAlumno
from reporte import Reporte, ReporteCreate
from service import GPTService
from solucionarioService import SolucionarioService
from db import alumnos_collection, temas_collection, progresos_collection, reportes_collection
from request import LoginAlumnoRequest

router = APIRouter(
    prefix="",
    tags=["Preguntas"]
)

# Helper para serializar UUIDs
def serialize_uuids_for_json(document):
    """Convierte UUIDs a strings para serialización JSON"""
    if isinstance(document, dict):
        result = {}
        for key, value in document.items():
            if isinstance(value, UUID):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = serialize_uuids_for_json(value)
            elif isinstance(value, list):
                result[key] = [serialize_uuids_for_json(item) if isinstance(item, dict) else str(item) if isinstance(item, UUID) else item for item in value]
            else:
                result[key] = value
        return result
    return document

# 1. AGREGAR PREGUNTA A UN TEMA
@router.post("/temas/{tema_id}/niveles/{nivel}/preguntas", response_model=Dict[str, Any])
async def agregar_pregunta(
    tema_id: str,
    nivel: NivelEnum,
    pregunta_data: PreguntaCreate
):
    """Agrega una nueva pregunta a un nivel específico de un tema"""
    try:
        # ✅ SIMPLIFICADO: Solo validar y convertir a UUID
        tema_uuid = UUID(tema_id)
        
        # Crear la nueva pregunta con ID único
        nueva_pregunta = Pregunta(
            id=uuid4(),
            **pregunta_data.dict()
        )
        
        # Buscar el tema
        tema = await temas_collection.find_one({"_id": tema_uuid})
        if not tema:
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        
        # Actualizar usando MongoDB $push con filtro de array
        resultado = await temas_collection.update_one(
            {
                "_id": tema_uuid,
                "niveles.nivel": nivel.value
            },
            {
                "$push": {
                    "niveles.$.preguntas": nueva_pregunta.dict()
                }
            }
        )
        
        if resultado.matched_count == 0:
            # Si no se encontró el nivel, crearlo
            nuevo_nivel = Nivel(nivel=nivel, preguntas=[nueva_pregunta])
            resultado_nivel = await temas_collection.update_one(
                {"_id": tema_uuid},
                {"$push": {"niveles": nuevo_nivel.dict()}}
            )
            
            if resultado_nivel.modified_count == 0:
                raise HTTPException(status_code=500, detail="No se pudo agregar el nivel")
        
        return {
            "mensaje": "Pregunta agregada exitosamente",
            "pregunta_id": str(nueva_pregunta.id),
            "tema_id": tema_id,
            "nivel": nivel.value
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de tema inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# 2. ELIMINAR PREGUNTA DE UN TEMA
@router.delete("/temas/{tema_id}/niveles/{nivel}/preguntas/{pregunta_id}")
async def eliminar_pregunta(
    tema_id: str,
    nivel: NivelEnum,
    pregunta_id: str
):
    """Elimina una pregunta específica de un nivel de un tema"""
    try:
        # ✅ SIMPLIFICADO: Solo convertir a UUID
        tema_uuid = UUID(tema_id)
        pregunta_uuid = UUID(pregunta_id)
        
        # Eliminar la pregunta usando $pull
        resultado = await temas_collection.update_one(
            {
                "_id": tema_uuid,
                "niveles.nivel": nivel.value
            },
            {
                "$pull": {
                    "niveles.$.preguntas": {
                        "id": pregunta_uuid
                    }
                }
            }
        )
        
        if resultado.matched_count == 0:
            raise HTTPException(status_code=404, detail="Tema o nivel no encontrado")
        
        # Verificar si la pregunta existía antes de intentar eliminarla
        tema = await temas_collection.find_one({"_id": tema_uuid, "niveles.nivel": nivel.value})
        pregunta_existe = False
        if tema:
            for nivel_doc in tema.get("niveles", []):
                if nivel_doc.get("nivel") == nivel.value:
                    for pregunta in nivel_doc.get("preguntas", []):
                        if pregunta.get("id") == pregunta_uuid:
                            pregunta_existe = True
                            break

        if not pregunta_existe:
            raise HTTPException(status_code=404, detail="Pregunta no encontrada")
        
        return {
            "mensaje": "Pregunta eliminada exitosamente",
            "pregunta_id": pregunta_id,
            "tema_id": tema_id,
            "nivel": nivel.value
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# 3. ACTUALIZAR UNA PREGUNTA ESPECÍFICA
@router.put("/temas/{tema_id}/niveles/{nivel}/preguntas/{pregunta_id}", response_model=Dict[str, Any])
async def actualizar_pregunta(
    tema_id: str,
    nivel: NivelEnum,
    pregunta_id: str,
    pregunta_data: PreguntaUpdate
):
    """Actualiza una pregunta específica de un tema"""
    try:
        # ✅ SIMPLIFICADO: Solo convertir a UUID
        tema_uuid = UUID(tema_id)
        pregunta_uuid = UUID(pregunta_id)
        
        # Crear el objeto de actualización solo con campos no nulos
        update_data = {
            f"niveles.$[nivel].preguntas.$[pregunta].{k}": v 
            for k, v in pregunta_data.dict(exclude_unset=True).items()
        }
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        # Actualizar usando arrayFilters
        resultado = await temas_collection.update_one(
            {"_id": tema_uuid},
            {"$set": update_data},
            array_filters=[
                {"nivel.nivel": nivel.value},
                {"pregunta.id": pregunta_uuid}
            ]
        )
        
        if resultado.matched_count == 0:
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        
        if resultado.modified_count == 0:
            raise HTTPException(status_code=404, detail="Pregunta no encontrada o sin cambios")
        
        return {
            "mensaje": "Pregunta actualizada exitosamente",
            "pregunta_id": pregunta_id,
            "tema_id": tema_id,
            "nivel": nivel.value
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# 4. OBTENER TODAS LAS PREGUNTAS DE UN NIVEL ESPECÍFICO - ✅ CORREGIDO
@router.get("/temas/{tema_id}/niveles/{nivel}/preguntas", response_model=Dict[str, Any])
async def obtener_preguntas_nivel(
    tema_id: str,
    nivel: NivelEnum
):
    """Obtiene todas las preguntas de un nivel específico"""
    try:
        # ✅ SIMPLIFICADO: Solo convertir a UUID
        tema_uuid = UUID(tema_id)
        
        # ✅ CORREGIDO: Pipeline sin conversión problemática de UUID a string
        pipeline = [
            {"$match": {"_id": tema_uuid}},
            {"$unwind": "$niveles"},
            {"$match": {"niveles.nivel": nivel.value}},
            {"$project": {
                "tema_nombre": "$nombre",
                "nivel": "$niveles.nivel",
                "preguntas": "$niveles.preguntas"
            }}
        ]
        
        resultado = await temas_collection.aggregate(pipeline).to_list(1)
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Tema o nivel no encontrado")
        
        # ✅ SIMPLIFICADO: Usar helper para serializar UUIDs
        resultado_serializado = serialize_uuids_for_json(resultado[0])
        
        return {
            "tema_id": tema_id,  # ✅ CORREGIDO: Usar parámetro original (ya es string)
            "tema_nombre": resultado_serializado["tema_nombre"],
            "nivel": resultado_serializado["nivel"],
            "preguntas": resultado_serializado["preguntas"],
            "total_preguntas": len(resultado_serializado["preguntas"])
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de tema inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# 5. OBTENER UNA PREGUNTA ESPECÍFICA - ✅ CORREGIDO
@router.get("/temas/{tema_id}/niveles/{nivel}/preguntas/{pregunta_id}", response_model=Dict[str, Any])
async def obtener_pregunta_especifica(
    tema_id: str,
    nivel: NivelEnum,
    pregunta_id: str
):
    """Obtiene una pregunta específica"""
    try:
        # ✅ SIMPLIFICADO: Solo convertir a UUID
        tema_uuid = UUID(tema_id)
        pregunta_uuid = UUID(pregunta_id)
        
        # ✅ CORREGIDO: Pipeline sin conversión problemática de UUID a string
        pipeline = [
            {"$match": {"_id": tema_uuid}},
            {"$unwind": "$niveles"},
            {"$match": {"niveles.nivel": nivel.value}},
            {"$unwind": "$niveles.preguntas"},
            {"$match": {"niveles.preguntas.id": pregunta_uuid}},
            {"$project": {
                "tema_nombre": "$nombre",
                "nivel": "$niveles.nivel",
                "pregunta": "$niveles.preguntas"
            }}
        ]
        
        resultado = await temas_collection.aggregate(pipeline).to_list(1)
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Pregunta no encontrada")
            
        
        # ✅ SIMPLIFICADO: Usar helper para serializar UUIDs
        resultado_serializado = serialize_uuids_for_json(resultado[0])
        
        return {
            "tema_id": tema_id,  # ✅ CORREGIDO: Usar parámetro original (ya es string)
            "tema_nombre": resultado_serializado["tema_nombre"],
            "nivel": resultado_serializado["nivel"],
            "pregunta": resultado_serializado["pregunta"]
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")