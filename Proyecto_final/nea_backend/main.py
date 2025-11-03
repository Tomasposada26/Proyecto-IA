from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "entertainment_db.json")


class UserPreferences(BaseModel):
    categoria: str
    gustos: List[str]

class SearchQuery(BaseModel):
    categoria: str
    query: str



@app.post("/recomendar")
def recomendar(preferencias: UserPreferences):
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    items = db.get(preferencias.categoria, [])
    recomendaciones = []
    for item in items:
        if any(g.lower() in item.get("tags", []) for g in preferencias.gustos):
            recomendaciones.append(item)
    if not recomendaciones:
        recomendaciones = items[:3]  # fallback
    return {"recomendaciones": recomendaciones}



# Endpoint para top 10 de la categoría (por calificación)
@app.get("/top10/{categoria}")
def top10_categoria(categoria: str):
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    items = db.get(categoria, [])
    # Ordenar por calificación descendente
    items_sorted = sorted(items, key=lambda x: x.get("calificacion", 0), reverse=True)
    return {"top10": items_sorted[:10]}

# Endpoint para búsqueda detallada por título, autor u obra
@app.post("/buscar")
def buscar_detallado(query: SearchQuery):
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    items = db.get(query.categoria, [])
    resultados = []
    q = query.query.lower()
    for item in items:
        if (
            q in item.get("nombre", "").lower()
            or q in item.get("autor", "").lower()
            or q in item.get("titulo", "").lower()
        ):
            resultados.append(item)
    return {"resultados": resultados}

@app.get("/categorias")
def categorias():
    return {"categorias": ["videojuegos", "peliculas", "libros", "musica", "series"]}