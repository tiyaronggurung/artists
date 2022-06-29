from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.artist import Artist
from flask_app.models.painting import Painting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register_artist():
    if not Artist.validate_reg(request.form):
        return redirect("/")
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['fname'],
        "last_name": request.form['l_name'],
        "email": request.form['email'],
        "password": hashed_pass
    }
    artist_id = Artist.create(data)
    session["aid"] = artist_id
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    # retrieve artist form DB by email address
    this_artist = Artist.read_by_email({"email": request.form['email']})
    if bcrypt.check_password_hash(this_artist.password, request.form['password']):
        session['aid'] = this_artist.id
        return redirect("dashboard")
    else:
        flash("Invalid Username/password combination")
        return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "aid" not in session:
        flash("You Must be logged in")
        return redirect("/")
    this_artist = Artist.read_by_id({"id": session['aid']})
    all_paintings = Painting.read_all()
    return render_template("dashboard.html", artist = this_artist, all_paintings = all_paintings)

@app.route("/logout")
def logout():
    session.pop("aid")
    return redirect("/")