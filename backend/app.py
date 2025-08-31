from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import time

app = FastAPI()

# Historial de hallazgos
hallazgos = []

# Patrullaje activo
patrullaje_activo = False

@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/iniciar")
def iniciar(background_tasks: BackgroundTasks):
    global patrullaje_activo
    patrullaje_activo = True
    background_tasks.add_task(patrullar)
    return {"status": "Patrullaje iniciado"}

@app.post("/detener")
def detener():
    global patrullaje_activo
    patrullaje_activo = False
    return {"status": "Patrullaje detenido"}

@app.get("/hallazgos")
def obtener_hallazgos():
    return {"hallazgos": hallazgos}

@app.get("/stream")
async def stream():
    async def event_generator():
        last_index = 0
        while True:
            if last_index < len(hallazgos):
                yield {
                    "event": "hallazgo",
                    "data": hallazgos[last_index]
                }
                last_index += 1
            await asyncio.sleep(1)
    return EventSourceResponse(event_generator())

def patrullar():
    while patrullaje_activo:
        hallazgo = f"Hallazgo #{len(hallazgos)+1} @ {time.strftime('%H:%M:%S')}"
        hallazgos.append(hallazgo)
        time.sleep(5)
