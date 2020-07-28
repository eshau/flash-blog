# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
from datetime import datetime
import model

# -- Initialization section --
app = Flask(__name__)

# -- Routes section --
@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html", time=datetime.now())

@app.route('/new_post/')
def new_post():
    return render_template("new_post.html", time=datetime.now())