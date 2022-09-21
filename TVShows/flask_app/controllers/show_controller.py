from flask_app.models.show import Show
from flask_app import app
from flask import render_template,redirect,request,session, flash

@app.route('/new')
def new():
    return render_template('newshow.html')

@app.route('/create_show' , methods=['POST'])
def create_show():
    if not Show.validate_show(request.form):
        return redirect('/new')
    data = {
        "title" : request.form['title'],
        "network" : request.form['network'],
        "release_date" : request.form['release_date'],
        "description" : request.form['description'],
        "user_id" : session['user_id']
    }
    Show.create(data)
    return redirect('/dashboard')

@app.route('/edit/<int:show_id>')
def edit(show_id):
    data = {
        "show_id" : show_id
    }
    return render_template('editshow.html', show = Show.get_show_by_id(data))

@app.route('/show/<int:show_id>')
def show_show(show_id):
    data = {
        "show_id" : show_id
    }
    return render_template('showshow.html', show = Show.get_show_with_user(data), likes = Show.count_likes(data))

@app.route('/edit_show/<int:show_id>', methods=['POST'])
def edit_show(show_id):
    if not Show.validate_show(request.form):
        return redirect(f'/edit/{show_id}')
    data = {
        "title" : request.form['title'],
        "network" : request.form['network'],
        "release_date" : request.form['release_date'],
        "description" : request.form['description'],
        "id" : show_id
    }
    Show.update_show(data)
    return redirect('/dashboard')

@app.route('/delete/<int:show_id>')
def delete(show_id):
    data = {
        "id" : show_id
    }
    Show.delete(data)
    return redirect('/dashboard')