
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_PATH = os.path.join(os.path.dirname(__file__), "entertainment_db.json")
DATASET_PATHS = {
    "musica": os.path.join(os.path.dirname(__file__), "datasets", "Spotify_songs.csv"),
    "peliculas": os.path.join(os.path.dirname(__file__), "datasets", "filmaffinity_dataset.csv"),
    "libros": os.path.join(os.path.dirname(__file__), "datasets", "books.csv"),
    "videojuegos": os.path.join(os.path.dirname(__file__), "datasets", "vgsales.csv"),
}


class UserPreferences(BaseModel):
    categoria: str
    gustos: List[str]

class SearchQuery(BaseModel):
    categoria: str
    query: str
    filtros: Optional[dict] = None  # Para búsquedas avanzadas por campo



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

# Utilidad para buscar en CSV por cualquier campo relevante
def buscar_en_csv(categoria, query, filtros=None):
    path = DATASET_PATHS.get(categoria)
    if not path or not os.path.exists(path):
        return []
    resultados = []
    q = (query or "").lower()
    # Definir los campos relevantes por categoría
    campos_categoria = {
        "musica": ["track_name", "artist(s)_name", "released_year", "bpm", "key", "mode", "danceability_%", "valence_%", "energy_%", "acousticness_%", "instrumentalness_%", "liveness_%", "speechiness_%", "streams", "genre", "reseña", "tags"],
        "videojuegos": ["Name", "Platform", "Year", "Genre"],
        "peliculas": ["Título", "Año", "Género", "Tipo filme", "Dirección", "Reparto"],
        "libros": ["title", "authors", "publication_date", "average_rating", "genres", "author", "isbn", "language_code"],
    }
    campos_filtro = {
        "musica": {"año": "released_year", "artista": "artist(s)_name", "genero": "genre"},
        "videojuegos": {"año": "Year", "genero": "Genre", "plataforma": "Platform"},
        "peliculas": {"año": "Año", "genero": "Género"},
        "libros": {"año": "publication_date", "genero": "genres", "autor": "authors"},
    }
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            valores = []
            for campo in campos_categoria.get(categoria, []):
                if campo in row and row[campo]:
                    valores.append(str(row[campo]).lower())
            # Coincidencia: si hay query, debe estar en algún campo relevante; si hay filtros, deben cumplirse todos
            match_query = True
            if q:
                match_query = any(q in v for v in valores)
            match_filtros = True
            if filtros:
                for filtro, valor in filtros.items():
                    if valor:
                        campo_csv = campos_filtro.get(categoria, {}).get(filtro)
                        if campo_csv and campo_csv in row:
                            # Comparación exacta para released_year en música
                            if categoria == "musica" and filtro == "año":
                                if str(row[campo_csv]).strip() != str(valor).strip():
                                    match_filtros = False
                                    break
                            else:
                                if str(valor).lower() not in str(row[campo_csv]).lower():
                                    match_filtros = False
                                    break
            if match_query and match_filtros:
                # Normalizar para frontend: solo los campos relevantes
                if categoria == "musica":
                    resultados.append({
                        "nombre": row.get("track_name", ""),
                        "artista": row.get("artist(s)_name", ""),
                        "año": row.get("released_year", ""),
                        "streams": row.get("streams", ""),
                        "cover_url": row.get("cover_url", ""),
                    })
                else:
                    resultados.append(row)
    return resultados

@app.post("/buscar")
def buscar_detallado(query: SearchQuery):
    # Si la categoría tiene dataset CSV, buscar ahí
    if query.categoria in DATASET_PATHS:
        resultados = buscar_en_csv(query.categoria, query.query, query.filtros)
        return {"resultados": resultados}
    # Fallback: buscar en el JSON
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
    items = db.get(query.categoria, [])
    resultados = []
    q = query.query.lower()
    for item in items:
        campos = [str(v).lower() for v in item.values() if v is not None]
        if q in " ".join(campos):
            resultados.append(item)
    return {"resultados": resultados}

@app.get("/categorias")
def categorias():
    return {"categorias": ["videojuegos", "peliculas", "libros", "musica", "series"]}