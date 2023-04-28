from db.Models.Product import Product
from db.cliente import client
from fastapi import HTTPException,status

def product_schema(product) -> dict:
    return {"id": str(product["_id"]),
            "name": product["name"],
            "stock": product["stock"],
            "price": product["price"],
            "last_update": str(product["last_update"])}

def products_schema(products) ->list:
    return [product_schema(product) for product in products]


def search_product(field: str, key):
    try:
        product = product_schema(client.products.find_one({field: key}))
        new_product = Product(**product)
        return new_product
    except:
        return "No se encontro"