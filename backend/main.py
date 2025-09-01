from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
import json
import os

app = FastAPI()
LOG_PATH = "backend/logs.json"

def registrar_evento(request: Request, status_code: int):
    ip = request.client.host
    metodo = request.method
    ruta = request.url.path
    query = str(request.url.query)
    timestamp = datetime.utcnow().isoformat()

    evento = {
        "ip": ip,
        "timestamp": timestamp,
        "metodo": metodo,
        "ruta": ruta + ("?" + query if query else ""),
        "status": status_code
    }

    # Cargar logs existentes
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(evento)

    # Guardar
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

@app.get("/login", response_class=HTMLResponse)
async def mostrar_login(request: Request):
    registrar_evento(request, 200)
    error = request.query_params.get("error")
    mensaje_error = "<p style='color:red;'>Credenciales inválidas</p>" if error == "1" else ""
    return HTMLResponse(f"""
        <html>
        <head><title>Login</title></head>
        <body>
            <h2>Acceso al Panel Oracular</h2>
            {mensaje_error}
            <form method="post" action="/login">
                <label>Usuario:</label><br>
                <input type="text" name="usuario"><br>
                <label>Contraseña:</label><br>
                <input type="password" name="contraseña"><br>
                <input type="submit" value="Ingresar">
            </form>
        </body>
        </html>
    """)

@app.post("/login")
async def login(request: Request, usuario: str = Form(...), contraseña: str = Form(...)):
    if usuario == "admin" and contraseña == "secreto":
        registrar_evento(request, 302)
        return RedirectResponse("/panel", status_code=302)
    else:
        registrar_evento(request, 302)
        return RedirectResponse("/login?error=1", status_code=302)

@app.get("/panel", response_class=HTMLResponse)
async def panel(request: Request):
    registrar_evento(request, 200)
    return HTMLResponse("""
        <html>
        <head><title>Panel</title></head>
        <body>
            <h2>Bienvenido al Panel Oracular</h2>
            <p>Visualización en tiempo real activa.</p>
        </body>
        </html>
    """)
