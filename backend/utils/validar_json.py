import json
import os

def cargar_json_seguro(path):
    """
    Carga un archivo JSON validando su estructura.
    Si hay error de formato, lo reporta con precisión.
    """
    if not os.path.exists(path):
        print(f"[✗] Archivo no encontrado: {path}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[✓] JSON cargado correctamente desde: {path}")
        return data

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON malformado en {path}")
        print(f"↳ Línea: {e.lineno}, Columna: {e.colno}, Posición: {e.pos}")
        print(f"↳ Detalle: {e.msg}")
        return None

    except Exception as e:
        print(f"[ERROR] Fallo inesperado al cargar {path}: {e}")
        return None
