from fastapi import FastAPI, Response, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
#from fastapi.staticfiles import StaticFiles
from datetime import date, timedelta
from typing import Optional
from pydantic import BaseModel

import hashlib

app = FastAPI()
app.id = 0
app.cache = []
app.access_tokens = []
app.secret_key = 'kashduhashdbahsdgahskdgasdgasdgsdgkjasfnuaevbczknckzygschkzsgckjhwz'
#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return {"message": "Hello world!"}

    
@app.api_route('/method', methods=["GET", "DELETE", "PUT", "OPTIONS"])
def method_view(request: Request):
    return {"method": request.method}


@app.post("/method", status_code=201)
def post_method():
    return {"method": "POST"}


@app.get("/auth")
def auth(response: Response, password: Optional[str] = None, password_hash: Optional[str] = None):
    if password == "" or password_hash == "":
        response.status_code = 401
        return {"auth": "wrong"}
    elif password is not None or password_hash is not None:
        h_password = hashlib.sha512(password.encode("unicode-escape"))
        if h_password.hexdigest() == password_hash:
            response.status_code = 204
            return {"auth": "ok"}
        else:
            response.status_code = 401
            return {"auth": "wrong"}           
    else:
        response.status_code = 401
        return {"auth": "wrong"}


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


# L3 Ex1
@app.get("/hello", response_class=HTMLResponse)
def hello(request: Request):
    return templates.TemplateResponse(
        "index.html.j2",
        {"request": request, "todays_date": date.today()},
    )


@app.post("/login_session")
def login(user: str, password: str, response: Response):
    session_token = hashlib.sha256(f"{user}:{password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return {"message": "Welcome"}


@app.post("/login_token")
def login(user: str, password: str, response: Response):
    session_token = hashlib.sha256(f"{user}:{password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return {"token": {session_token}}



'''
@app.post("/login_session")
def login(user: str, password: str, response: Response):
    session_token = hashlib.sha256(f"{user}{password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return {"message": "Welcome"}


@app.get("/data/")
def secured_data(*, response: Response, session_token: str = Cookie(None)):
    print(session_token)
    print(app.access_tokens)
    print(session_token in app.access_tokens)
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=403, detail="Unathorised")
    else:
        return {"message": "Secure Content"}

'''