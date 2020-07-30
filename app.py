# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
@app.route('/', methods=['GET','POST'])
def home_page():
    data = {
        'book_reviews':mongo.db["books-list"].find({}).sort('time', -1).limit(20),
    }
    return render_template('home_page.html', data=data, model=model, time=datetime.now())


@app.route('/new_post', methods=['GET','POST'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html', time=datetime.now())
    else:
        book_reviews = mongo.db['books-list']
        form = request.form
        book_title = form["book_title"]
        post_title = form["post_title"]
        author = form["author"]
        genres = form.getlist('genres')
        image_link = form['image_link']
        review = form["review"]
        rating = form["rating"]
        if float(rating) % 1 == 0:
            rating = int(rating)
        else:
            rating = float(rating)
        now = datetime.utcnow()
        book_review = {
            "book_title" : book_title,
            "post_title" : post_title,
            "author" : author,
            "genres" : genres,
            "image_link" : image_link,
            "review" : review,
            "rating" : rating,
            "time" : now,
        }
        book_reviews.insert(book_review)
        return redirect(url_for('home_page'))

@app.route('/blog_post/<book_review_id>')
def blog_post(book_review_id):
    book_reviews = mongo.db["books-list"]
    book_review_id = ObjectId(book_review_id)
    book_review = book_reviews.find_one({'_id':book_review_id})
    return render_template('blog_post.html', book_review=book_review, model=model, time=datetime.now())

@app.route('/tag_by/<book_review_tag>')
def tag_by(book_review_tag):
    book_reviews = mongo.db["books-list"]
    genres =   ["Action|Adventure", "Classics", "Comic|Graphic Novel", "Detective|Mystery",
                "Fantasy", "Historical Fiction", "Horror", "Literary Fiction",
                "Romance", "Science Fiction", "Short-Stories", "Suspense|Thrillers",
                "Biographies", "Memoirs", "Poetry", "Other",
                ]
    if book_review_tag in genres:
        book_review_tag = book_review_tag.replace('|','/')
        data = {
            'book_reviews':book_reviews.find({'genres':book_review_tag}).sort([('rating',-1),('time', -1)])
        }
        print(len(data))
    else:
        data = {
            'book_reviews':book_reviews.find({'author':book_review_tag}).sort([('rating',-1),('time', -1)])
        }
    return render_template('home_page.html', data=data, model=model, time=datetime.now())

@app.route('/sort_by', methods=['GET', 'POST'])
def sort_by():
    if request.method == 'GET':
        return "hi"
    else:
        book_reviews = mongo.db["books-list"]
        form = request.form
        genres_options = form["genres_options"]
        genres = form.getlist("genres")
        ratings_range_options = form["ratings_range_options"]
        ratings_range_slider = form["ratings_range_slider"].split(";")
        lower = float(ratings_range_slider[0])
        upper = float(ratings_range_slider[1])
        order = -1 if ratings_range_options == 'max_to_min' else 1
        if genres_options == 'all':
            if genres:
                data = {
                    'book_reviews' :    book_reviews.find(
                                            {'genres':{'$all':genres},
                                            'rating':{'$gte': lower, '$lte': upper}
                                            }
                                        ).sort([('rating',order),('time', -1)])
                }      
            else:
                data = {}
        elif genres_options == 'any':
            if genres:
                data = {
                    'book_reviews' :    book_reviews.find(
                                            {'genres':{'$in':genres},
                                            'rating':{'$gte': lower, '$lte': upper}
                                            }
                                        ).sort([('rating',order),('time', -1)])
                }
            else:
                data = {}
        else:
            if genres:
                data = {
                    'book_reviews' :    book_reviews.find(
                                            {'genres':{'$not': {'$in':genres}},
                                            'rating':{'$gte': lower, '$lte': upper}
                                            }
                                        ).sort([('rating',order),('time', -1)])
                }
            else:
                data = {
                    'book_reviews' : book_reviews.find(
                                        {'rating':{'$gte': lower, '$lte': upper}}
                                    ).sort([('rating',order),('time', -1)])
                }
        return render_template('home_page.html', data=data, model=model, time=datetime.now())