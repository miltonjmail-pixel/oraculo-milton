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

# 📓 Logging estructurado
def registrar_log(tipo, mensaje, extra=None):
    ruta = Path("backend/logs.json")
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "tipo": tipo,
        "mensaje": mensaje,
        "extra": extra or {}
    }
    try:
        if ruta.exists():
            with ruta.open("r", encoding="utf-8") as f:
                contenido = json.load(f)
                if not isinstance(contenido, list):
                    contenido = []
        else:
            contenido = []
        contenido.append(log)
        with ruta.open("w", encoding="utf-8") as f:
            json.dump(contenido, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Fallo al registrar log: {e}")

# 🔍 Patrullaje
async def patrullar():
    global patrullaje_activo
    patrullaje_activo = True
    registrar_log("sistema", "Patrullaje iniciado")

    try:
        with open("backend/zonas.json", "r", encoding="utf-8") as f:
            zonas = json.load(f)
        if not isinstance(zonas, list):
            print("[WARN] zonas.json no es una lista. Se usa fallback.")
            registrar_log("advertencia", "zonas.json no es una lista")
            zonas = ["Nodo 3", "Nodo 7", "Nodo 12"]
    except Exception as e:
        print(f"[ERROR] Fallo al cargar zonas.json: {e}")
        registrar_log("error", "Fallo al cargar zonas.json", {"error": str(e)})
        zonas = ["Nodo 3", "Nodo 7", "Nodo 12"]

    while patrullaje_activo:
        for zona in zonas:
            print(f"[{datetime.utcnow()}] Patrullando zona: {zona}")
            registrar_log("patrullaje", "Zona patrullada", {"zona": zona})
            evento = detectar_evento(zona)
            if evento:
                hallazgo = registrar_hallazgo(zona, evento, "Alta", "patrullaje.py")
                if hallazgo and isinstance(hallazgo, dict):
                    await emitir_evento(hallazgo)
                    registrar_log("hallazgo", "Evento registrado", hallazgo)
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
        try:
            with ruta.open("r", encoding="utf-8") as f:
                contenido = json.load(f)
                if isinstance(contenido, list):
                    datos = contenido
                else:
                    print("[WARN] hallazgos.json no es una lista. Se reinicia.")
                    registrar_log("advertencia", "hallazgos.json no es una lista")
        except Exception as e:
            print(f"[ERROR] Fallo al leer hallazgos.json: {e}")
            registrar_log("error", "Fallo al leer hallazgos.json", {"error": str(e)})

    datos.append(nuevo)

    try:
        with ruta.open("w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Fallo al escribir hallazgos.json: {e}")
        registrar_log("error", "Fallo al escribir hallazgos.json", {"error": str(e)})

    return nuevo

async def evento_generator():
    while True:
        try:
            evento = await eventos_sse.get()
            if evento and isinstance(evento, dict):
                yield f"data: {json.dumps(evento)}\n\n"
        except Exception as e:
            print(f"[ERROR] evento_generator: {e}")
            registrar_log("error", "Error en evento_generator", {"error": str(e)})
            continue

async def emitir_evento(evento):
    if evento and isinstance(evento, dict):
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
    registrar_log("sistema", "Patrullaje detenido")
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
        registrar_log("error", "Archivo de credenciales no encontrado")
        return HTMLResponse(content="<h3>Error: archivo de credenciales no encontrado</h3>", status_code=500)

    if usuarios.get(username) == password:
        registrar_log("acceso", "Login exitoso", {"usuario": username})
        return RedirectResponse(url="/panel", status_code=302)
    registrar_log("acceso", "Login fallido", {"usuario": username})
    return HTMLResponse(content="<h3>Acceso denegado</h3>", status_code=401)
