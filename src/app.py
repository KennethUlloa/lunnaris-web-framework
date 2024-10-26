from fastapi import FastAPI
from config import configure_app, lifespan

app = FastAPI(lifespan=lifespan)
configure_app(app)