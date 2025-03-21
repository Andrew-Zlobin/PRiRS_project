from datetime import timedelta

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import WebSocket
import websockets

from fastalchemy import SQLAlchemyMiddleware, db

import json

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from passlib.context import CryptContext

SECRET = '6a824282e5030a2d2c4059d0c096a820e22d8e2898036434'
manager = LoginManager(SECRET, token_url='/auth/token')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

# app.add_middleware(SQLAlchemyMiddleware,
#                    db_module=database,
#                    models_module=models)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # '*'
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.1.1",
        "http://172.30.16.1"
        "http://localhost:19006",
        "http://localhost:8081",
        "http://localhost:8000",

        "ws://localhost",
        "ws://127.0.0.1",
        "ws://127.0.1.1",
        "ws://172.30.16.1"
        "ws://localhost:19006",
        "ws://localhost:8081",
        "ws://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_db = {'test@test.com': {'password': 'test'}}
def get_user(fake_db : dict, username):
    if username in fake_db.keys():
        return {"hashed_password": fake_db[username]["password"]}
    return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@manager.user_loader()
def load_user(email: str):
    # user = fake_db._db.get(email)
    user = fake_db[email]
    user["email"] = email
    return user


@app.get('/hello')
def hello(user=Depends(manager)):
    return user["email"]


@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    print("try to login")
    email = data.username
    password = data.password

    user = load_user(
        email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email), expires=timedelta(hours=8))
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.post('/logout')
def login(user=Depends(manager)):

    return {'access_token': "Ivalid", 'token_type': 'bearer'}




@app.get("/allTasks")
def getAllTaskListForCurrentUser(user=Depends(manager)):
    print(user)
    return [
    {
      "key": "task_1",
      "name": "task 1",
      "text": "please do this task firstly",
      "difficulty": 5},
    {
      "key": "task_2",
      "name": "task 2",
      "text": "please do this task",
      "difficulty": 3},
    {
      "key": "task_3",
      "name": "task 3",
      "text": "please do this task again",
      "difficulty": 5},
    {
      "key": "task_4",
      "name": "task 4",
      "text": "please do this task",
      "difficulty": 5},
    {
      "key": "task_5",
      "name": "task 5",
      "text": "please do this task final",
      "difficulty": 5},
      {
        "key": "task_6",
        "name": "task 6",
        "text": "please do this task firstly",
        "difficulty": 5},
      {
        "key": "task_7",
        "name": "task 7",
        "text": "please do this task",
        "difficulty": 3},
      {
        "key": "task_8",
        "name": "task 8",
        "text": "please do this task again",
        "difficulty": 5},
      {
        "key": "task_9",
        "name": "task 9",
        "text": "please do this task",
        "difficulty": 5},
      {
        "key": "task_10",
        "name": "task 10",
        "text": "please do this task final",
        "difficulty": 5},
    ]

# change email to smth like id, because its cringe

connections = {}
@app.websocket("/voiceStream/{id}")
async def websocketForAudio(webSocketServer: WebSocket, id: str): # , user=Depends(manager)
    try:
        print("connect", id)
        await webSocketServer.accept()
        connections[id] = webSocketServer
        print("check", connections.keys())
        while True:
            data = await webSocketServer.receive_text()
            print("websocket B server recieved: ", data, id)
            # await webSocketServer.send_text('{"response": "done"}')
    
        # await connections[id].send_text("hello")
    except Exception as e:
        print("connection closing id : ",connections[id],"  error  : " ,e)

@app.post("/getAudio")
def getAudio(data, user=Depends(manager)):
    