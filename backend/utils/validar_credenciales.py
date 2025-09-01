import json

def validar_credenciales(usuario: str, contraseña: str) -> bool:
    try:
        with open("data/credenciales.json", "r") as f:
            credenciales = json.load(f)
        return credenciales.get(usuario) == contraseña
    except Exception as e:
        print(f"⚠️ Error al validar credenciales: {e}")
        return False
