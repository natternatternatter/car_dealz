from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import EMAIL_REGEX, DATABASE
from flask_app.models.user import User


class Car:

    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def validate_car(data):

        is_valid = True

        # drop down menu makes it impossible for price to be empty

        # if data['price'] == "":
        #     flash("Price cannot be empty")
        #     is_valid = False
        if data['model'] == "":
            flash("Model cannot be empty")
            is_valid = False
        if data['make'] == "":
            flash("Make cannot be empty")
            is_valid = False

        # drop down menu makes it impossible for year to be empty

        # if data['year'] == "":
        #     flash("Year cannot be empty")
        #     is_valid = False

        if data['description'] == "":
            flash("Description cannot be empty")
            is_valid = False

        # drop down menu makes it impossible for year to be less than 0

        # if data['year'] < 0:
        #     flash("Must provide a proper year (ex. 1995)")
        #     is_valid = False

        # drop down menu makes it impossible for price to be less than 0

        # if data['price'] < 0:
        #     flash("Price cannot be less than 0")
        #     is_valid = False

        if len(data['description']) > 50:
            flash("Description is too long (max 50)")
            is_valid = False

        return is_valid

    @classmethod
    def new_car(cls, data):
        query = "INSERT INTO cars (price, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM cars JOIN users ON cars.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)

        list_cars = []

        for row in results:
            current_car = cls(row)

            user_data = {
                **row,
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at'],
                "id": row['users.id']
            }

            current_user = User(user_data)
            current_car.user = current_user
            list_cars.append(current_car)

        return list_cars

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM cars JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if len(result) >= 1:
            current_car = cls(result[0])
            user_data = {
                **result[0],
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at'],
                "id": result[0]['users.id']
            }
            current_car.user = User(user_data)
            return current_car
        else:
            return None

    @classmethod
    def update_car(cls, data):
        query = "UPDATE cars SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s, user_id=%(user_id)s WHERE id=%(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def delete_tree(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # @classmethod
    # def user_trees(cls, data):
    #     query = "SELECT * FROM trees WHERE user_id = %(id)s;"
    #     result = connectToMySQL(DATABASE).query_db(query, data)

    #     return result

    @classmethod
    def select_car(cls, data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        current_car = cls(result[0])

        return current_car
