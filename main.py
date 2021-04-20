from fastapi import FastAPI, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime, date
import requests
from typing import Optional
from pydantic import BaseModel
import hashlib
app = FastAPI()
app.id = 0
app.cache = []
#app.counter = 1

    
"""

class Item(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str
"""   
   

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
    if (password == "" and password_hash == ""):
        response.status_code = 401
        return {"auth": "wrong"}
    elif (password != None or password_hash != None):
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
"""       
@app.post("/register")
def register(person: Optional[Item], name: Optional[str] = None, surname: Optional[str] = None):
    if (name != None and surname != None):
        person.id = app.counter
        person.name = name
        person.surname = surname
        today = date.today()
        f_today = today.strftime("%Y-%m-%d")
        person.register_date = f_today
        waiting = 0
        for char in name:
            if char.isalpha():
                waiting += 1
        for char in surname:
            if car.isalpha():
                waiting += 1
        f_vacc_day = today + timedelta(days=waiting)
        person.vaccination_date = f_vacc_day.strftime("%Y-%m-%d")
        waiting = 0
        #global app.counter += 1
        json_compatible_item_data = jsonable_encoder(person)
        return JSONResponse(content=json_compatible_item_data)
    return
"""
# Ex4
class Register(BaseModel):
    name: str
    surname: str


def count_letters(word):
    return len([i for i in word if i.isalpha()])


@app.post('/register', status_code=201)
def register_view(register: Register):
    app.id += 1
    today = date.today()
    days = count_letters(register.name) + count_letters(register.surname)
    output_json = {
        'id': app.id,
        'name': register.name,
        'surname': register.surname,
        'register_date': str(today),
        'vaccination_date': str(today + timedelta(days=days))
    }
    app.cache.append(output_json)
    return output_json
    
# Ex5
@app.get('/patient/{patient_id}')
def patient_view(patient_id: int, response: Response):
    if patient_id < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response
    for patient_json in app.cache:
        if patient_json['id'] == patient_id:
            return patient_json
    response.status_code = status.HTTP_404_NOT_FOUND
    return response
