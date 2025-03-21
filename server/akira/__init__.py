from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return 'Akira'

import akira.controllers
from akira.models import db