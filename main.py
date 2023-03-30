from fastapi import FastAPI
from Routers import authUser,Product
app = FastAPI()
app.include_router(authUser.router)
app.include_router(Product.router)

@app.get("/")
async def inicio():
    return "Bienvenido"