# main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime
import json
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Modelos
from alumno import Alumno, AlumnoCreate, PyObjectId
from tema import Tema, TemaCreate, NivelEnum
from progreso import Progreso, ProgresoCreate, RespuestaAlumno
from reporte import Reporte, ReporteCreate
from service import GPTService
from solucionarioService import SolucionarioService
from db import alumnos_collection, temas_collection, progresos_collection, reportes_collection
from request import LoginAlumnoRequest
load_dotenv()

app = FastAPI(title="Plataforma de Aprendizaje", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servicios
gpt_service = GPTService()
solucionario_service = SolucionarioService()

# ========================
# ENDPOINTS DE USUARIO
# ========================

@app.post("/usuarios/registrar", response_model=Dict[str, Any])
async def registrar_usuario(alumno: AlumnoCreate):
    """Registra un nuevo usuario en la plataforma"""
    # Verificar si el username ya existe
    print(f"Datos de registro recibidos: {alumno}")
    usuario_existente = await alumnos_collection.find_one({"username": alumno.username})
    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario registrado con este username"
        )
    
    # Crear nuevo usuario
    nuevo_alumno = Alumno(**alumno.dict())
    resultado = await alumnos_collection.insert_one(nuevo_alumno.dict(by_alias=True))
    
    # Obtener el usuario creado
    usuario_creado = await alumnos_collection.find_one({"_id": resultado.inserted_id})
    usuario_creado["_id"] = str(usuario_creado["_id"])
    
    return {
        "status": "Usuario registrado exitosamente",
        "usuario": usuario_creado
    }

@app.post("/usuarios/login", response_model=Dict[str, Any])
async def login_usuario(alumno: LoginAlumnoRequest):
    """Inicia sesión de usuario"""
    print(f"Datos de inicio de sesión recibidos: {alumno}")
    usuario = await alumnos_collection.find_one({"username": alumno.username})
    if not usuario or usuario.get("password") != alumno.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    usuario["_id"] = str(usuario["_id"])
    return {
        "status": "Inicio de sesión exitoso",
        "usuario": usuario
    }


@app.get("/usuarios/{usuario_id}", response_model=Dict[str, Any])
async def obtener_usuario(usuario_id: str):
    """Obtiene información de un usuario por ID"""
    if not ObjectId.is_valid(usuario_id):
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    
    usuario = await alumnos_collection.find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario["_id"] = str(usuario["_id"])
    return {"usuario": usuario}

# ========================
# ENDPOINTS DE EJERCICIOS
# ========================

@app.get("/ejercicio", response_model=Dict[str, Any])
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

@app.get("/ejercicios/{tema}", response_model=Dict[str, Any])
async def obtener_ejercicios(tema: str):
    """Obtiene ejercicios de un tema específico"""
    tema_data = await temas_collection.find_one(
        {"nombre": {"$regex": f"^{tema}$", "$options": "i"}}
    )
    
    if not tema_data:
        # Si no existe, generar automáticamente
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
    
    tema_data["_id"] = str(tema_data["_id"])
    return {"tema": tema_data}

@app.get("/ejercicios/{tema}/nivel/{nivel}", response_model=Dict[str, Any])
async def obtener_ejercicios_por_nivel(tema: str, nivel: NivelEnum):
    """Obtiene ejercicios de un tema específico filtrados por nivel"""
    tema_data = await temas_collection.find_one(
        {"nombre": {"$regex": f"^{tema}$", "$options": "i"}}
    )
    
    if not tema_data:
        raise HTTPException(status_code=404, detail=f"Tema '{tema}' no encontrado")
    
    # Filtrar por nivel
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

# ========================
# ENDPOINTS DE SOLUCIONARIO
# ========================

@app.post("/solucionario/resolver", response_model=Dict[str, Any])
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

@app.post("/solucionario/evaluar", response_model=Dict[str, Any])
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

# ========================
# ENDPOINTS DE PROGRESO
# ========================

