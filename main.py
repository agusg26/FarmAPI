from fastapi import FastAPI, Request
from Routers import authUser,Product
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(authUser.router)
app.include_router(Product.router)

@app.get("/")
async def inicio(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})