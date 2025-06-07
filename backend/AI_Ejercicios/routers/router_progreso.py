from fastapi import APIRouter, HTTPException, Query, Body, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import httpx  # Para realizar las solicitudes HTTP al endpoint de verificación del token
import logging
from uuid import UUID, uuid4  # Usamos UUID en lugar de ObjectId y agregamos uuid4
from bson import Binary, ObjectId
from pymongo import ReturnDocument

# Modelos
from alumno import Alumno
from tema import NivelEnum, Tema, TemaCreate, TemaUpdate, TemaResponse, Pregunta, PreguntaCreate, PreguntaUpdate, Nivel
from progreso import Progreso, ProgresoCreate, RespuestaAlumno
from reporte import Reporte, ReporteCreate
from service import GPTService
from solucionarioService import SolucionarioService
from db import alumnos_collection, temas_collection, progresos_collection, reportes_collection
from request import LoginAlumnoRequest

gpt_service = GPTService()
solucionario_service = SolucionarioService()

router = APIRouter(
    prefix="",
    tags=["Progreso"]
)

@router.post("/progreso/iniciar", response_model=Dict[str, Any])
async def iniciar_progreso(request: Dict[str, Any]):
    """
    Inicia el progreso de un alumno en un tema específico
    Body: {
        "alumno_id": "string",
        "tema_id": "string"
    }
    """
    try:
        alumno_id = request.get("alumno_id")
        tema_id = request.get("tema_id")
        
        try:
            alumno_uuid = UUID(alumno_id)
            tema_uuid = UUID(tema_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="IDs inválidos")
        
        # Verificar si ya existe progreso
        progreso_existente = await progresos_collection.find_one({
            "alumno_id": alumno_uuid,
            "tema_id": tema_uuid,
            "estado": "en_progreso"
        })
        
        if progreso_existente:
            progreso_existente["id"] = str(progreso_existente["_id"])
            progreso_existente["alumno_id"] = str(progreso_existente["alumno_id"])
            progreso_existente["tema_id"] = str(progreso_existente["tema_id"])
            return {
                "status": "Progreso ya existente",
                "progreso": progreso_existente
            }
        
        # Crear nuevo progreso
        nuevo_progreso = ProgresoCreate(
            alumno_id=alumno_uuid,
            tema_id=tema_uuid
        )
        
        # Convertir a dict y mapear id -> _id para MongoDB
        progreso_dict = nuevo_progreso.dict(by_alias=True)
        
        resultado = await progresos_collection.insert_one(progreso_dict)
        progreso_creado = await progresos_collection.find_one({"_id": resultado.inserted_id})
        
        progreso_creado["id"] = str(progreso_creado["_id"])
        progreso_creado["alumno_id"] = str(progreso_creado["alumno_id"])
        progreso_creado["tema_id"] = str(progreso_creado["tema_id"])
        
        return {
            "status": "Progreso iniciado exitosamente",
            "progreso": progreso_creado
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/progreso/responder", response_model=Dict[str, Any])
async def registrar_respuesta(request: Dict[str, Any]):
    """
    Registra la respuesta de un alumno a una pregunta
    Body: {
        "progreso_id": "string",
        "nivel": int,
        "pregunta": "string",
        "respuesta_alumno": "string",
        "respuesta_correcta": "string",
        "tema": "string"
    }
    """
    try:
        progreso_id = request.get("progreso_id")
        nivel = request.get("nivel")
        pregunta = request.get("pregunta")
        respuesta_alumno = request.get("respuesta_alumno")
        respuesta_correcta = request.get("respuesta_correcta")
        tema = request.get("tema")
        
        try:
            progreso_uuid = UUID(progreso_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de progreso inválido")
        
        # Evaluar respuesta
        evaluacion = await solucionario_service.evaluar_respuesta(
            pregunta, respuesta_correcta, respuesta_alumno, tema
        )
        
        # Crear respuesta del alumno
        nueva_respuesta = RespuestaAlumno(
            nivel=nivel,
            pregunta=pregunta,
            respuesta_alumno=respuesta_alumno,
            explicacion_gpt=evaluacion["explicacion"],
            correcto=evaluacion["correcto"]
        )
        
        # Actualizar progreso
        await progresos_collection.update_one(
            {"_id": progreso_uuid},
            {
                "$push": {"respuestas": nueva_respuesta.dict()},
                "$set": {"nivel_actual": nivel}
            }
        )
        
        return {
            "status": "Respuesta registrada exitosamente",
            "evaluacion": evaluacion,
            "siguiente_nivel": nivel + 1 if evaluacion["correcto"] else nivel
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/progreso/{alumno_id}/{tema_id}", response_model=Dict[str, Any])
async def obtener_progreso(alumno_id: str, tema_id: str):
    """Obtiene el progreso de un alumno en un tema específico"""
    try:
        try:
            alumno_uuid = UUID(alumno_id)
            tema_uuid = UUID(tema_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="IDs inválidos")
        
        progreso = await progresos_collection.find_one({
            "alumno_id": alumno_uuid,
            "tema_id": tema_uuid
        })
        
        if not progreso:
            raise HTTPException(status_code=404, detail="Progreso no encontrado")
        
        progreso["id"] = str(progreso["_id"])
        progreso["alumno_id"] = str(progreso["alumno_id"])
        progreso["tema_id"] = str(progreso["tema_id"])
        
        return {"progreso": progreso}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

