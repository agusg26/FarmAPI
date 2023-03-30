from db.Modelos.User import User
from db.Modelos.Userdb import Userdb
from db.cliente import client

def user_schema(user) -> dict:
    return{ "id": str(user["_id"]),
           "fullname": user["fullname"],
           "email": user["email"],
           "disabled": user["disabled"]}
def users_schema(users) ->list:
    return [user_schema(user) for user in users]

def buscaUserdb(field: str, key):       
    try:
        user = user_schema(client.users2.find_one({field: key}))
        new_user = User(**user)
        return new_user
    except:
        return {"ERROR": "No se encontro el usuario"}
    
