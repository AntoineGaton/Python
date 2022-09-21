from flask_app import app, utility
from flask import render_template, redirect, request, session, flash
from flask_app.models.magazine import Magazine
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def dashboard():
    magazines = Magazine.get_all_magazines()
    user = User.get_user_by_id(session["user_id"])
    return render_template("dashboard.html", magazines = magazines, full_name = user.get_full_name())

@app.route('/show/<id>')
def show_magazine(id):
    data = {"id": id}
    magazine = Magazine.get_magazine(data)
    return render_template("show.html", magazine = magazine)

@app.route('/new')
def new_magazine():
    return render_template("new_magazine.html")

@app.route('/add_magazine', methods =["POST"])
def add_magazine():
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "added_by_id": session["user_id"]
    }

    valid = True
    if len(data["title"]) < 2:
        flash("Title must have at least 2 characters")
        valid = False

    if len(data["description"]) < 10:
        flash("Description must have at least 10 characters")
        valid = False

    if not valid:
        return redirect('/new')

    Magazine.create_magazine(data)
    return redirect('/dashboard')

@app.route('/subscribe/<id>')
def subscribe(id):
    data = {
        "id": id, 
        "user_id": session["user_id"]
    }
    Magazine.subscribe(data)
    return redirect('/dashboard')

@app.route('/unsubscribe/<id>')
def unsubscribe(id):
    data = {
        "id": id, 
        "user_id": session["user_id"]
    }
    Magazine.unsubscribe(data)
    return redirect('/dashboard')

@app.route('/delete/<id>')
def delete_magazine(id):
    data = {
        "id": id
    }
    Magazine.delete_magazine(data)
    return redirect("/user/account")