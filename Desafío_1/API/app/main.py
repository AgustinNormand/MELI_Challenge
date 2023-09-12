import uvicorn
from fastapi import FastAPI

from app.Secapp import Secapp

app = FastAPI()
secapp = Secapp()
app.include_router(secapp.router)
