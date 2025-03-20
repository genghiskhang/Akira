from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Akira'

import akira.controllers
from akira.models import db