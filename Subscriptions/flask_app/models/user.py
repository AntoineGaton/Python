from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import flask_app.models.magazine as mag # Fixed circular dependency...
import re 

# Does pattern matching
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# From beginning '^', must have letters of a-z (lower) and A-Z (upper) and digits (\d) minimum 8 chars until end '$'
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$')

# Defining a User
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    #########################################################
    # Instance Methods: What our magazines can do
    #########################################################

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_magazines(self):
        return mag.Magazine.get_users_magazines({"added_by_id": self.id})


    #########################################################
    # Class Methods
    #########################################################

    # Getting the user by email
    @classmethod
    def get_user_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {"email": email}
        users_from_db = connectToMySQL("python_black_belt").query_db(query, data)

        # If email doesn't exist, return None
        if len(users_from_db) == 0:
            return None
        
        # If email exist, return User
        return cls(users_from_db[0])

    # Getting the user by id
    @classmethod
    def get_user_by_id(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {"id": id}
        users_from_db = connectToMySQL("python_black_belt").query_db(query, data)

        # If id doesn't exist, return None
        if len(users_from_db) == 0:
            return None
        
        # If id exist, return User
        return cls(users_from_db[0])

    # Inserting User into the database
    @classmethod
    def create_user(cls, first_name, last_name, email, password):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        data = {"first_name": first_name, "last_name": last_name, "email": email, "password": password}
        return connectToMySQL("python_black_belt").query_db(query, data)


    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s"
        connectToMySQL("python_black_belt").query_db(query, data)


    #########################################################
    # Validating Methods
    #########################################################

    @staticmethod
    def validate_name(user, category):
        is_valid = True

        # Validating the length of first name
        if len(user["first_name"]) < 3:
            flash("First name must have at least 3 characters", category)
            is_valid = False
        
        # Validating the length of last name
        if len(user["last_name"]) < 3:
            flash("Last name must have at least 3 characters", category)
            is_valid = False

        return is_valid

    @staticmethod
    def validate_password(user, category):
        is_valid = True

        # Validating the length of password
        if len(user["password"]) < 8:
            flash("Password must have at least 8 characters", category)
            is_valid = False
        
        # Checking if passwords match
        if not PASSWORD_REGEX.match(user["password"]):
            flash("Password must contain at least 1 number and 1 uppercase letter", category)
            is_valid = False

        if user["password"] != user["c_password"]:
            flash("Passwords need to match!", category)
            is_valid = False

        return is_valid

    #Validations, categorizing each error by passing category
    @staticmethod
    def validate_email(user, category):
        is_valid = True

        if not EMAIL_REGEX.match(user["email"]):
            flash("Email invalid", category)
            is_valid = False

        return is_valid

    def validate_registered_user(user):
        valid_name = User.validate_name(user, "register")
        valid_pass = User.validate_password(user, "register")
        valid_email = User.validate_email(user, "register")
        return valid_name and valid_pass and valid_email

    def validate_updated_user(user):
        valid_name = User.validate_name(user, "updated")
        valid_email = User.validate_email(user, "updated")
        return valid_name and valid_email