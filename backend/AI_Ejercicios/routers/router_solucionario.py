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
    tags=["Solucionario"]
)



@router.post("/solucionario/resolver", response_model=Dict[str, Any])
async def resolver_ejercicio(request: Dict[str, Any]):
    """
    Resuelve un ejercicio paso a paso con explicación detallada
    Body: {
        "pregunta": "string",
        "tema": "string",
        "nivel": "facil|medio|dificil"
    }
    """
    try:
        pregunta = request.get("pregunta")
        tema = request.get("tema")
        nivel = request.get("nivel", "medio")
        
        if not pregunta or not tema:
            raise HTTPException(
                status_code=400,
                detail="Se requieren los campos 'pregunta' y 'tema'"
            )
        
        solucion = await solucionario_service.resolver_ejercicio(pregunta, tema, nivel)
        return solucion
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/solucionario/evaluar", response_model=Dict[str, Any])
async def evaluar_respuesta(request: Dict[str, Any]):
    """
    Evalúa la respuesta de un estudiante y proporciona retroalimentación
    Body: {
        "pregunta": "string",
        "respuesta_correcta": "string",
        "respuesta_alumno": "string",
        "tema": "string"
    }
    """
    try:
        pregunta = request.get("pregunta")
        respuesta_correcta = request.get("respuesta_correcta")
        respuesta_alumno = request.get("respuesta_alumno")
        tema = request.get("tema")
        
        if not all([pregunta, respuesta_correcta, respuesta_alumno, tema]):
            raise HTTPException(
                status_code=400,
                detail="Se requieren todos los campos: pregunta, respuesta_correcta, respuesta_alumno, tema"
            )
        
        evaluacion = await solucionario_service.evaluar_respuesta(
            pregunta, respuesta_correcta, respuesta_alumno, tema
        )
        return evaluacion
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
