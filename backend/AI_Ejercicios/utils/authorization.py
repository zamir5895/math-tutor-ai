from fastapi import HTTPException
import httpx  # Para realizar las solicitudes HTTP al endpoint de verificación del token
from typing import List, Optional, Dict, Any
from uuid import UUID



# Funciones de autenticación y autorización
async def verify_student_token(token: str) -> Dict[str, Any]:
    """
    Verifica que el token sea válido y pertenezca a un STUDENT
    Retorna los datos del usuario si es válido
    """
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8080/auth/verify-token", headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        data = resp.json()
        if data.get("role") != "STUDENT":
            raise HTTPException(status_code=403, detail="No es estudiante")
        
        return data

async def verify_teacher_token(token: str) -> Dict[str, Any]:
    """
    Verifica que el token sea válido y pertenezca a un TEACHER
    Retorna los datos del usuario si es válido
    """
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8080/auth/verify-token", headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        data = resp.json()
        if data.get("role") != "TEACHER":
            raise HTTPException(status_code=403, detail="No es profesor")
        
        return data

async def verify_admin_token(token: str) -> Dict[str, Any]:
    """
    Verifica que el token sea válido y pertenezca a un ADMIN
    Retorna los datos del usuario si es válido
    """
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8080/auth/verify-token", headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        data = resp.json()
        if data.get("role") != "ADMIN":
            raise HTTPException(status_code=403, detail="No es administrador")
        
        return data
    


async def verify_teacher_or_admin_token(token: str) -> Dict[str, Any]:
    """
    Verifica que el token sea válido y pertenezca a un TEACHER o ADMIN
    Retorna los datos del usuario si es válido
    """
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8080/auth/verify-token", headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        data = resp.json()
        if data.get("role") not in ["TEACHER", "ADMIN"]:
            raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol de profesor o administrador")
        
        return data
    




async def verify_student_token_and_id(token: str, alumno_id: str) -> bool:
    """
    Verifica que el token sea válido, pertenezca a un STUDENT y que el userID
    coincida con el alumno_id proporcionado.
    
    Retorna True si el userID es igual al alumno_id, de lo contrario False.
    """
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        # Realizar la solicitud de verificación del token
        resp = await client.get("http://localhost:8080/auth/verify-token", headers=headers)
        
        # Si la respuesta no es 200, lanzar una excepción de token inválido
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        # Extraer los datos de la respuesta
        data = resp.json()
        
        # Verificar que el role sea "STUDENT"
        if data.get("role") != "STUDENT":
            raise HTTPException(status_code=403, detail="No es estudiante")
        
        # Obtener el userID desde la respuesta
        user_id_from_token = data.get("userId")
        
        # Comparar el userID con el alumno_id proporcionado
        return user_id_from_token == alumno_id
