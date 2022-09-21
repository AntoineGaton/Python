from flask_app import app, utility
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    # Check if we already are logged in, if so: redirect to dashboard
    if utility.logged_in():
        return redirect('/dashboard')
    return render_template("register_login.html")

@app.route('/register', methods = ["POST"])
def register():
    # Getting all the data that was submitted into our form
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]

    # Validating the data that were given
    if not User.validate_registered_user(request.form):
        return redirect('/')

    # Is email already registered?
    user = User.get_user_by_email(request.form["email"])
    if user != None:
        flash("Invalid Email/Password", "register")
        return redirect('/')

    # Encrypting our password
    password = bcrypt.generate_password_hash(password)

    # Creating the user and storing the session
    session['user_id'] = User.create_user(first_name, last_name, email, password)
    session['first_name'] = first_name
    session['last_name'] = last_name
    return redirect ('/dashboard')

@app.route('/login', methods = ["POST"])
def login():

    # Get the email from the user and validate if it already exist 
    email = request.form["email"]
    user = User.get_user_by_email(email)
    if user == None:
        flash("Invalid Email/Password", "login")
        return redirect('/')

    # Get the password and validate if it matches
    password = request.form["password"]
    if not bcrypt.check_password_hash(user.password, password):
        flash("Invalid Email/Password", "login")
        return redirect('/dashboard')

    # Setting the session which signifies that they're logged in
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('first_name')
    session.pop('last_name')
    return redirect('/')

@app.route('/user/account')
def update_user():
    user = User.get_user_by_id(session["user_id"])
    return render_template("update_user.html", user = user)

@app.route('/user/update', methods = ["POST"])
def update():
    # Validate the first_name, last_name, and email are still valid
    if not User.validate_updated_user(request.form):
        return redirect('/user/account')

    data = {
        "id": session["user_id"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
    }
    User.update_user(data)
    return redirect('/user/account')