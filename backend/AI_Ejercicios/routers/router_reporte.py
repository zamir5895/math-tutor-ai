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
    tags=["Reporte"]
)



@router.post("/reportes/generar", response_model=Dict[str, Any])
async def generar_reporte(request: Dict[str, Any]):
    """
    Genera un reporte de rendimiento del alumno
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
        
        # Obtener progreso
        progreso = await progresos_collection.find_one({
            "alumno_id": alumno_uuid,
            "tema_id": tema_uuid
        })
        
        if not progreso:
            raise HTTPException(status_code=404, detail="No se encontró progreso para generar reporte")
        
        # Obtener información del tema
        tema = await temas_collection.find_one({"_id": tema_uuid})
        tema_nombre = tema["nombre"] if tema else "Tema desconocido"
        
        # Calcular métricas
        respuestas = progreso.get("respuestas", [])
        total_respuestas = len(respuestas)
        correctas = sum(1 for r in respuestas if r["correcto"])
        porcentaje = (correctas / total_respuestas * 100) if total_respuestas > 0 else 0
        nivel_maximo = max([r["nivel"] for r in respuestas]) if respuestas else 0
        
        # Generar observaciones con GPT
        observaciones = await solucionario_service.generar_observaciones_reporte(
            respuestas, porcentaje, nivel_maximo
        )
        
        # Crear reporte
        nuevo_reporte = ReporteCreate(
            alumno_id=alumno_uuid,
            tema_id=tema_uuid,
            tema_nombre=tema_nombre,
            nivel_maximo=nivel_maximo,
            respuestas_totales=total_respuestas,
            correctas=correctas,
            porcentaje=round(porcentaje, 2),
            observaciones=observaciones
        )
        
        # Convertir a dict y mapear para MongoDB
        reporte_dict = nuevo_reporte.dict(by_alias=True)
        
        resultado = await reportes_collection.insert_one(reporte_dict)
        reporte_creado = await reportes_collection.find_one({"_id": resultado.inserted_id})
        
        reporte_creado["id"] = str(reporte_creado["_id"])
        reporte_creado["alumno_id"] = str(reporte_creado["alumno_id"])
        reporte_creado["tema_id"] = str(reporte_creado["tema_id"])
        
        return {
            "status": "Reporte generado exitosamente",
            "reporte": reporte_creado,
            "metricas": {
                "nivel_alcanzado": nivel_maximo,
                "precision": f"{porcentaje:.1f}%",
                "ejercicios_resueltos": total_respuestas,
                "ejercicios_correctos": correctas,
                "ejercicios_incorrectos": total_respuestas - correctas
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reportes/{alumno_id}", response_model=Dict[str, Any])
async def obtener_reportes_alumno(alumno_id: str):
    """Obtiene todos los reportes de un alumno"""
    try:
        try:
            alumno_uuid = UUID(alumno_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        reportes = await reportes_collection.find(
            {"alumno_id": alumno_uuid}
        ).sort("fecha", -1).to_list(100)
        
        for reporte in reportes:
            reporte["id"] = str(reporte["_id"])
            reporte["alumno_id"] = str(reporte["alumno_id"])
            reporte["tema_id"] = str(reporte["tema_id"])
        
        return {
            "reportes": reportes,
            "total": len(reportes)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
