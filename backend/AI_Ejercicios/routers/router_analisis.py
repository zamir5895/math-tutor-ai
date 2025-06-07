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
    tags=["Analisis"]
)


@router.post("/analisis/patrones", response_model=Dict[str, Any])
async def analizar_patrones_errores(request: Dict[str, Any]):
    """
    Analiza patrones de errores del alumno y proporciona recomendaciones
    Body: {
        "alumno_id": "string",
        "tema_id": "string" (opcional)
    }
    """
    try:
        alumno_id = request.get("alumno_id")
        tema_id = request.get("tema_id")
        
        try:
            alumno_uuid = UUID(alumno_id)
            tema_uuid = UUID(tema_id) if tema_id else None
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        # Construir filtro
        filtro = {"alumno_id": alumno_uuid}
        if tema_uuid:
            filtro["tema_id"] = tema_uuid
        
        # Obtener progresos del alumno
        progresos = await progresos_collection.find(filtro).to_list(100)
        
        if not progresos:
            raise HTTPException(status_code=404, detail="No se encontraron progresos para analizar")
        
        # Recopilar todas las respuestas
        todas_respuestas = []
        for progreso in progresos:
            todas_respuestas.extend(progreso.get("respuestas", []))
        
        if not todas_respuestas:
            raise HTTPException(status_code=404, detail="No se encontraron respuestas para analizar")
        
        # Analizar patrones
        analisis = await gpt_service.analizar_patron_errores(todas_respuestas)
        
        return {
            "status": "Análisis completado",
            "alumno_id": alumno_id,
            "respuestas_analizadas": len(todas_respuestas),
            "analisis": analisis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ejercicios/personalizados", response_model=Dict[str, Any])
async def generar_ejercicios_personalizados(request: Dict[str, Any]):
    """
    Genera ejercicios personalizados basados en las dificultades del alumno
    Body: {
        "alumno_id": "string",
        "tema": "string",
        "dificultades_identificadas": ["concepto1", "concepto2"]
    }
    """
    try:
        alumno_id = request.get("alumno_id")
        tema = request.get("tema")
        dificultades = request.get("dificultades_identificadas", [])
        
        try:
            alumno_uuid = UUID(alumno_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        if not tema:
            raise HTTPException(status_code=400, detail="Se requiere especificar el tema")
        
        ejercicios = await gpt_service.generar_ejercicios_personalizados(
            str(alumno_uuid), tema, dificultades
        )
        
        return {
            "status": "Ejercicios personalizados generados",
            "tema": tema,
            "ejercicios": ejercicios
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ejercicios/adicionales", response_model=Dict[str, Any])
async def generar_ejercicios_adicionales(request: Dict[str, Any]):
    """
    Genera ejercicios adicionales basados en el nivel del alumno
    Body: {
        "tema": "string",
        "nivel": "facil|medio|dificil",
        "cantidad": int (opcional, default 5),
        "alumno_id": "string" (opcional, para personalizar)
    }
    """
    try:
        tema = request.get("tema")
        nivel = request.get("nivel")
        cantidad = request.get("cantidad", 5)
        alumno_id = request.get("alumno_id")
        
        if not tema or not nivel:
            raise HTTPException(
                status_code=400,
                detail="Se requieren los campos 'tema' y 'nivel'"
            )
        
        # Convertir alumno_id a string si es válido
        alumno_id_str = None
        if alumno_id:
            try:
                alumno_uuid = UUID(alumno_id)
                alumno_id_str = str(alumno_uuid)
            except ValueError:
                pass  # Ignorar si el ID no es válido
        
        # Generar ejercicios adicionales
        ejercicios_adicionales = await gpt_service.generar_ejercicios_adicionales(
            tema, nivel, cantidad, alumno_id_str
        )
        
        return {
            "status": "Ejercicios adicionales generados exitosamente",
            "tema": tema,
            "nivel": nivel,
            "cantidad_generada": len(ejercicios_adicionales),
            "ejercicios": ejercicios_adicionales
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/temas", response_model=Dict[str, Any])
async def listar_temas():
    """Lista todos los temas disponibles"""
    try:
        temas = await temas_collection.find({}, {"nombre": 1, "descripcion": 1}).to_list(100)
        for tema in temas:
            tema["id"] = str(tema["_id"])
            del tema["_id"]  # Eliminar _id para evitar confusión
        
        return {
            "temas": temas,
            "total": len(temas)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas/{alumno_id}", response_model=Dict[str, Any])
async def obtener_estadisticas_alumno(alumno_id: str):
    """Obtiene estadísticas generales de un alumno"""
    try:
        try:
            alumno_uuid = UUID(alumno_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        # Obtener todos los progresos del alumno
        progresos = await progresos_collection.find(
            {"alumno_id": alumno_uuid}
        ).to_list(100)
        
        # Calcular estadísticas
        total_temas = len(progresos)
        total_ejercicios = sum(len(p.get("respuestas", [])) for p in progresos)
        ejercicios_correctos = sum(
            sum(1 for r in p.get("respuestas", []) if r.get("correcto", False))
            for p in progresos
        )
        precision_general = (ejercicios_correctos / total_ejercicios * 100) if total_ejercicios > 0 else 0
        
        # Obtener reportes
        reportes = await reportes_collection.find(
            {"alumno_id": alumno_uuid}
        ).sort("fecha", -1).to_list(100)
        
        return {
            "estadisticas": {
                "temas_estudiados": total_temas,
                "ejercicios_resueltos": total_ejercicios,
                "ejercicios_correctos": ejercicios_correctos,
                "precision_general": f"{precision_general:.1f}%",
                "reportes_generados": len(reportes),
                "ultimo_reporte": reportes[0]["fecha"] if reportes else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

