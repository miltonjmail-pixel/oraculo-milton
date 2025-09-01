from fastapi import FastAPI, Request, BackgroundTasks, Form
from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json, time, hashlib, asyncio
from datetime import datetime

app = FastAPI()

# 🛡️ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📁 Archivos estáticos
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# 🔄 Estado global
patrullaje_activo = False
eventos_sse = asyncio.Queue()

# 🔍 Patrullaje
async def patrullar():
    global patrullaje_activo
    patrullaje_activo = True
    try:
        with open("backend/zonas.json", "r", encoding="utf-8") as f:
            zonas = json.load(f)
    except FileNotFoundError:
        zonas = ["Nodo 3", "Nodo 7", "Nodo 12"]

    while patrullaje_activo:
        for zona in zonas:
            print(f"[{datetime.utcnow()}] Patrullando zona: {zona}")  # ✅ Ajustado dentro del ciclo
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

    ruta = Path("backend/hallazgos.json")
    datos = []
    if ruta.exists():
        with ruta.open("r", encoding="utf-8") as f:
            datos = json.load(f)

    datos.append(nuevo)
    with ruta.open("w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2)

    return nuevo

async def evento_generator():
    while True:
        evento = await eventos_sse.get()
        yield f"data: {json.dumps(evento)}\n\n"

async def emitir_evento(evento):
    await eventos_sse.put(evento)

# 🌐 Endpoints

@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse("frontend/index.html")

@app.get("/panel")
def mostrar_panel():
    return FileResponse("frontend/index.html")

@app.get("/stream")
async def stream():
    return StreamingResponse(evento_generator(), media_type="text/event-stream")

@app.post("/iniciar-patrullaje")
async def iniciar(background_tasks: BackgroundTasks):
    background_tasks.add_task(patrullar)
    return {"status": "Patrullaje iniciado"}

@app.post("/detener-patrullaje")
def detener():
    global patrullaje_activo
    patrullaje_activo = False
    return {"status": "Patrullaje detenido"}

@app.get("/estado")
def estado():
    return {"patrullaje": patrullaje_activo}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    try:
        with open("users/credenciales.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        return HTMLResponse(content="<h3>Error: archivo de credenciales no encontrado</h3>", status_code=500)

    if usuarios.get(username) == password:
        return RedirectResponse(url="/panel", status_code=302)
    return HTMLResponse(content="<h3>Acceso denegado</h3>", status_code=401)
