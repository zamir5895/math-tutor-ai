from datetime import datetime
from db.db import mongo
from collections import defaultdict

class StatsAlumnoService:

    def __init__(self):
        pass

    @staticmethod
    async def procesar_estadistica_init(data: dict):
        db = mongo.db
        alumno_stats = await db.alumnos.find_one({"alumno_id": data["alumno_id"]})
        if not alumno_stats:
            documento_inicial = {
                "alumno_id": data["alumno_id"],
                "progreso_general": {
                    "correctos": 0,
                    "errores": 0,
                    "completados": 0,
                    "total": sum(data["ejercicios_por_nivel"].values()),
                    "porcentaje": 0.0
                },
                "temas": [],
                "updated_at": datetime.utcnow()
            }
            await db.alumnos.insert_one(documento_inicial)
            alumno_stats = documento_inicial

        tema_existente = next(
            (t for t in alumno_stats["temas"] if t["tema_id"] == data["tema_id"]),
            None
        )

        if not tema_existente:
            nuevo_tema = {
                "tema_id": data["tema_id"],
                "correctos": 0,
                "errores": 0,
                "total": sum(data["ejercicios_por_nivel"].values()),
                "subtemas": []
            }
            await db.alumnos.update_one(
                {"alumno_id": data["alumno_id"]},
                {"$push": {"temas": nuevo_tema}}
            )

        subtema_existente = next(
            (s for s in tema_existente["subtemas"] if s["subtema_id"] == data["subtema_id"]),
            None
        ) if tema_existente else None

        if not subtema_existente:
            nuevo_subtema = {
                "subtema_id": data["subtema_id"],
                "correctos": 0,
                "errores": 0,
                "total": sum(data["ejercicios_por_nivel"].values()),
                "niveles": {
                    nivel: {"correctos": 0, "errores": 0, "total": total}
                    for nivel, total in data["ejercicios_por_nivel"].items()
                }
            }
            ejercicios_nuevo = nuevo_subtema["total"]
            await db.alumnos.update_one(
                {"alumno_id": data["alumno_id"], "temas.tema_id": data["tema_id"]},
                {"$push": {"temas.$.subtemas": nuevo_subtema}}
            )
            await db.alumnos.update_one(
                    {"alumno_id": data["alumno_id"], "temas.tema_id": data["tema_id"]},
                    {
                        "$inc": {
                            "temas.$.total": ejercicios_nuevo,
                            "progreso_general.total": ejercicios_nuevo
                        }
                    }
                )
    
    @staticmethod
    async def procesar_progreso_event(event: dict):
        db = mongo.db
    
        if event["es_correcto"]:
            update = [
                {
                    "$set": {
                        "progreso_general.correctos": {"$add": ["$progreso_general.correctos", 1]},
                        "progreso_general.completados": {"$add": ["$progreso_general.completados", 1]},
                        "progreso_general.errores": {
                            "$cond": [
                                {"$gt": ["$progreso_general.errores", 0]},
                                {"$subtract": ["$progreso_general.errores", 1]},
                                0
                            ]
                        },
                        "temas": {
                            "$map": {
                                "input": "$temas",
                                "as": "tema",
                                "in": {
                                    "$mergeObjects": [
                                        "$$tema",
                                        {
                                            "correctos": {
                                                "$cond": [
                                                    {"$eq": ["$$tema.tema_id", event["tema_id"]]},
                                                    {"$add": ["$$tema.correctos", 1]},
                                                    "$$tema.correctos"
                                                ]
                                            },
                                            "errores": {
                                                "$cond": [
                                                    {"$and": [
                                                        {"$eq": ["$$tema.tema_id", event["tema_id"]]},
                                                        {"$gt": ["$$tema.errores", 0]}
                                                    ]},
                                                    {"$subtract": ["$$tema.errores", 1]},
                                                    "$$tema.errores"
                                                ]
                                            },
                                            "subtemas": {
                                                "$map": {
                                                    "input": "$$tema.subtemas",
                                                    "as": "subtema",
                                                    "in": {
                                                        "$mergeObjects": [
                                                            "$$subtema",
                                                            {
                                                                "correctos": {
                                                                    "$cond": [
                                                                        {"$eq": ["$$subtema.subtema_id", event["subtema_id"]]},
                                                                        {"$add": ["$$subtema.correctos", 1]},
                                                                        "$$subtema.correctos"
                                                                    ]
                                                                },
                                                                "errores": {
                                                                    "$cond": [
                                                                        {"$and": [
                                                                            {"$eq": ["$$subtema.subtema_id", event["subtema_id"]]},
                                                                            {"$gt": ["$$subtema.errores", 0]}
                                                                        ]},
                                                                        {"$subtract": ["$$subtema.errores", 1]},
                                                                        "$$subtema.errores"
                                                                    ]
                                                                },
                                                               "niveles": {
                                                                    event["nivel"]: {
                                                                        "correctos": {
                                                                            "$add": [
                                                                                "$$subtema.niveles." + event["nivel"] + ".correctos",
                                                                                1
                                                                            ]
                                                                        },
                                                                        "errores": {
                                                                            "$cond": [
                                                                                {"$gt": ["$$subtema.niveles." + event["nivel"] + ".errores", 0]},
                                                                                {"$subtract": [
                                                                                    "$$subtema.niveles." + event["nivel"] + ".errores",
                                                                                    1
                                                                                ]},
                                                                                "$$subtema.niveles." + event["nivel"] + ".errores"
                                                                            ]
                                                                        },
                                                                        "total": "$$subtema.niveles." + event["nivel"] + ".total"
                                                                    }
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        },
                        "updated_at": datetime.utcnow()
                    }
                }
            ]
            await db.alumnos.update_one(
                {"alumno_id": event["alumno_id"]},
                update
            )
        else:
            update = {
                "$inc": {
                    "progreso_general.errores": 1,
                    "progreso_general.completados": 1,
                    "temas.$[t].errores": 1,
                    "temas.$[t].subtemas.$[s].errores": 1,
                    f"temas.$[t].subtemas.$[s].niveles.{event['nivel']}.errores": 1
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
            await db.alumnos.update_one(
                {"alumno_id": event["alumno_id"]},
                update,
                array_filters=[
                    {"t.tema_id": event["tema_id"]},
                    {"s.subtema_id": event["subtema_id"]}
                ]
            )
        doc = await db.alumnos.find_one({"alumno_id": event["alumno_id"]})
        if doc:
            correctos = doc["progreso_general"]["correctos"]
            total = doc["progreso_general"]["total"]
            porcentaje = (correctos / total) * 100 if total > 0 else 0
            await db.alumnos.update_one(
                {"alumno_id": event["alumno_id"]},
                {"$set": {"progreso_general.porcentaje": porcentaje}}
                
            )
            await StatsAlumnoService.actualizar_temas_dominados_alumno(event["alumno_id"])
            await StatsAlumnoService.actualizar_subtemas_dominados_alumno(event["alumno_id"])
            salon_id = doc.get("salon_id")
            if salon_id:
                await StatsAlumnoService.actualizar_temas_dominados_salon(salon_id)
                await StatsAlumnoService.actualizar_subtemas_dominados_salon(salon_id)

    @staticmethod
    async def obtener_por_tema_id(alumno_id: str, tema_id: str):
        db = mongo.db
        doc = await db.alumnos.find_one(
            {"alumno_id": alumno_id, "temas.tema_id": tema_id},
            {"temas.$": 1, "_id": 0}
        )
        return doc["temas"][0] if doc and "temas" in doc and doc["temas"] else None


    @staticmethod
    async def obtener_por_subtema_id(alumno_id: str, tema_id: str, subtema_id: str):
        db = mongo.db
        doc = await db.alumnos.find_one(
            {"alumno_id": alumno_id, "temas.tema_id": tema_id, "temas.subtemas.subtema_id": subtema_id},
            {"temas.$": 1, "_id": 0}
        )
        if doc and "temas" in doc and doc["temas"]:
            subtemas = doc["temas"][0].get("subtemas", [])
            for subtema in subtemas:
                if subtema["subtema_id"] == subtema_id:
                    return subtema
        return None


    @staticmethod
    async def obtener_por_alumno_id(alumno_id: str):
        db = mongo.db
        doc = await db.alumnos.find_one({"alumno_id": alumno_id}, {"_id": 0})
        return doc


    @staticmethod
    async def obtener_por_subtema_y_nivel(alumno_id: str, tema_id: str, subtema_id: str, nivel: str):
        db = mongo.db
        doc = await db.alumnos.find_one(
            {"alumno_id": alumno_id, "temas.tema_id": tema_id, "temas.subtemas.subtema_id": subtema_id},
            {"temas.$": 1, "_id": 0}
        )
        if doc and "temas" in doc and doc["temas"]:
            subtemas = doc["temas"][0].get("subtemas", [])
            for subtema in subtemas:
                if subtema["subtema_id"] == subtema_id:
                    niveles = subtema.get("niveles", {})
                    return niveles.get(nivel)
        return None


    @staticmethod
    async def resumen_por_salon_id(salon_id: str):
        db = mongo.db
        alumnos = await db.alumnos.find({"salon_id": salon_id}).to_list(length=None)
        if not alumnos:
            return None

        resumen_temas = defaultdict(lambda: {
            "tema_id": None,
            "nombre": "",
            "total_correctos": 0,
            "total_errores": 0,
            "total": 0,
            "subtemas": defaultdict(lambda: {
                "subtema_id": None,
                "nombre": "",
                "total_correctos": 0,
                "total_errores": 0,
                "niveles": defaultdict(lambda: {
                    "nivel": "",
                    "total_correctos": 0,
                    "total_errores": 0,
                    "total": 0
                })
            })
        })

        for alumno in alumnos:
            for tema in alumno.get("temas", []):
                tema_id = tema["tema_id"]
                resumen_tema = resumen_temas[tema_id]
                resumen_tema["tema_id"] = tema_id
                resumen_tema["total_correctos"] += tema.get("correctos", 0)
                resumen_tema["total_errores"] += tema.get("errores", 0)
                resumen_tema["total"] += tema.get("total", 0)
                for subtema in tema.get("subtemas", []):
                    subtema_id = subtema["subtema_id"]
                    resumen_subtema = resumen_tema["subtemas"][subtema_id]
                    resumen_subtema["subtema_id"] = subtema_id
                    resumen_subtema["total_correctos"] += subtema.get("correctos", 0)
                    resumen_subtema["total_errores"] += subtema.get("errores", 0)
                    for nivel, stats in subtema.get("niveles", {}).items():
                        resumen_nivel = resumen_subtema["niveles"][nivel]
                        resumen_nivel["nivel"] = nivel
                        resumen_nivel["total_correctos"] += stats.get("correctos", 0)
                        resumen_nivel["total_errores"] += stats.get("errores", 0)
                        resumen_nivel["total"] += stats.get("total", 0)
        resumen_final = []
        for tema in resumen_temas.values():
            tema["subtemas"] = [dict(st, niveles=list(st["niveles"].values())) for st in tema["subtemas"].values()]
            resumen_final.append(tema)

        return {
            "salon_id": salon_id,
            "temas": resumen_final,
        }


    @staticmethod
    async def resumen_por_salon_y_tema(salon_id: str, tema_id: str):
        db = mongo.db
        alumnos = await db.alumnos.find({"salon_id": salon_id}).to_list(length=None)
        if not alumnos:
            return None

        resumen = {
            "tema_id": tema_id,
            "total_correctos": 0,
            "total_errores": 0,
            "total": 0,
            "subtemas": {}
        }

        for alumno in alumnos:
            for tema in alumno.get("temas", []):
                if tema["tema_id"] == tema_id:
                    resumen["total_correctos"] += tema.get("correctos", 0)
                    resumen["total_errores"] += tema.get("errores", 0)
                    resumen["total"] += tema.get("total", 0)
                    for subtema in tema.get("subtemas", []):
                        sid = subtema["subtema_id"]
                        if sid not in resumen["subtemas"]:
                            resumen["subtemas"][sid] = {
                                "subtema_id": sid,
                                "total_correctos": 0,
                                "total_errores": 0,
                                "niveles": {}
                            }
                        resumen["subtemas"][sid]["total_correctos"] += subtema.get("correctos", 0)
                        resumen["subtemas"][sid]["total_errores"] += subtema.get("errores", 0)
                        for nivel, stats in subtema.get("niveles", {}).items():
                            if nivel not in resumen["subtemas"][sid]["niveles"]:
                                resumen["subtemas"][sid]["niveles"][nivel] = {
                                    "nivel": nivel,
                                    "total_correctos": 0,
                                    "total_errores": 0,
                                    "total": 0
                                }
                            resumen["subtemas"][sid]["niveles"][nivel]["total_correctos"] += stats.get("correctos", 0)
                            resumen["subtemas"][sid]["niveles"][nivel]["total_errores"] += stats.get("errores", 0)
                            resumen["subtemas"][sid]["niveles"][nivel]["total"] += stats.get("total", 0)
        resumen["subtemas"] = [
            dict(st, niveles=list(st["niveles"].values()))
            for st in resumen["subtemas"].values()
        ]
        return resumen


    @staticmethod
    async def resumen_por_salon_tema_subtema(salon_id: str, tema_id: str, subtema_id: str):
        db = mongo.db
        alumnos = await db.alumnos.find({"salon_id": salon_id}).to_list(length=None)
        if not alumnos:
            return None

        resumen = {
            "subtema_id": subtema_id,
            "total_correctos": 0,
            "total_errores": 0,
            "niveles": {}
        }

        for alumno in alumnos:
            for tema in alumno.get("temas", []):
                if tema["tema_id"] == tema_id:
                    for subtema in tema.get("subtemas", []):
                        if subtema["subtema_id"] == subtema_id:
                            resumen["total_correctos"] += subtema.get("correctos", 0)
                            resumen["total_errores"] += subtema.get("errores", 0)
                            for nivel, stats in subtema.get("niveles", {}).items():
                                if nivel not in resumen["niveles"]:
                                    resumen["niveles"][nivel] = {
                                        "nivel": nivel,
                                        "total_correctos": 0,
                                        "total_errores": 0,
                                        "total": 0
                                    }
                                resumen["niveles"][nivel]["total_correctos"] += stats.get("correctos", 0)
                                resumen["niveles"][nivel]["total_errores"] += stats.get("errores", 0)
                                resumen["niveles"][nivel]["total"] += stats.get("total", 0)
        resumen["niveles"] = list(resumen["niveles"].values())
        return resumen


    @staticmethod
    async def resumen_por_salon_tema_subtema_nivel(salon_id: str, tema_id: str, subtema_id: str, nivel: str):
        db = mongo.db
        alumnos = await db.alumnos.find({"salon_id": salon_id}).to_list(length=None)
        if not alumnos:
            return None

        resumen = {
            "nivel": nivel,
            "total_correctos": 0,
            "total_errores": 0,
            "total": 0
        }

        for alumno in alumnos:
            for tema in alumno.get("temas", []):
                if tema["tema_id"] == tema_id:
                    for subtema in tema.get("subtemas", []):
                        if subtema["subtema_id"] == subtema_id:
                            stats = subtema.get("niveles", {}).get(nivel)
                            if stats:
                                resumen["total_correctos"] += stats.get("correctos", 0)
                                resumen["total_errores"] += stats.get("errores", 0)
                                resumen["total"] += stats.get("total", 0)
        return resumen
    

    @staticmethod
    async def actualizar_temas_dominados_alumno(alumno_id: str):
        db = mongo.db
        alumno = await db.alumnos.find_one({"alumno_id": alumno_id})
        if not alumno:
            return

        temas_dominados = []
        for tema in alumno.get("temas", []):
            subtemas_dominados = []
            for subtema in tema.get("subtemas", []):
                if subtema.get("correctos", 0) == subtema.get("total", 0) and subtema.get("total", 0) > 0:
                    subtemas_dominados.append(subtema["subtema_id"])
            if subtemas_dominados:
                temas_dominados.append({
                    "tema_id": tema["tema_id"],
                    "subtemas_dominados": subtemas_dominados
                })

        await db.temas_dominados_alumno.update_one(
            {"alumno_id": alumno_id},
            {"$set": {"temas_dominados": temas_dominados}},
            upsert=True
        )      
    

    @staticmethod
    async def actualizar_subtemas_dominados_alumno(alumno_id: str):
        db = mongo.db
        alumno = await db.alumnos.find_one({"alumno_id": alumno_id})
        if not alumno:
            return
    
        subtemas_dominados = []
        for tema in alumno.get("temas", []):
            for subtema in tema.get("subtemas", []):
                if subtema.get("correctos", 0) == subtema.get("total", 0) and subtema.get("total", 0) > 0:
                    subtemas_dominados.append({
                        "tema_id": tema["tema_id"],
                        "subtema_id": subtema["subtema_id"]
                    })
    
        await db.subtemas_dominados_alumno.update_one(
            {"alumno_id": alumno_id},
            {"$set": {"subtemas_dominados": subtemas_dominados}},
            upsert=True
        )


    @staticmethod
    async def actualizar_temas_dominados_salon(salon_id: str):
        db = mongo.db
        alumnos = await db.alumnos.find({"salon_id": salon_id}).to_list(length=None)
        if not alumnos:
            return
    
        if not alumnos:
            temas_dominados = []
        else:
            temas_ids = set(t["tema_id"] for a in alumnos for t in a.get("temas", []))
            temas_dominados = []
            for tema_id in temas_ids:
                todos_dominan = True
                for alumno in alumnos:
                    tema = next((t for t in alumno.get("temas", []) if t["tema_id"] == tema_id), None)
                    if not tema:
                        todos_dominan = False
                        break
                    for subtema in tema.get("subtemas", []):
                        if subtema.get("correctos", 0) < subtema.get("total", 0):
                            todos_dominan = False
                            break
                    if not todos_dominan:
                        break
                if todos_dominan:
                    temas_dominados.append(tema_id)
    
        await db.temas_dominados_salon.update_one(
            {"salon_id": salon_id},
            {"$set": {"temas_dominados": temas_dominados}},
            upsert=True
        )


    @staticmethod
    async def actualizar_subtemas_dominados_salon(salon_id: str):
        db = mongo.db
        alumnos = await db.alumnos.find({"salon_id": salon_id}).to_list(length=None)
        if not alumnos:
            return
    
        subtemas_ids = set(
            (t["tema_id"], s["subtema_id"])
            for a in alumnos
            for t in a.get("temas", [])
            for s in t.get("subtemas", [])
        )
        subtemas_dominados = []
        for tema_id, subtema_id in subtemas_ids:
            todos_dominan = True
            for alumno in alumnos:
                tema = next((t for t in alumno.get("temas", []) if t["tema_id"] == tema_id), None)
                if not tema:
                    todos_dominan = False
                    break
                subtema = next((s for s in tema.get("subtemas", []) if s["subtema_id"] == subtema_id), None)
                if not subtema or subtema.get("correctos", 0) < subtema.get("total", 0):
                    todos_dominan = False
                    break
            if todos_dominan:
                subtemas_dominados.append({"tema_id": tema_id, "subtema_id": subtema_id})
    
        await db.subtemas_dominados_salon.update_one(
            {"salon_id": salon_id},
            {"$set": {"subtemas_dominados": subtemas_dominados}},
            upsert=True
        )
    

    @staticmethod
    async def get_temas_dominados_alumno(alumno_id: str):
        db = mongo.db
        doc = await db.temas_dominados_alumno.find_one({"alumno_id": alumno_id}, {"_id": 0})
        return doc["temas_dominados"] if doc else []
    

    @staticmethod
    async def get_subtemas_dominados_alumno(alumno_id: str):
        db = mongo.db
        doc = await db.subtemas_dominados_alumno.find_one({"alumno_id": alumno_id}, {"_id": 0})
        return doc["subtemas_dominados"] if doc else []
    
    @staticmethod
    async def get_temas_dominados_salon(salon_id: str):
        db = mongo.db
        doc = await db.temas_dominados_salon.find_one({"salon_id": salon_id}, {"_id": 0})
        return doc["temas_dominados"] if doc else []


    @staticmethod
    async def get_subtemas_dominados_salon(salon_id: str):
        db = mongo.db
        doc = await db.subtemas_dominados_salon.find_one({"salon_id": salon_id}, {"_id": 0})
        return doc["subtemas_dominados"] if doc else []
    
    @staticmethod
    async def eliminar_tema_dominado_alumno(alumno_id: str, tema_id: str):
        db = mongo.db
        await db.temas_dominados_alumno.update_one(
            {"alumno_id": alumno_id},
            {"$pull": {"temas_dominados": {"tema_id": tema_id}}}
        )
    
    @staticmethod
    async def eliminar_subtema_dominado_alumno(alumno_id: str, tema_id: str, subtema_id: str):
        db = mongo.db
        await db.subtemas_dominados_alumno.update_one(
            {"alumno_id": alumno_id},
            {"$pull": {"subtemas_dominados": {"tema_id": tema_id, "subtema_id": subtema_id}}}
        )
    
    @staticmethod
    async def eliminar_tema_dominado_salon(salon_id: str, tema_id: str):
        db = mongo.db
        await db.temas_dominados_salon.update_one(
            {"salon_id": salon_id},
            {"$pull": {"temas_dominados": tema_id}}
        )

    @staticmethod
    async def eliminar_subtema_dominado_salon(salon_id: str, tema_id: str, subtema_id: str):
        db = mongo.db
        await db.subtemas_dominados_salon.update_one(
            {"salon_id": salon_id},
            {"$pull": {"subtemas_dominados": {"tema_id": tema_id, "subtema_id": subtema_id}}}
        )