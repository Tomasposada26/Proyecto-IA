# Script para importar datasets CSV a entertainment_db.json
# Uso: python import_datasets.py

import csv
import json
import os

BASE_PATH = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_PATH, "entertainment_db.json")
DATASETS_PATH = os.path.join(BASE_PATH, "datasets")

# Configuración de archivos y campos por categoría
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
            "plataforma": "Platform"
        }
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
            "director": "Dirección"
        }
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
            "autor": "authors"
        }
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
            "artista": "artist(s)_name"
        }
    }
}

def parse_tags(value):
    if not value:
        return []
    if "," in value:
        return [v.strip() for v in value.split(",") if v.strip()]
    if ";" in value:
        return [v.strip() for v in value.split(";") if v.strip()]
    return [value.strip()]

def import_category(cat, conf):
    path = os.path.join(DATASETS_PATH, conf["csv"])
    items = []
    if not os.path.exists(path):
        print(f"[ERROR] No se encontró el archivo {path}")
        return items
    import random
    GENEROS_COMUNES = ["acción", "aventura", "deportes", "estrategia", "ficción", "drama", "comedia", "fantasía", "terror", "romance", "misterio", "musical", "historia", "ciencia ficción"]
    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                print(f"[ADVERTENCIA] El archivo {path} está vacío o no tiene datos.")
            for row in rows:
                item = {}
                for k, v in conf["fields"].items():
                    if v == "":
                        item[k] = ""
                    elif k == "tags":
                        item[k] = parse_tags(row.get(v, ""))
                    elif k == "calificacion":
                        # Asignar calificación aleatoria entre 2.4 y 5.0
                        item[k] = round(random.uniform(2.4, 5.0), 2)
                    else:
                        item[k] = row.get(v, "")
                # Normalizar género/reseña
                genero = (item.get("reseña", "") or "").lower()
                genero_final = []
                for g in GENEROS_COMUNES:
                    if g in genero:
                        genero_final.append(g.capitalize())
                if not genero_final and genero:
                    genero_final = [genero.capitalize()]
                item["reseña"] = ", ".join(genero_final) if genero_final else "N/A"
                # Asignar número aleatorio de reseñas
                item["num_reseñas"] = random.randint(10, 5000)
                # Solo agregar si el campo principal 'nombre' no está vacío
                if item.get("nombre", "").strip():
                    items.append(item)
    except UnicodeDecodeError:
        print(f"[ADVERTENCIA] {path} no es UTF-8, intentando con latin-1...")
        import random
        GENEROS_COMUNES = ["acción", "aventura", "deportes", "estrategia", "ficción", "drama", "comedia", "fantasía", "terror", "romance", "misterio", "musical", "historia", "ciencia ficción"]
        with open(path, encoding="latin-1") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                print(f"[ADVERTENCIA] El archivo {path} está vacío o no tiene datos.")
            for row in rows:
                item = {}
                for k, v in conf["fields"].items():
                    if v == "":
                        item[k] = ""
                    elif k == "tags":
                        item[k] = parse_tags(row.get(v, ""))
                    elif k == "calificacion":
                        item[k] = round(random.uniform(2.4, 5.0), 2)
                    else:
                        item[k] = row.get(v, "")
                genero = (item.get("reseña", "") or "").lower()
                genero_final = []
                for g in GENEROS_COMUNES:
                    if g in genero:
                        genero_final.append(g.capitalize())
                if not genero_final and genero:
                    genero_final = [genero.capitalize()]
                item["reseña"] = ", ".join(genero_final) if genero_final else "N/A"
                item["num_reseñas"] = random.randint(10, 5000)
                if item.get("nombre", "").strip():
                    items.append(item)
    print(f"[INFO] {cat}: {len(items)} elementos importados.")
    return items

def main():
    db = {"videojuegos": [], "peliculas": [], "libros": [], "musica": []}
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
