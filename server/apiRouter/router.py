from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import JSONResponse


from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import WebSocket
import websockets

from fastalchemy import SQLAlchemyMiddleware, db

import json

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from passlib.context import CryptContext

from dbController.dbDriver import dbController

from speakChecker.pronunciation_check import PronunciationModel
from recommendationSystem.pipeline import recommendationModel

SECRET = '6a824282e5030a2d2c4059d0c096a820e22d8e2898036434'
manager = LoginManager(SECRET, token_url='/auth/token')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

context_instances = {}
@asynccontextmanager
async def lifespan(app: FastAPI):
    context_instances["database"] = dbController()
    context_instances["pronunciationModel"] = PronunciationModel()
    context_instances["recommendationModel"] = recommendationModel(context_instances["database"])
    yield
    context_instances["database"].on_shutdown()

app = FastAPI(lifespan=lifespan)
# app = FastAPI()

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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)





@manager.user_loader()
def load_user(email: str):
    # user = fake_db._db.get(email)
    
    return context_instances["database"].get_user(email)


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
    # print(user)
    return context_instances["database"].get_task_for_user(user["email"])

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


@app.get("/currentTask")
async def getCurrentTask(user=Depends(manager)):
    return context_instances["database"].get_task_for_user(user["email"])[0]


@app.post("/getAudio")
async def getAudio(file: UploadFile = File(...), user=Depends(manager)):
    print("user from get audio", user)
    try:
        # Read file contents (optional)
        contents = await file.read()
        
        # Save the file (optional)
        # file_location = f"{file.filename}"
        # with open(file_location, "wb+") as f:
        #     f.write(contents)
        print('user["email"] = ', user["email"])
        current_task = context_instances["database"].get_task_for_user(user["email"])[0]
        print("try to process audio")
        res = context_instances["pronunciationModel"].evaluate_task(current_task["text"], contents)
        context_instances["recommendationModel"].evaluate_errors(user, res)
        return JSONResponse(content={"status": "checked", "res": res["indexes_of_errors"]}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
