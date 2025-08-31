from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json, time, hashlib, asyncio
from datetime import datetime

app = FastAPI()

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔁 Patrullaje activo
patrullaje_activo = True

# 🔄 Ciclo de patrullaje
async def patrullar():
    zonas = ["Nodo 3", "Nodo 7", "Nodo 12"]
    while patrullaje_activo:
        for zona in zonas:
            evento = detectar_evento(zona)
            if evento:
                hallazgo = registrar_hallazgo(zona, evento, "Alta", "patrullaje.py")
                await emitir_evento(hallazgo)
        await asyncio.sleep(10)

# 🧠 Detección real (puedes conectar sensores o APIs aquí)
def detectar_evento(zona):
    # Aquí puedes usar lógica real: sensores, APIs, etc.
    return "Token detectado"  # Solo si es real

# 📝 Registro con hash y trazabilidad
def registrar_hallazgo(zona, evento, prioridad, origen):
    timestamp = datetime.utcnow().isoformat()
    raw = f"{timestamp}-{zona}-{evento}"
    hash_id = hashlib.sha256(raw.encode()).hexdigest()[:12]
    nuevo = {
        "id": f"HX-{timestamp[:10].replace('-', '')}-{hash_id}",
        "timestamp": timestamp,
        "zona": zona,
        "evento": evento,
        "prioridad": prioridad,
        "origen": origen,
        "hash": hash_id
    }

    ruta = "backend/hallazgos.json"
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except:
        datos = []

    datos.append(nuevo)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2)

    return nuevo

# 📡 Emisión SSE al frontend
async def evento_generator():
    global eventos_sse
    eventos_sse = asyncio.Queue()
    while True:
        evento = await eventos_sse.get()
        yield f"data: {json.dumps(evento)}\n\n"

async def emitir_evento(evento):
    await eventos_sse.put(evento)

@app.get("/stream")
async def stream():
    return StreamingResponse(evento_generator(), media_type="text/event-stream")

# 🚀 Activar patrullaje desde frontend
@app.post("/iniciar-patrullaje")
async def iniciar(background_tasks: BackgroundTasks):
    background_tasks.add_task(patrullar)
    return {"status": "Patrullaje iniciado"}

# 🧪 Endpoint de prueba
@app.get("/")
def root():
    return {"status": "Sistema oracular activo"}
