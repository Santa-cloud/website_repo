from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello world!"}

    
@app.get("/method")
def method():
    return {"message": "GET"}
    
   
@app.delete("/method")
def method():
    return {"message": "DELETE"}
    
    
@app.put("/method")
def method():
    return {"message": "PUT"}
    
    
@app.options("/method")
def method():
    return {"message": "OPTIONS"}
