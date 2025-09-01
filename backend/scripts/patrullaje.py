- import json
+ from utils.validar_json import cargar_json_seguro

- with open("backend/logs/patrullaje.json", "r", encoding="utf-8") as f:
-     data = json.load(f)

+ log_path = "backend/logs/patrullaje.json"
+ data = cargar_json_seguro(log_path)

if data is None:
    print("[!] Patrullaje abortado: JSON inválido.")
    exit(1)
