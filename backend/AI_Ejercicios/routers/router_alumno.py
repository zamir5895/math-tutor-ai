from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from uuid import UUID
from bson import Binary
import httpx
import logging
from bson import Binary, ObjectId
from utils.authorization import verify_teacher_or_admin_token, verify_student_token_and_id
from pydantic import BaseModel

from db import alumnos_collection, temas_collection
from fastapi import Header


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/alumnos",
    tags=["Alumnos"]
)


@router.post("/enroll_alumno_tema", response_model=Dict[str, Any])
async def enroll_alumno_tema(
    tema_id: str = Body(...),
    token: str = Body(...),
    alumno_id: str = Body(...)
):
    try:
        auth_data = await verify_teacher_or_admin_token(token)
        
        try:
            student_uuid = UUID(alumno_id)
            student_id_binary = Binary.from_uuid(student_uuid)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        alumno = await alumnos_collection.find_one({"_id": student_id_binary})
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        
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
        
        if "temas" not in alumno:
            alumno["temas"] = []
        
        temas_inscritos = [str(t.get("id")) for t in alumno["temas"]]
        if tema_id in temas_inscritos:
            return {
                "status": "Ya inscrito",
                "message": f"El alumno ya está inscrito en el tema '{tema['nombre']}'",
                "alumno_id": alumno_id,
                "tema": tema["nombre"],
                "enrolled_by": auth_data.get("username"),
                "enrolled_by_role": auth_data.get("role")
            }
        
        alumno["temas"].append({
            "id": tema_id,
            "nombre": tema["nombre"],
            "nivel": "facil"
        })
        
        await alumnos_collection.update_one(
            {"_id": student_id_binary},
            {"$set": {"temas": alumno["temas"]}}
        )
        
        return {
            "status": "Inscrito",
            "message": f"Alumno inscrito exitosamente en el tema '{tema['nombre']}'",
            "alumno_id": alumno_id,
            "tema": tema["nombre"],
            "enrolled_by": auth_data.get("username"),
            "enrolled_by_role": auth_data.get("role")
        }
        
    except HTTPException as http_exc:
        raise http_exc
    except ValueError as ve:
        logger.error(f"Error de UUID: {str(ve)}")
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        logger.error(f"Error en enroll_alumno_tema: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    






@router.post("/unenroll_alumno_tema", response_model=Dict[str, Any])
async def unenroll_alumno_tema(
    tema_id: str = Body(...),
    token: str = Body(...),
    alumno_id: str = Body(...)
):
    try:
        auth_data = await verify_teacher_or_admin_token(token)
        
        try:
            student_uuid = UUID(alumno_id)
            student_id_binary = Binary.from_uuid(student_uuid)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        alumno = await alumnos_collection.find_one({"_id": student_id_binary})
        if not alumno:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
        print(f"DEBUG: Recibido tema_id: '{tema_id}' (tipo: {type(tema_id)}, longitud: {len(tema_id)})")
        tema_id_clean = tema_id.strip()
        print(f"DEBUG: tema_id limpio: '{tema_id_clean}'")
        tema_uuid = UUID(tema_id_clean)
        print(f"DEBUG: UUID convertido: {tema_uuid}")

        tema = await temas_collection.find_one({"_id": tema_uuid})
        print(f"DEBUG: Resultado de búsqueda: {tema is not None}")
        
        if not tema:
            # Vamos a buscar todos los temas para ver qué IDs existen
            print("DEBUG: Buscando todos los temas para diagnosticar...")
            all_temas = await temas_collection.find({}, {"_id": 1, "nombre": 1}).to_list(length=10)
            print(f"DEBUG: Temas existentes: {[(str(t.get('_id')), t.get('nombre')) for t in all_temas]}")
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        
        # Verificar si el alumno está inscrito en el tema
        if "temas" not in alumno:
            alumno["temas"] = []
        
        temas_inscritos = [str(t.get("id")) for t in alumno["temas"]]
        if tema_id not in temas_inscritos:
            raise HTTPException(status_code=400, detail=f"El alumno no está inscrito en el tema '{tema['nombre']}'")
        
        # Desinscribir al alumno del tema
        alumno["temas"] = [t for t in alumno["temas"] if str(t.get("id")) != tema_id]
        
        # Actualizar en la base de datos
        await alumnos_collection.update_one(
            {"_id": student_id_binary},
            {"$set": {"temas": alumno["temas"]}}
        )
        
        return {
            "status": "Desinscrito",
            "message": f"Alumno desinscrito exitosamente del tema '{tema['nombre']}'",
            "alumno_id": alumno_id,
            "tema": tema["nombre"],
            "unenrolled_by": auth_data.get("username"),
            "unenrolled_by_role": auth_data.get("role")
        }
        
    except HTTPException as http_exc:
        # Permitir que FastAPI maneje HTTPException correctamente
        raise http_exc
    except ValueError as ve:
        logger.error(f"Error de UUID: {str(ve)}")
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        logger.error(f"Error en unenroll_alumno_tema: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")





@router.get("/{usuario_id}", response_model=Dict[str, Any])
async def obtener_usuario_v2(
    usuario_id: str,
    authorization: str = Header(...)
):
    """Obtiene información de un usuario por ID - Versión simplificada"""
    try:
        # Extraer el token Bearer
        if not isinstance(authorization, str) or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Formato de autorización inválido")
        token = authorization.removeprefix("Bearer ").strip()

        # Verificar si el token es de un estudiante
        auth_data = None
        auth_data2 = None
        try:
            auth_data = await verify_student_token_and_id(token, usuario_id)
        except Exception:
            auth_data = None
        if not auth_data:
            try:
                auth_data2 = await verify_teacher_or_admin_token(token)
            except Exception:
                auth_data2 = None
        if not auth_data and not auth_data2:
            raise HTTPException(status_code=403, detail="No autorizado para acceder a este recurso")

        # ✅ SIMPLIFICADO: Solo convertir string a UUID
        user_uuid = UUID(usuario_id)
        
        # ✅ MongoDB ahora maneja automáticamente la conversión UUID ↔ Binary
        usuario = await alumnos_collection.find_one({"_id": user_uuid})
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # ✅ Ya no necesitas serialize_binary - MongoDB devuelve UUIDs como objetos UUID
        # Pero FastAPI necesita serializar UUIDs, así que convertimos a string
        if "_id" in usuario:
            usuario["_id"] = str(usuario["_id"])
        
        return {"usuario": usuario}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    


class TemaUpdate(BaseModel):
    nombre: str
    nivel: str  # aquí podrías también usar Literal["facil","medio","dificil"] si quieres validar valores.

@router.put("/{usuario_id}/temas/{tema_id}", response_model=Dict[str, Any])
async def actualizar_tema_de_usuario(
    usuario_id: str,
    tema_id: str,
    tema_data: TemaUpdate,
    authorization: str = Header(...)
):
    """Actualiza un tema (por tema_id) dentro del array `temas` de un usuario."""
    # 1) Validación Authorization header
    if not isinstance(authorization, str) or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de autorización inválido")
    token = authorization.removeprefix("Bearer ").strip()

    # 2) Verificar permisos: mismo estudiante o profesor/admin
    permitido = False
    try:
        if await verify_student_token_and_id(token, usuario_id):
            permitido = True
    except:
        pass
    if not permitido:
        try:
            if await verify_teacher_or_admin_token(token):
                permitido = True
        except:
            pass
    if not permitido:
        raise HTTPException(status_code=403, detail="No autorizado")

    # 3) Validar UUID de usuario (lanza ValueError si inválido)
    try:
        user_uuid = UUID(usuario_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")

    # 4) Ejecución update: filtramos por _id de usuario y existencia del tema en el array
    result = await alumnos_collection.update_one(
        {"_id": user_uuid, "temas.id": tema_id},
        {"$set": {
            "temas.$.nombre": tema_data.nombre,
            "temas.$.nivel": tema_data.nivel
        }}
    )
    # 5) Interpretar resultado
    if result.matched_count == 0:
        # Puede ser que el usuario no exista o que el tema no esté en su array
        existe_usuario = await alumnos_collection.find_one({"_id": user_uuid})
        if not existe_usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        else:
            raise HTTPException(status_code=404, detail="Tema no encontrado para este usuario")

    # 6) Recuperar el documento actualizado
    usuario = await alumnos_collection.find_one({"_id": user_uuid})
    usuario["_id"] = str(usuario["_id"])
    return {"usuario": usuario}
