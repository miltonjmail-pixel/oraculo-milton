from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Middleware CORS para permitir acceso desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto si lo deseas
    allow_methods=["*"],
    allow_headers=["*"],
)

# Token secreto para proteger el endpoint
TOKEN_SECRETO = "oraculo-privado-2025"

# Ruta protegida para obtener hallazgos
@app.get("/hallazgos")
async def obtener_hallazgos(request: Request):
    token = request.headers.get("Authorization")
    if token != f"Bearer {TOKEN_SECRETO}":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    ruta_archivo = os.path.join(os.path.dirname(__file__), "hallazgos.json")
    if not os.path.exists(ruta_archivo):
        raise HTTPException(status_code=404, detail="Archivo de hallazgos no encontrado")

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer hallazgos: {str(e)}")

# Ruta raíz opcional para verificar que el backend está activo
@app.get("/")
def root():
    return {"status": "oráculo activo", "versión": "1.0.0"}
