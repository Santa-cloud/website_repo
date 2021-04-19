from fastapi import FastAPI
import requests
from typing import Optional
from pydantic import BaseModel
app = FastAPI()



class Item(BaseModel):
    name: Optional[str] = None
   

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

@app.post("/method")
async def post_method(item: Item):
    return {"method": "POST"}