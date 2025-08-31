from fastapi import FastAPI, Request, BackgroundTasks, Form
from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import json, time, hashlib, asyncio
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

patrullaje_activo = False
eventos_sse = asyncio.Queue()

# 🔄 Patrullaje
async def patrullar():
    global patrullaje_activo
    patrullaje_activo = True
    try:
        with open("backend/zonas.json", "r", encoding="utf-8") as f:
            zonas = json.load(f)
    except:
        zonas = ["Nodo 3", "Nodo 7", "Nodo 12"]

    while patrullaje_activo:
        for zona in zonas:
            evento = detectar_evento(zona)
            if evento:
                hallazgo = registrar_hallazgo(zona, evento, "Alta", "patrullaje.py")
                await emitir_evento(hallazgo)
        await asyncio.sleep(10)

def detectar_evento(zona):
    return "Token detectado"

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

async def evento_generator():
    while True:
        evento = await eventos_sse.get()
        yield f"data: {json.dumps(evento)}\n\n"

async def emitir_evento(evento):
    await eventos_sse.put(evento)

@app.get("/stream")
async def stream():
    return StreamingResponse(evento_generator(), media_type="text/event-stream")

@app.post("/iniciar-patrullaje")
async def iniciar(background_tasks: BackgroundTasks):
    background_tasks.add_task(patrullar)
    return {"status": "Patrullaje iniciado"}

@app.get("/estado")
def estado():
    return {"patrullaje": patrullaje_activo}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    with open("users/credenciales.json", "r", encoding="utf-8") as f:
        usuarios = json.load(f)
    if usuarios.get(username) == password:
        return RedirectResponse(url="/frontend/index.html", status_code=302)
    return HTMLResponse(content="<h3>Acceso denegado</h3>", status_code=401)

@app.get("/")
def root():
    return {"status": "Sistema oracular activo"}
