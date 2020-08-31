# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template, redirect, url_for, session, flash
from flask import request
from flask_pymongo import PyMongo
from datetime import datetime
from model import User
from find import find_items, clear_type
from functions import get_title
from functions import gen_info
import os

import bcrypt, uuid, secrets

# -- Initialization section --
app = Flask(__name__)

app.config['SECRET'] = os.getenv("SECRET_KEY")
SECRET = app.config['SECRET']

# top is for heroku deployment
# s3 = os.environ['SECRET']
# secret_key = os.environ['SSECRET']
s3 = SECRET
secret_key = os.getenv("SSECRET")

app.config['SECRET_KEY'] = secret_key

# name of database
app.config['MONGO_DBNAME'] = 'users'

# URI of database
app.config['MONGO_URI'] = f'mongodb+srv://admin_2:{s3}@cluster0.fnifx.mongodb.net/users?retryWrites=true&w=majority'

mongo = PyMongo(app)

users = mongo.db.users

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    if(session.get('lin') == True):
        return redirect(url_for('dashboard'))
    return render_template('landing.html', time = datetime.now())

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if(session.get('lin') == True):
        if request.method == 'POST':
            clear_type(users, session.get('username'),'pending')
            clear_type(users, session.get('username'),'otw')

        existing_user = users.find_one({'username': session.get('username')})['items']
        num = {
            'pending_num': find_items(existing_user,'pending'),
            'otw_num': find_items(existing_user,'otw'),
            'completed_num': find_items(existing_user,'completed')
        }

        return render_template('index.html',time=datetime.now(), num = num, item_list=existing_user)
    return redirect(url_for('index'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    global users
    if (session.get('lin') == True):
        return(redirect(url_for('index')))
    if(request.method == 'POST'):
        existing_user = users.find_one({'username': request.form['username']}) 
        if existing_user:
            hashed = existing_user['password']
            if bcrypt.checkpw(request.form['password'].encode("utf-8"), hashed):
                session['username'] = request.form['username'] #TODO: secure sessions, maybe use unique id for this?
                temphold =  users.find_one({'username': request.form['username']})
                session['unique'] = temphold['unique']
                session['lin'] = True
                return(redirect(url_for('index')))
        flash('Invalid username or password. Please try again.')
        #return render_template('login.html', time = datetime.now())
    return render_template('login.html', time = datetime.now())

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    global users
    if request.method == 'POST':
        # does the user exist?
        existing_user = users.find_one({'username': request.form['username']}) 
        # if it doesn't yet:
        if existing_user is None:
            holdunique = uuid.uuid4().hex  #generate unique identifier to misuse
            hashed = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt())
            new_user = User(request.form['username'], hashed, holdunique) #create user
            #push user to db
            users.insert({
                'username': new_user.username,
                'password': new_user.password,
                'unique': new_user.unique,
                'items':[]
            })
            session['username'] = request.form['username'] #TODO: secure sessions
            session['unique'] = holdunique #currently using the unique id for "secure" sessions
            # app.config['SECRET_KEY'] = holdunique
            session['lin'] = True
            return redirect(url_for('index'))
        #if it already exists:
        flash( 'That username already exists! Try a different username.')
        # return render_template('login.html', time = datetime.now())
    return render_template('signup.html', time = datetime.now())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add', methods=['POST', 'GET'])
def add():
    global users
    if(session.get('lin') == True):
        form_info = {}

        if request.method == 'POST':
            user = session.get('username') 

            # if(request.form['type'].lower() == 'trade'):
            #     user_status = request.form['status1']
            # elif(request.form['type'].lower() == 'purchase'):
            #     user_status = request.form['status2']
            # else:
            #     user_status = request.form['status3']
            
            if (request.form['type'].lower() == 'trade' and request.form['status1'] == "Select status") or (request.form['type'].lower() == 'purchase' and request.form['status2'] == "Select status") or (request.form['type'].lower() == 'go' and request.form['status3'] == "Select status"):
                
                form_info = gen_info(request.form)
                flash('Please select a status.')
                return render_template('add.html', time = datetime.now(), form_info = form_info)
            
            info = gen_info(request.form)

            users.update(
                { 'username': user },
                { "$push": { 'items' : info} }
            )
            
            return redirect(url_for('index'))
            
        return render_template('add.html', time = datetime.now(), form_info = form_info)
    return redirect(url_for('index'))

@app.route('/completed', methods=['POST', 'GET'])
def completed():
    if(session.get('lin') == True):
        if request.method == 'POST':
            if request.form['id'] == 'clear':
                clear_type(users, session.get('username'),'completed')
            else:
                query = 'items.' + request.form['id'] + '.hidden_status'
                query_2 = 'items.' + request.form['id'] + '.status'
                users.update(
                    {'username':session.get('username')},
                    {'$set':{query:'completed',query_2:'Completed'}}
                )
        existing_user = users.find_one({'username': session.get('username')})['items']
        return render_template('completed.html',time=datetime.now(), item_list=existing_user)
    return redirect(url_for('index'))

@app.route('/item-<number>')
def item(number):
    if(session.get('lin') == True):
        existing_user = users.find_one({'username': session.get('username')})['items']
        item = existing_user[int(number)-1]
        num=int(number)-1
        item_name = get_title(item['getting'])
        return render_template('item.html',time=datetime.now(),item=item, num=num, item_name = item_name)
    return redirect(url_for('index'))

@app.route('/editing', methods=['POST', 'GET'])
def editing():
    if(session.get('lin') == True):
        if request.method == 'POST':
            user = session.get('username')
            
            # everything getting added
            info = gen_info(request.form)

            push_key = 'items.' + request.form['id']
            users.update(
                { 'username': user },
                { "$set": { push_key : info} }
            )
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if(session.get('lin') == True):
        if request.method == 'POST':
            push_key = 'items.' + request.form['id'] + '.delete'
            users.update(
                {'username': session.get('username')}, 
                {'$set': {push_key:'delete'}}
            )
            users.update(
                {'username': session.get('username')}, 
                {'$pull': {'items': {'delete': 'delete'}}}
            )
    return redirect(url_for('index'))