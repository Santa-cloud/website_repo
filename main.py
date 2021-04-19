from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello world!"}

    
@app.get('/method')
def method():

    return {"message": "GET"}
