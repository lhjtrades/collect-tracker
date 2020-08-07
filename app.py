# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo
from datetime import datetime
import os


# -- Initialization section --
app = Flask(__name__)

app.config['SECRET'] = os.getenv("SECRET_KEY")
SECRET = app.config['SECRET']

# name of database
app.config['MONGO_DBNAME'] = 'users'

# URI of database
app.config['MONGO_URI'] = f'mongodb+srv://admin_2:{SECRET}@cluster0.fnifx.mongodb.net/users?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', time = datetime.now())
