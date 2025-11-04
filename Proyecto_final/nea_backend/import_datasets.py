"""Script for importing CSV datasets into entertainment_db.json.

This script reads several CSV files corresponding to different categories
(videojuegos, peliculas, libros, musica) and converts them into a single JSON
database used by the NEA recommender.  Each category has a configuration that
maps the desired fields to columns in the CSV.  If a particular CSV file
includes no rating column, the script assigns a random rating between 2.4 and
5.0 as a placeholder.  You can customise the CONFIG dictionary below to
support alternative datasets or new categories.

Usage:
    python import_datasets.py
"""


import csv
import json
import os
import random
from typing import List, Dict

BASE_PATH = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_PATH, "entertainment_db.json")
DATASETS_PATH = os.path.join(BASE_PATH, "datasets")

# Configuration of files and fields per category.  You can modify the
# ``csv`` filenames to point to more recent datasets (e.g. movies_dataset.csv,
# goodreads_books_100k.csv, spotify_metrics_2024.csv) and update the field
# mappings accordingly.  Leave a value empty ("") to set the field to an
# empty string.
CONFIG = {
    "videojuegos": {
        "csv": "vgsales.csv",
        "fields": {
            "nombre": "Name",
            "calificacion": "User_Score",
            "reseña": "Genre",
            "sinopsis": "",
            "tags": "Genre",
            "link": "",
            "plataforma": "Platform",
        },
    },
    "peliculas": {
        "csv": "filmaffinity_dataset.csv",
        "fields": {
            "nombre": "Título",
            "calificacion": "Nota",
            "reseña": "Género",
            "sinopsis": "",
            "tags": "Género",
            "link": "",
            "director": "Dirección",
        },
    },
    "libros": {
        "csv": "books.csv",
        "fields": {
            "nombre": "title",
            "calificacion": "average_rating",
            "reseña": "description",
            "sinopsis": "description",
            "tags": "genres",
            "link": "url",
            "autor": "authors",
        },
    },
    "musica": {
        "csv": "Spotify_songs.csv",
        "fields": {
            "nombre": "track_name",
            "calificacion": "streams",
            "reseña": "artist(s)_name",
            "sinopsis": "",
            "tags": "artist(s)_name",
            "link": "cover_url",
            "artista": "artist(s)_name",
        },
    },
}


def parse_tags(value: str) -> List[str]:
    """Split a tag string into a list."""
    if not value:
        return []
    for sep in [",", ";"]:
        if sep in value:
            return [v.strip() for v in value.split(sep) if v.strip()]
    return [value.strip()]


def import_category(cat: str, conf: Dict) -> List[Dict]:
    """Import a single category from its CSV file."""
    path = os.path.join(DATASETS_PATH, conf["csv"])
    items: List[Dict] = []
    if not os.path.exists(path):
        print(f"[ERROR] No se encontró el archivo {path}")
        return items
    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                print(f"[ADVERTENCIA] El archivo {path} está vacío o no tiene datos.")
            for row in rows:
                item: Dict = {}
                for k, v in conf["fields"].items():
                    if v == "":
                        item[k] = ""
                    elif k == "tags":
                        item[k] = parse_tags(row.get(v, ""))
                    elif k == "calificacion":
                        # Use provided rating if available; otherwise assign random between 2.4 and 5.0
                        try:
                            rating_str = row.get(v, "")
                            item[k] = float(rating_str) if rating_str else round(random.uniform(2.4, 5.0), 2)
                        except ValueError:
                            item[k] = round(random.uniform(2.4, 5.0), 2)
                    else:
                        item[k] = row.get(v, "")
                # Normalize the genre/reseña field
                genero_raw = (item.get("reseña", "") or "").lower()
                GENEROS_COMUNES = [
                    "acción",
                    "aventura",
                    "deportes",
                    "estrategia",
                    "ficción",
                    "drama",
                    "comedia",
                    "fantasía",
                    "terror",
                    "romance",
                    "misterio",
                    "musical",
                    "historia",
                    "ciencia ficción",
                ]
                genero_final: List[str] = []
                for g in GENEROS_COMUNES:
                    if g in genero_raw:
                        genero_final.append(g.capitalize())
                if not genero_final and genero_raw:
                    genero_final = [genero_raw.capitalize()]
                item["reseña"] = ", ".join(genero_final) if genero_final else "N/A"
                # Assign a random number of reviews to simulate popularity
                item["num_reseñas"] = random.randint(10, 5000)
                if item.get("nombre", "").strip():
                    items.append(item)
    except UnicodeDecodeError:
        print(f"[ADVERTENCIA] {path} no es UTF-8, intentando con latin-1...")
        with open(path, encoding="latin-1") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                print(f"[ADVERTENCIA] El archivo {path} está vacío o no tiene datos.")
            for row in rows:
                item: Dict = {}
                for k, v in conf["fields"].items():
                    if v == "":
                        item[k] = ""
                    elif k == "tags":
                        item[k] = parse_tags(row.get(v, ""))
                    elif k == "calificacion":
                        try:
                            rating_str = row.get(v, "")
                            item[k] = float(rating_str) if rating_str else round(random.uniform(2.4, 5.0), 2)
                        except ValueError:
                            item[k] = round(random.uniform(2.4, 5.0), 2)
                    else:
                        item[k] = row.get(v, "")
                genero_raw = (item.get("reseña", "") or "").lower()
                GENEROS_COMUNES = [
                    "acción",
                    "aventura",
                    "deportes",
                    "estrategia",
                    "ficción",
                    "drama",
                    "comedia",
                    "fantasía",
                    "terror",
                    "romance",
                    "misterio",
                    "musical",
                    "historia",
                    "ciencia ficción",
                ]
                genero_final: List[str] = []
                for g in GENEROS_COMUNES:
                    if g in genero_raw:
                        genero_final.append(g.capitalize())
                if not genero_final and genero_raw:
                    genero_final = [genero_raw.capitalize()]
                item["reseña"] = ", ".join(genero_final) if genero_final else "N/A"
                item["num_reseñas"] = random.randint(10, 5000)
                if item.get("nombre", "").strip():
                    items.append(item)
    print(f"[INFO] {cat}: {len(items)} elementos importados.")
    return items


def main() -> None:
    """Main function to import all categories and write to JSON."""
    db: Dict[str, List[Dict]] = {cat: [] for cat in CONFIG.keys()}
    for cat, conf in CONFIG.items():
        print(f"Importando {cat}...")
        db[cat] = import_category(cat, conf)
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"[OK] Base de datos guardada en {DB_PATH}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo JSON: {e}")
    print("¡Importación completada!")


if __name__ == "__main__":
    main()