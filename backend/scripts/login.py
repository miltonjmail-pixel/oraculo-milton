from fastapi import FastAPI, Request
from utils.validar_credenciales import validar_credenciales
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/login")
async def login(request: Request):
    datos = await request.json()
    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")
    if validar_credenciales(usuario, contraseña):
        return JSONResponse(content={"status": "ok"})
    else:
        return JSONResponse(content={"status": "error", "detail": "Credenciales inválidas"}, status_code=401)
