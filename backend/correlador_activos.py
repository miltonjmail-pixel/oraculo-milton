import json
import os
from datetime import datetime

# Rutas
HALLAZGOS_PATH = "backend/hallazgos.json"
ACTIVOS_PATH = "backend/data/activos.json"
DETECTADOS_PATH = "backend/data/activos_detectados.json"

# Cargar hallazgos
with open(HALLAZGOS_PATH, "r") as f:
    hallazgos = json.load(f)

# Cargar activos
with open(ACTIVOS_PATH, "r") as f:
    activos = json.load(f)

# Índice por hash
activos_por_hash = {a["hash"]: a for a in activos}

# Detectados
detectados = []

for h in hallazgos:
    hash_hallazgo = h.get("hash")
    if hash_hallazgo in activos_por_hash:
        activo = activos_por_hash[hash_hallazgo]
        detectado = {
            "timestamp": datetime.utcnow().isoformat(),
            "hallazgo_id": h["id"],
            "zona": h["zona"],
            "tipo_activo": activo["tipo"],
            "estado": activo["estado"],
            "saldo": activo.get("saldo", 0),
            "moneda": activo.get("moneda", "N/A"),
            "hash": hash_hallazgo,
            "origen": h["origen"]
        }
        detectados.append(detectado)

# Guardar resultados
os.makedirs(os.path.dirname(DETECTADOS_PATH), exist_ok=True)
with open(DETECTADOS_PATH, "w") as f:
    json.dump(detectados, f, indent=2)

print(f"[✓] {len(detectados)} activos detectados correlacionados con hallazgos.")
