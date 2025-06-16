from fastapi import FastAPI, HTTPException, Query, Body, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import httpx  
import logging
from uuid import UUID, uuid4  
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



from routers.router_alumno import router as alumno_router
from routers.router_preguntas import router as preguntas_router
from routers.router_respuestas import router as respuestas_router
from routers.router_temas import router as temas_router
from routers.router_ejercicios import router as ejercicios_router
from routers.router_solucionario import router as solucionario_router
from routers.router_progreso import router as progreso_router
from routers.router_reporte import router as reporte_router
from routers.router_analisis import router as analisis_router



load_dotenv()

app = FastAPI(title="Plataforma de Aprendizaje", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gpt_service = GPTService()
solucionario_service = SolucionarioService()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



app.include_router(alumno_router)




app.include_router(preguntas_router)




app.include_router(respuestas_router)


app.include_router(temas_router)



app.include_router(ejercicios_router)


app.include_router(solucionario_router)


app.include_router(progreso_router)



app.include_router(reporte_router)

app.include_router(analisis_router)


@app.get("/health")
async def health_check():
    """Endpoint de salud de la API"""
    return {"status": "OK", "timestamp": datetime.utcnow()}