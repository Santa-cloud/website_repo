from fastapi import FastAPI, Response, status
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
def auth(response: Response, password: Optional[str] = None, password_hash: Optional[str] = None):
    if (password != None or password_hash != None):
        e_password = password.encode("unicode-escape")
        h_password = hashlib.sha512(e_password)
        
        if (h_password.hexdigest() == password_hash):
            response.status_code = 204
            return {"auth": "ok"}
        else:
            response.status_code = 401
            return {"auth": "wrong"}           
    else:
        response.status_code = 401
        return {"auth": "wrong"}