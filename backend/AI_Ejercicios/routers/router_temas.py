from fastapi import APIRouter, HTTPException, Query, Body, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any


from uuid import UUID, uuid4 
from bson import Binary
from pymongo import ReturnDocument

from alumno import Alumno
from tema import NivelEnum, Tema, TemaCreate, TemaUpdate, TemaResponse, Pregunta, PreguntaCreate, PreguntaUpdate, Nivel

from db import alumnos_collection, temas_collection, progresos_collection, reportes_collection



router = APIRouter(
    prefix="",
    tags=["Temas"]
)


@router.post("/temas", response_model=TemaResponse, status_code=status.HTTP_201_CREATED)
async def crear_tema(tema_data: TemaCreate):
    try:
        nuevo_tema = Tema(**tema_data.dict())
        
        if not isinstance(nuevo_tema.id, UUID):
            raise HTTPException(status_code=400, detail="El ID del tema no es un UUID válido.")
        
        tema_dict = nuevo_tema.dict(by_alias=True)
        
        tema_dict["_id"] = Binary.from_uuid(nuevo_tema.id)
        
        for nivel in tema_dict.get("niveles", []):
            for pregunta in nivel.get("preguntas", []):

                if "id" in pregunta:
                    if isinstance(pregunta["id"], str):
                        pregunta["id"] = Binary.from_uuid(UUID(pregunta["id"]))
                    elif isinstance(pregunta["id"], UUID):
                        pregunta["id"] = Binary.from_uuid(pregunta["id"])
        
        resultado = await temas_collection.insert_one(tema_dict)
        
        if not resultado.inserted_id:
            raise HTTPException(status_code=500, detail="No se pudo crear el tema")
        
        tema_response = TemaResponse(
            **nuevo_tema.dict(exclude={"id"}),
            id=str(nuevo_tema.id)
        )
        
        return tema_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear tema: {str(e)}")



@router.get("/temas", response_model=List[TemaResponse])
async def obtener_todos_los_temas(
    skip: int = 0,
    limit: int = 100
):
    try:
        cursor = temas_collection.find().skip(skip).limit(limit)
        temas = await cursor.to_list(length=limit)
        
        temas_response = []
        for tema in temas:
            if isinstance(tema.get("_id"), Binary):
                tema_id = str(tema["_id"].as_uuid())
            else:
                tema_id = str(tema["_id"])
            
            for nivel in tema.get("niveles", []):
                for pregunta in nivel.get("preguntas", []):
                    if "id" in pregunta and isinstance(pregunta["id"], Binary):
                        pregunta["id"] = str(pregunta["id"].as_uuid())
            
            tema_response = TemaResponse(
                **{k: v for k, v in tema.items() if k != "_id"},
                id=tema_id
            )
            temas_response.append(tema_response)
        
        return temas_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener temas: {str(e)}")

@router.get("/temas/{tema_id}", response_model=TemaResponse)
async def obtener_tema_por_id(tema_id: str):
    try:
        print(f"DEBUG: Recibido tema_id: '{tema_id}' (tipo: {type(tema_id)}, longitud: {len(tema_id)})")
        
        tema_id_clean = tema_id.strip()
        print(f"DEBUG: tema_id limpio: '{tema_id_clean}'")
        
        tema_uuid = UUID(tema_id_clean)
        print(f"DEBUG: UUID convertido: {tema_uuid}")
        
        tema = await temas_collection.find_one({"_id": tema_uuid})
        print(f"DEBUG: Resultado de búsqueda: {tema is not None}")
        
        if not tema:
            print("DEBUG: Buscando todos los temas para diagnosticar...")
            all_temas = await temas_collection.find({}, {"_id": 1, "nombre": 1}).to_list(length=10)
            print(f"DEBUG: Temas existentes: {[(str(t.get('_id')), t.get('nombre')) for t in all_temas]}")
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        
        def convert_uuids_to_string(obj):
            if isinstance(obj, dict):
                return {k: convert_uuids_to_string(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_uuids_to_string(item) for item in obj]
            elif isinstance(obj, UUID):
                return str(obj)
            elif isinstance(obj, Binary):
                return str(obj.as_uuid())
            else:
                return obj
        
        tema_clean = convert_uuids_to_string(tema)
        
        tema_response = TemaResponse(
            **{k: v for k, v in tema_clean.items() if k != "_id"},
            id=tema_id_clean
        )
        return tema_response
        
    except ValueError as ve:
        print(f"DEBUG: Error de ValueError: {ve}")
        print(f"DEBUG: tema_id que causó el error: '{tema_id}'")
        raise HTTPException(status_code=400, detail=f"ID de tema inválido: {tema_id}")
    except Exception as e:
        print(f"DEBUG: Error general: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener tema: {str(e)}")




    
        
@router.put("/temas/{tema_id}", response_model=TemaResponse)
async def actualizar_tema(tema_id: str, tema_data: TemaUpdate):
    try:
        tema_uuid = UUID(tema_id)
        tema_binary_id = Binary.from_uuid(tema_uuid)
        
        update_data = tema_data.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        if "niveles" in update_data:
            for nivel in update_data["niveles"]:
                for pregunta in nivel.get("preguntas", []):
                    if "id" in pregunta:
                        if isinstance(pregunta["id"], str):
                            try:
                                pregunta["id"] = Binary.from_uuid(UUID(pregunta["id"]))
                            except Exception:
                                pass  
        
        resultado = await temas_collection.find_one_and_update(
            {"_id": tema_binary_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        
        for nivel in resultado.get("niveles", []):
            for pregunta in nivel.get("preguntas", []):
                if "id" in pregunta and isinstance(pregunta["id"], Binary):
                    try:
                        pregunta["id"] = str(pregunta["id"].as_uuid())
                    except Exception:
                        pregunta["id"] = str(pregunta["id"])
        
        tema_response = TemaResponse(
            **{k: v for k, v in resultado.items() if k != "_id"},
            id=str(tema_uuid)
        )
        
        return tema_response
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de tema inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar tema: {str(e)}")





@router.delete("/temas/{tema_id}")
async def eliminar_tema(tema_id: str):
    """Elimina un tema por su ID"""
    try:
        tema_uuid = UUID(tema_id)
        tema_binary_id = Binary.from_uuid(tema_uuid)
        
        tema_existente = await temas_collection.find_one({"_id": tema_binary_id})
        
        if not tema_existente:
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        
        resultado = await temas_collection.delete_one({"_id": tema_binary_id})
        
        if resultado.deleted_count == 0:
            raise HTTPException(status_code=500, detail="No se pudo eliminar el tema")
        
        return {
            "mensaje": "Tema eliminado exitosamente",
            "tema_id": tema_id,
            "tema_nombre": tema_existente.get("nombre", "Desconocido")
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de tema inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar tema: {str(e)}")
    

