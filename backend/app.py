from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from backend.logic import generar_oraculo
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/oraculo")
async def oraculo():
    def evento():
        for i in range(5):
            yield f"data: {generar_oraculo(i)}\n\n"
            time.sleep(1)
    return HTMLResponse(evento(), media_type="text/event-stream")

@app.get("/")
async def home():
    return HTMLResponse(open("frontend/index.html").read())
