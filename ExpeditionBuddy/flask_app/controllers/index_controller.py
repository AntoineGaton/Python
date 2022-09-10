from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#========================#
# REDIRECT TOH HOME PAGE #
#========================#
@app.route('/')
def index():
    return redirect ('/home')

#====================#
#     HOME PAGE      #
#====================#
@app.route('/home')
def home():
    return render_template('home.html')

#=====================#
#      DASHBOARD      #
#=====================#
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    
    return render_template("dashboard.html", user=user)

#=========================#
#   CREATE ACCOUNT PAGE   #
#=========================#
@app.route('/create_account')
def create_account():
    return render_template('create_account.html')

#==================#
#     ADD USER     #
#==================#
@app.route('/add_user', methods=['POST'])
def add_user():
    if not User.validate_register(request.form):
        return redirect('/create_account')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "car_model": request.form['car_model']
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

#============#
# LOGIN PAGE #
#============#
@app.route('/login')
def login():
    return render_template('login.html')

#===========#
#   LOGIN   #
#===========#
@app.route('/signin', methods=['POST'])
def signin():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/login')

    session['user_id'] = user.id

    return redirect('/dashboard')

#========#
# LOGOUT #
#========#
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')