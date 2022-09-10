from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.painting import Painting
from flask_app.models.user import User

#===================#
# NEW ROUTE
#===================#
@app.route('/new/painting')
def painting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('add.html',user=User.get_by_id(data))

#===================#
# CREATE ENGINE
#===================#
@app.route('/create/painting',methods=['POST'])
def create_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect('/new/painting')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "user_id": session["user_id"]
    }
    Painting.save(data)
    return redirect('/painting')

#===================#
# EDIT ROUTE
#===================#
@app.route('/edit/painting/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }

    return render_template("edit.html",painting=Painting.get_one(data),user=User.get_by_id(user_data))

#===================#
# UPDATE ENGINE
#===================#
@app.route('/update/painting/<int:id>',methods=['POST'])
def update_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect(f'/update/painting/{id}')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "id": id
    }
    Painting.update(data)
    return redirect('/painting')

#===================#
# VIEW ROUTE
#===================#
@app.route('/painting/<int:id>')
def show_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view.html",painting=Painting.get_one(data),user=User.get_painter(user_data))

#===================#
# DESTROY ROUTE
#===================#
@app.route('/destroy/painting/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Painting.destroy(data)
    return redirect('/painting')