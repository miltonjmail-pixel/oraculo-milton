import json
import os
from datetime import datetime

# Rutas absolutas relativas al proyecto
RUTA_CREDENCIALES = os.path.join(os.path.dirname(__file__), "..", "data", "credenciales.json")
RUTA_LOGS = os.path.join(os.path.dirname(__file__), "..", "logs.json")

def validar_credenciales(usuario: str, contraseña: str) -> bool:
    try:
        with open(RUTA_CREDENCIALES, "r", encoding="utf-8") as f:
            credenciales = json.load(f)
        return credenciales.get(usuario) == contraseña
    except Exception as e:
        print(f"⚠️ Error al validar credenciales: {e}")
        return False

def registrar_intento(usuario: str, exito: bool):
    entrada = {
        "usuario": usuario,
        "exito": exito,
        "timestamp": datetime.now().isoformat()
    }
    try:
        if os.path.exists(RUTA_LOGS):
            with open(RUTA_LOGS, "r+", encoding="utf-8") as f:
                logs = json.load(f)
                logs.append(entrada)
                f.seek(0)
                json.dump(logs, f, indent=2)
        else:
            with open(RUTA_LOGS, "w", encoding="utf-8") as f:
                json.dump([entrada], f, indent=2)
    except Exception as e:
        print(f"⚠️ Error al registrar intento: {e}")
