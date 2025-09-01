from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from utils.validar_credenciales import validar_credenciales, registrar_intento

app = FastAPI()

@app.get("/login")
def mostrar_login():
    return HTMLResponse("""
        <form method="post" action="/login">
            <label>Usuario:</label><br>
            <input type="text" name="usuario"><br>
            <label>Contraseña:</label><br>
            <input type="password" name="contraseña"><br>
            <input type="submit" value="Ingresar">
        </form>
    """)

@app.post("/login")
def procesar_login(usuario: str = Form(...), contraseña: str = Form(...)):
    exito = validar_credenciales(usuario, contraseña)
    registrar_intento(usuario, exito)

    if exito:
        return RedirectResponse(url="/panel", status_code=302)
    return HTMLResponse("<h3>Credenciales incorrectas</h3>", status_code=401)

@app.get("/panel")
def mostrar_panel():
    return HTMLResponse("<h2>Bienvenido al panel</h2>")
