# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template, redirect, url_for, session, flash
from flask import request
from flask_pymongo import PyMongo
from datetime import datetime
from model import User
import os

import bcrypt, uuid, secrets

# -- Initialization section --
app = Flask(__name__)

app.config['SECRET'] = os.getenv("SECRET_KEY")
SECRET = app.config['SECRET']

secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

# name of database
app.config['MONGO_DBNAME'] = 'users'

# URI of database
app.config['MONGO_URI'] = f'mongodb+srv://admin_2:{SECRET}@cluster0.fnifx.mongodb.net/users?retryWrites=true&w=majority'

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

@app.route('/dashboard')
def dashboard():
    if(session.get('lin') == True):
        existing_user = users.find_one({'username': session.get('username')})
        num = {
            'pending_num': len(existing_user['pending']),
            'otw_num': len(existing_user['otw']),
            'completed_num': len(existing_user['completed'])
        }
        item_list = {
            'pending':existing_user['pending'],
            'otw':existing_user['otw']
        }
        return render_template('index.html',time=datetime.now(), num = num, item_list=item_list)
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
        flash('invalid username or password')
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
                'pending':[],
                'otw':[],
                'completed':[]
            })
            session['username'] = request.form['username'] #TODO: secure sessions
            session['unique'] = holdunique #currently using the unique id for "secure" sessions
            app.config['SECRET_KEY'] = holdunique
            session['lin'] = True
            return redirect(url_for('index'))
        #if it already exists:
        flash( 'That username already exists! Try logging in.')
        return render_template('login.html', time = datetime.now())
    return render_template('signup.html', time = datetime.now())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/add', methods=['POST', 'GET'])
def add():
    global users
    if(session.get('lin') == True):

        if request.method == 'POST':
            if (request.form['type'].lower() == 'trade' and request.form['status1'] == "Select status") or (request.form['type'].lower() == 'purchase' and request.form['status2'] == "Select status") or (request.form['type'].lower() == 'go' and request.form['status3'] == "Select status"):
                flash('Please select a status.')
                return redirect(url_for('add'))
            user = session.get('username')
            existing_user = users.find_one({'username': user})
            if(request.form['type'].lower() == 'trade'):
                    user_status = request.form['status1']
            elif(request.form['type'].lower() == 'purchase'):
                user_status = request.form['status2']
            else:
                user_status = request.form['status3']
            info = {
                'type':request.form['type'],
                'date':request.form['date'],
                'account':request.form['account'],
                'platform':request.form['platform'].capitalize(),
                'giving':request.form['giving'],
                'getting':request.form['getting'],
                'status':user_status
            }
            
            #setting up status to push
            status =""
            if (request.form['type'].lower() == 'purchase') and (request.form['status2'].lower() == 'paid'):
                status = 'pending'
            elif (request.form['type'].lower() == 'go') and (request.form['status3'].lower() != 'on the way'):
                status = 'pending'
            else:
                if(request.form['type'].lower() == 'trade'):
                    status = request.form['status1'].lower()
                elif(request.form['type'].lower() == 'purchase'):
                    status = request.form['status2'].lower()
                else:
                    status = request.form['status3'].lower()

            users.update(
                { 'username': user },
                { "$push": { status : info} }, 
                True
            )
            
            return redirect(url_for('index'))
            
        return render_template('add.html', time = datetime.now())
    return redirect(url_for('index'))

@app.route('/completed')
def completed():
    if(session.get('lin') == True):
        existing_user = users.find_one({'username': session.get('username')})
        item_list = {
            'pending':existing_user['pending'],
            'otw':existing_user['otw']
        }
        return render_template('completed.html',time=datetime.now(), item_list=item_list)
    return redirect(url_for('index'))