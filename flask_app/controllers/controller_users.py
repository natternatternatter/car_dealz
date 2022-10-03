from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def login_and_registration():
    return render_template("login_registration.html")


@app.route("/user/register", methods=["POST"])
def process_registration():
    if User.validate_registration(request.form) == False:
        return redirect("/")

    if User.validate_email(request.form) != None:
        flash("That email has already been used, try another")
        return redirect("/")

    data = {
        **request.form,
        "password": bcrypt.generate_password_hash(request.form['password'])
    }

    user_id = User.save(data)

    session['first_name'] = data['first_name']
    session['email'] = data['email']
    session['user_id'] = user_id

    return redirect("/dashboard")


@app.route("/user/login", methods=["POST"])
def process_login():
    current_user = User.validate_email(request.form)
    if current_user == None:
        flash("That email is not registered")
        return redirect("/")
    if not bcrypt.check_password_hash(current_user.password, request.form['password']):
        flash("Email and Password do not match")
        return redirect("/")

    session['first_name'] = current_user.first_name
    session['email'] = current_user.email
    session['user_id'] = current_user.id

    return redirect("/dashboard")


@app.route("/user/logout")
def process_logout():
    if "email" not in session:
        return redirect("/")
    session.clear()
    return redirect("/")
