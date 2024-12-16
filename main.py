
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

# Modelos
class Carro(BaseModel):
    id: str
    marca: str
    modelo: int

class Usuario(BaseModel):
    id: str
    nombre: str
    edad: int

# Datos iniciales
carros = [
    Carro(id="1", marca="Mazda", modelo=1983),
    Carro(id="2", marca="Honda", modelo=1993),
    Carro(id="3", marca="Toyota", modelo=2005),
    Carro(id="4", marca="Chevrolet", modelo=2010),
]

usuarios = [
    Usuario(id="1", nombre="Juan Pérez", edad=30),
    Usuario(id="2", nombre="Ana Gómez", edad=25),
    Usuario(id="3", nombre="Luis Fernández", edad=28),
    Usuario(id="4", nombre="Carlos López", edad=35),
]

app = FastAPI()


app.mount("/modelo", StaticFiles(directory="modelo"), name="modelo")


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("modelo/index.html", "r", encoding="utf-8") as file:
        return file.read()


@app.get("/carros", response_model=List[Carro])
async def get_carros():
    return carros

@app.post("/carros")
async def create_carro(id: str = Form(...), marca: str = Form(...), modelo: int = Form(...)):
    nuevo_carro = Carro(id=id, marca=marca, modelo=modelo)
    carros.append(nuevo_carro)
    return {"message": "Nuevo carro creado"}

@app.delete("/carros/{id}")
async def delete_carro(id: str):
    global carros
    carros = [carro for carro in carros if carro.id != id]
    return {"message": f"Carro con id {id} ha sido eliminado"}

@app.put("/carros/{id}")
async def update_carro(id: str, carro: Carro):
    for index, c in enumerate(carros):
        if c.id == id:
            carros[index] = carro
            return {"message": "Carro actualizado"}
    raise HTTPException(status_code=404, detail="Carro no encontrado")

# Endpoints para usuarios
@app.get("/usuarios", response_model=List[Usuario])
async def get_usuarios():
    return usuarios

@app.post("/usuarios")
async def create_usuario(id: str = Form(...), nombre: str = Form(...), edad: int = Form(...)):
    nuevo_usuario = Usuario(id=id, nombre=nombre, edad=edad)
    usuarios.append(nuevo_usuario)
    return {"message": "Nuevo usuario creado"}

@app.delete("/usuarios/{id}")
async def delete_usuario(id: str):
    global usuarios
    usuarios = [usuario for usuario in usuarios if usuario.id != id]
    return {"message": f"Usuario con id {id} ha sido eliminado"}

@app.put("/usuarios/{id}")
async def update_usuario(id: str, usuario: Usuario):
    for index, u in enumerate(usuarios):
        if u.id == id:
            usuarios[index] = usuario
            return {"message": "Usuario actualizado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
