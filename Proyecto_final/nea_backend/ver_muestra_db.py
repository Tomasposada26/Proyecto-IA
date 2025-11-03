import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "entertainment_db.json")

with open(DB_PATH, "r", encoding="utf-8") as f:
    db = json.load(f)

for categoria in db:
    print(f"{categoria}: {len(db[categoria])} elementos")
    print("Primer elemento:")
    if db[categoria]:
        print(json.dumps(db[categoria][0], ensure_ascii=False, indent=2))
    print("-")
