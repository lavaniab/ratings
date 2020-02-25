"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("users-list.html", users=users)


@app.route('/register', methods=['GET'])
def register_form():
    """Getting the registration form"""
    return render_template("register-form.html")

    
@app.route('/register', methods=['POST'])
def register_process():
    """Obtain user log in information, with post request."""

    email = request.form["email"]
    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("Logged in, User {email} added.")

    return redirect("/")


@app.route('/login', methods=['POST'])
def login_process():
    """Login page, allow users to attempt login and check for validity"""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user exists")
        return redirect("/login")
    if user.password != password:
        flash("Incorrect password entered")

        session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/users/{user.user_id}")


@app.route('/logout')  
def logout():
    """Allow users to logout"""
    del session["user_id"]
    flash("Logged Out")
    return redirect("/")


@app.route('/movies')
def all_movies():
    """Here is a list of movies in database."""

    return render_template("movies.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
