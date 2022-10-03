from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.car import Car
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/dashboard")
def display_dashboard():
    if "email" not in session:
        return redirect("/")

    list_cars = Car.get_all_with_users()

    return render_template("dashboard.html", list_cars=list_cars)


# @app.route("/trees/<int:id>")
# def display_one_tree(id):
#     if "email" not in session:
#         return redirect("/")

#     data = {
#         "id": id
#     }

#     current_tree = Tree.get_one_with_user(data)

#     return render_template("display_tree.html", current_tree=current_tree)


@app.route("/new")
def display_new_car():
    if "email" not in session:
        return redirect("/")

    return render_template("new_car.html")


@app.route("/car/new", methods=["POST"])
def new_car():

    if "email" not in session:
        return redirect("/")

    if Car.validate_car(request.form) == False:
        return redirect("/new")

    data = {
        **request.form,
        "user_id": session['user_id']
    }

    Car.new_car(data)

    return redirect("/dashboard")


# @app.route("/user/account")
# def display_my_trees():
#     return render_template("my_trees.html")


@app.route("/show/<int:id>")
def show_car(id):

    if "email" not in session:
        return redirect("/")

    data = {
        "id": id
    }

    current_car = Car.get_one_with_user(data)
    return render_template("show_car.html", current_car=current_car)


@app.route("/edit/<int:id>")
def display_update_car(id):

    if "email" not in session:
        return redirect("/")

    data = {
        'id': id
    }

    car = Car.select_car(data)

    return render_template("edit_car.html", car=car)


@app.route("/edit/car/<int:id>/", methods=["POST"])
def update_car(id):

    if "email" not in session:
        return redirect("/")

    if Car.validate_car(request.form) == False:
        return redirect("/edit/<int:id>")

    car_data = {
        **request.form,
        "id": id,
        "user_id": session['user_id']
    }

    Car.update_car(car_data)
    return redirect("/dashboard")


@app.route("/<int:id>/delete")
def delete_car(id):

    if "email" not in session:
        return redirect("/")

    data = {
        "id": id
    }

    Car.delete_tree(data)
    return redirect("/dashboard")
