from fastapi import FastAPI
from pydantic import BaseModel
# from app.routers.login import authentication
from app.routers   import posesaan
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def config_router():
        # app.include_router(authentication.router)
        app.include_router(posesaan.router)

config_router()