import json

def validar_credenciales(usuario: str, contraseña: str) -> bool:
    try:
        with open("data/credenciales.json", "r") as f:
            credenciales = json.load(f)
        return credenciales.get(usuario) == contraseña
    except Exception as e:
        print(f"⚠️ Error al validar credenciales: {e}")
        return False

import json
from datetime import datetime

def registrar_intento(usuario: str, exito: bool):
    entrada = {
        "usuario": usuario,
        "exito": exito,
        "timestamp": datetime.now().isoformat()
    }
    try:
        with open("logs.json", "r+") as f:
            logs = json.load(f)
            logs.append(entrada)
            f.seek(0)
            json.dump(logs, f, indent=2)
    except:
        with open("logs.json", "w") as f:
            json.dump([entrada], f, indent=2)
