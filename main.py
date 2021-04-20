from fastapi import FastAPI
import requests
from typing import Optional
from pydantic import BaseModel
import hashlib
app = FastAPI()



class Item(BaseModel):
    name: str
   

@app.get("/")
def root():
    return {"message": "Hello world!"}

    
@app.get("/method")
def get_method():
    return {"method": "GET"}
    
   
@app.delete("/method")
def delete_method():
    return {"method": "DELETE"}
    
    
@app.put("/method")
def put_method():
    return {"method": "PUT"}
    
    
@app.options("/method")
def options_method():
    return {"method": "OPTIONS"}

@app.post("/method", status_code=201)
def post_method():
    return {"method": "POST"}
    
@app.get("/auth")
def auth(password: str, password_hash: str):
    h_password = hashlib.sha512(password.encode())
    if (h_password.hexdigset() == "013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215"):
        return {"auth": "ok", status_code=204}
    else:
        return {"auth": "wrong", status_code=401}