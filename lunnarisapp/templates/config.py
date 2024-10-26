import json
import importlib
from contextlib import asynccontextmanager
from fastapi import FastAPI


def configure_app(app: FastAPI):
    with open("config.json") as f:
        config = json.load(f)
    
    for module in config["modules.init"]:
        module = importlib.import_module(module)
        module.init(app)

@asynccontextmanager    
async def lifespan(app):
    yield

def add_middlewares(app: FastAPI):
    pass