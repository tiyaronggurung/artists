from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.painting import Painting

@app.route("/paintings/new")
def new_painting():
    return render_template("new_painting.html")

@app.route("/paintings/create", methods=["POST"])
def create_painting():
    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "price": request.form['price'],
        "artist_id": session['aid']
    }
    Painting.create(data)
    return redirect("/dashboard")

@app.route("/paintings/edit/<int:id>")
def edit_painting(id):
    painting_to_edit = Painting.read_by_id({"id": id})
    return render_template("edit_paiting.html", painting = painting_to_edit)

@app.route("/paintings/update", methods=["POST"])
def update_painting():
    data = {
        "id": request.form['id'],
        "title": request.form['title'],
        "description": request.form['description'],
        "price": request.form['price'],
        "artist_id": request.form["artist_id"]
    }
    Painting.update(data)
    return redirect("/dashboard")

@app.route("/paintings/delete/<int:id>")
def delete_painting(id):
    Painting.delete({"id": id})
    return redirect("/dashboard")

@app.route("/paintings/<int:id>")
def view_painting(id):
    this_painting = Painting.read_by_id({"id": id})
    return render_template("view_painting.html", painting = this_painting)