@app.post("/progreso/iniciar", response_model=Dict[str, Any])
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
        
        if not ObjectId.is_valid(alumno_id) or not ObjectId.is_valid(tema_id):
            raise HTTPException(status_code=400, detail="IDs inválidos")
        
        # Verificar si ya existe progreso
        progreso_existente = await progresos_collection.find_one({
            "alumno_id": ObjectId(alumno_id),
            "tema_id": ObjectId(tema_id),
            "estado": "en_progreso"
        })
        
        if progreso_existente:
            progreso_existente["_id"] = str(progreso_existente["_id"])
            progreso_existente["alumno_id"] = str(progreso_existente["alumno_id"])
            progreso_existente["tema_id"] = str(progreso_existente["tema_id"])
            return {
                "status": "Progreso ya existente",
                "progreso": progreso_existente
            }
        
        # Crear nuevo progreso
        nuevo_progreso = ProgresoCreate(
            alumno_id=ObjectId(alumno_id),
            tema_id=ObjectId(tema_id)
        )
        
        resultado = await progresos_collection.insert_one(nuevo_progreso.dict(by_alias=True))
        progreso_creado = await progresos_collection.find_one({"_id": resultado.inserted_id})
        
        progreso_creado["_id"] = str(progreso_creado["_id"])
        progreso_creado["alumno_id"] = str(progreso_creado["alumno_id"])
        progreso_creado["tema_id"] = str(progreso_creado["tema_id"])
        
        return {
            "status": "Progreso iniciado exitosamente",
            "progreso": progreso_creado
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/progreso/responder", response_model=Dict[str, Any])
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
        
        if not ObjectId.is_valid(progreso_id):
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
            {"_id": ObjectId(progreso_id)},
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

@app.get("/progreso/{alumno_id}/{tema_id}", response_model=Dict[str, Any])
async def obtener_progreso(alumno_id: str, tema_id: str):
    """Obtiene el progreso de un alumno en un tema específico"""
    try:
        if not ObjectId.is_valid(alumno_id) or not ObjectId.is_valid(tema_id):
            raise HTTPException(status_code=400, detail="IDs inválidos")
        
        progreso = await progresos_collection.find_one({
            "alumno_id": ObjectId(alumno_id),
            "tema_id": ObjectId(tema_id)
        })
        
        if not progreso:
            raise HTTPException(status_code=404, detail="Progreso no encontrado")
        
        progreso["_id"] = str(progreso["_id"])
        progreso["alumno_id"] = str(progreso["alumno_id"])
        progreso["tema_id"] = str(progreso["tema_id"])
        
        return {"progreso": progreso}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========================
# ENDPOINTS DE REPORTES
# ========================

@app.post("/reportes/generar", response_model=Dict[str, Any])
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
        
        if not ObjectId.is_valid(alumno_id) or not ObjectId.is_valid(tema_id):
            raise HTTPException(status_code=400, detail="IDs inválidos")
        
        # Obtener progreso
        progreso = await progresos_collection.find_one({
            "alumno_id": ObjectId(alumno_id),
            "tema_id": ObjectId(tema_id)
        })
        
        if not progreso:
            raise HTTPException(status_code=404, detail="No se encontró progreso para generar reporte")
        
        # Obtener información del tema
        tema = await temas_collection.find_one({"_id": ObjectId(tema_id)})
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
            alumno_id=ObjectId(alumno_id),
            tema_id=ObjectId(tema_id),
            tema_nombre=tema_nombre,
            nivel_maximo=nivel_maximo,
            respuestas_totales=total_respuestas,
            correctas=correctas,
            porcentaje=round(porcentaje, 2),
            observaciones=observaciones
        )
        
        resultado = await reportes_collection.insert_one(nuevo_reporte.dict(by_alias=True))
        reporte_creado = await reportes_collection.find_one({"_id": resultado.inserted_id})
        
        reporte_creado["_id"] = str(reporte_creado["_id"])
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

@app.get("/reportes/{alumno_id}", response_model=Dict[str, Any])
async def obtener_reportes_alumno(alumno_id: str):
    """Obtiene todos los reportes de un alumno"""
    try:
        if not ObjectId.is_valid(alumno_id):
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        reportes = await reportes_collection.find(
            {"alumno_id": ObjectId(alumno_id)}
        ).sort("fecha", -1).to_list(100)
        
        for reporte in reportes:
            reporte["_id"] = str(reporte["_id"])
            reporte["alumno_id"] = str(reporte["alumno_id"])
            reporte["tema_id"] = str(reporte["tema_id"])
        
        return {
            "reportes": reportes,
            "total": len(reportes)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========================
# ENDPOINTS DE ANÁLISIS Y PATRONES
# ========================

@app.post("/analisis/patrones", response_model=Dict[str, Any])
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
        
        if not ObjectId.is_valid(alumno_id):
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        # Construir filtro
        filtro = {"alumno_id": ObjectId(alumno_id)}
        if tema_id and ObjectId.is_valid(tema_id):
            filtro["tema_id"] = ObjectId(tema_id)
        
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

@app.post("/ejercicios/personalizados", response_model=Dict[str, Any])
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
        
        if not ObjectId.is_valid(alumno_id):
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        if not tema:
            raise HTTPException(status_code=400, detail="Se requiere especificar el tema")
        
        ejercicios = await gpt_service.generar_ejercicios_personalizados(
            alumno_id, tema, dificultades
        )
        
        return {
            "status": "Ejercicios personalizados generados",
            "tema": tema,
            "ejercicios": ejercicios
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========================
# ENDPOINTS DE EJERCICIOS ADICIONALES
# ========================

@app.post("/ejercicios/adicionales", response_model=Dict[str, Any])
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
        
        # Generar ejercicios adicionales
        ejercicios_adicionales = await gpt_service.generar_ejercicios_adicionales(
            tema, nivel, cantidad, alumno_id
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

# ========================
# ENDPOINTS DE INFORMACIÓN
# ========================

@app.get("/temas", response_model=Dict[str, Any])
async def listar_temas():
    """Lista todos los temas disponibles"""
    try:
        temas = await temas_collection.find({}, {"nombre": 1, "descripcion": 1}).to_list(100)
        for tema in temas:
            tema["_id"] = str(tema["_id"])
        
        return {
            "temas": temas,
            "total": len(temas)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estadisticas/{alumno_id}", response_model=Dict[str, Any])
async def obtener_estadisticas_alumno(alumno_id: str):
    """Obtiene estadísticas generales de un alumno"""
    try:
        if not ObjectId.is_valid(alumno_id):
            raise HTTPException(status_code=400, detail="ID de alumno inválido")
        
        # Obtener todos los progresos del alumno
        progresos = await progresos_collection.find(
            {"alumno_id": ObjectId(alumno_id)}
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
            {"alumno_id": ObjectId(alumno_id)}
        ).to_list(100)
        
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

@app.get("/health")
async def health_check():
    """Endpoint de salud de la API"""
    return {"status": "OK", "timestamp": datetime.utcnow()}

