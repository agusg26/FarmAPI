from fastapi import APIRouter,HTTPException,status,Depends,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from db.cliente import client
from db.Models.User import User
from db.Models.Product import Product
from db.Schemas.Product import search_product,products_schema,product_schema
from bson import ObjectId
from datetime import datetime
from Routers.authUser import current_user

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix= "/product",tags=["product"])




@router.post("/new",response_model=Product, status_code=status.HTTP_201_CREATED)
async def addProduct(product: Product, user: User = Depends(current_user)):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail= "Usted no esta registrado como usuario")
    if type(search_product("name",str.lower(product.name))) == Product:
        raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail= "El producto ya esta registrado")
    product_dict = dict(product)
    product_dict["name"] = str.lower(product_dict["name"])
    del product_dict["id"]
    product_dict["last_update"] = datetime.now()
    id = client.products.insert_one(product_dict).inserted_id
    return search_product("_id",id)

@router.get("/all", status_code=status.HTTP_200_OK)
async def getProducts(request: Request):
    list = products_schema(client.products.find())
    return templates.TemplateResponse("products.html",{"request": request, "products": list})

@router.get("/{id}",status_code=status.HTTP_302_FOUND)
async def getProduct(id: str, user: User = Depends(current_user)):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail= "Usted no esta registrado como usuario")
    return search_product("_id", ObjectId(id))

@router.post("/",status_code=status.HTTP_302_FOUND)
async def getProduct(request: Request):
    formdata = await request.form()
    name = formdata['name']
    product = search_product("name",name)
    return templates.TemplateResponse("product.html",{"request":request,"product":product})

@router.patch("/update_stock/{name}")
async def stock(name: str,cant: int ,user: User = Depends(current_user)):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail= "Usted no esta registrado como usuario")
    if type(search_product("name",name)) is not Product:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= "Producto no encontrado")
    client.products.update_one({"name": name},{"$inc": {"stock": cant}})
    client.products.update_one({"name": name},{"$set": {"last_update": datetime.now()}})
    return search_product("name",name)

@router.post("/update")
async def update(request: Request):
    data = await request.form()
    product_dict = dict(data)
    del product_dict["prod_name"]
    try:
        search_product("name",data["prod_name"])
        client.products.find_one_and_replace({"name": data["prod_name"]},product_dict)
        client.products.update_one({"name": product_dict["name"]},{"$set": {"last_update": datetime.now()}})
    except:
        return templates.TemplateResponse("errorupdate.html",{"request":request})
    return RedirectResponse("/",303)

@router.patch("/update_price/{name}")
async def price(name: str,price: int,user: User = Depends(current_user)):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail= "Usted no esta registrado como usuario")
    if type(search_product("name",name)) is not Product:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= "Producto no encontrado")
    client.products.update_one({"name": name},{"$inc": {"price": price}})
    client.products.update_one({"name": name},{"$set": {"last_update": datetime.now()}})
    return search_product("name",name)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def product_del(id: str, user: User = Depends(current_user)):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail= "Usted no esta registrado como usuario")
    found = client.products.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Producto no encontrado") 