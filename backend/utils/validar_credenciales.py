import json

def validar_credenciales(usuario: str, contraseña: str) -> bool:
    with open("data/credenciales.json", "r") as f:
        credenciales = json.load(f)
    return credenciales.get(usuario) == contraseña
