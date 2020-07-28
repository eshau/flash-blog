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
app.jinja_env.globals['current_time'] = datetime.now()

MONGO_DBNAME = os.getenv("MONGO_DBNAME")
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.r30xm.mongodb.net/{MONGO_DBNAME}?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
@app.route('/')
def home_page():
    return render_template('home_page.html', time=datetime.now())

@app.route('/new_post', methods=['GET','POST'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', time=datetime.now())
    else:
        books = mongo.db['books-list']
        form = request.form
        book_title = form["book_title"]
        post_title = form["post_title"]
        author = form["author"]
        genres = form.getlist('genres')
        review = form["review"]
        rating = form["rating"]
        print(genres)
        print(book_title, post_title, author, genres, review, rating)
        return render_template('home_page.html', time=datetime.now())

@app.route('/blog_post')
def blog_post():
    return render_template('blog_post.html')