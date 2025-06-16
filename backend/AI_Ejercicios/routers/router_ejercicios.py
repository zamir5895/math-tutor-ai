from fastapi import APIRouter, HTTPException, Query, Body, status
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
from tema import NivelEnum

from service import GPTService
from solucionarioService import SolucionarioService
from db import alumnos_collection, temas_collection, progresos_collection, reportes_collection



gpt_service = GPTService()
solucionario_service = SolucionarioService()

router = APIRouter(
    prefix="",
    tags=["Ejercicios"]
)


@router.get("/ejercicio", response_model=Dict[str, Any])
async def generar_ejercicios(
    tema: str = Query(..., description="Nombre del tema para generar ejercicios"),
    forzar_generacion: bool = Query(False, description="Forzar generación aunque el tema exista")
):
    try:
        print(f"TEMA RECIBIDO: {tema} (type: {type(tema)})")
        print(f"FORZAR_GENERACION RECIBIDO: {forzar_generacion} (type: {type(forzar_generacion)})")
        
        resultado = await gpt_service.generar_ejercicios(tema, forzar_generacion)
        print("RESULTADO:", resultado)
        return resultado
    except Exception as e:
        import traceback
        print("ERROR EN ENDPOINT /ejercicios:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/ejercicios/{tema}", response_model=Dict[str, Any])
async def obtener_ejercicios(tema: str):
    """Obtiene ejercicios de un tema específico"""
    try:
        tema_data = await temas_collection.find_one(
            {"nombre": {"$regex": f"^{tema}$", "$options": "i"}}
        )
        
        if not tema_data:
            try:
                resultado = await gpt_service.generar_ejercicios(tema)
                tema_data = await temas_collection.find_one(
                    {"nombre": {"$regex": f"^{tema}$", "$options": "i"}}
                )
            except Exception as e:
                raise HTTPException(
                    status_code=404,
                    detail=f"Tema '{tema}' no encontrado y no se pudo generar: {str(e)}"
                )

        tema_data["id"] = str(tema_data.pop("_id"))
        
        return {"tema": tema_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ejercicios: {str(e)}")


@router.get("/ejercicios/{tema}/nivel/{nivel}", response_model=Dict[str, Any])
async def obtener_ejercicios_por_nivel(tema: str, nivel: NivelEnum):
    """Obtiene ejercicios de un tema específico filtrados por nivel"""
    tema_data = await temas_collection.find_one(
        {"nombre": {"$regex": f"^{tema}$", "$options": "i"}}
    )
    
    if not tema_data:
        raise HTTPException(status_code=404, detail=f"Tema '{tema}' no encontrado")
    
    ejercicios_nivel = []
    for nivel_data in tema_data.get("niveles", []):
        if nivel_data["nivel"] == nivel:
            ejercicios_nivel = nivel_data["preguntas"]
            break
    
    return {
        "tema": tema,
        "nivel": nivel,
        "ejercicios": ejercicios_nivel,
        "total": len(ejercicios_nivel)
    }


