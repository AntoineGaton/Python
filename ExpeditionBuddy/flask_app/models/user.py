from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import trip
from flask import flash
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = 'expedition_buddy'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.car_model = data['car_model']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trip = {}

    #======================#
    # ADD USER TO DATABASE #
    #======================#    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password, car_model, created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s, %(car_model)s, NOW(),NOW());"
        return connectToMySQL(cls.db).query_db(query,data)

    #=====================#
    # FETCH USER BY EMAIL #
    #=====================#
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    #==================#
    # FETCH USER BY ID #
    #==================#
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    # @classmethod
    # def get_user_with_painting(cls,data):
    #     query = "SELECT * FROM users LEFT JOIN paintings ON paintings.user_id = users.id WHERE users.id = %(id)s"
    #     results = connectToMySQL(cls.db).query_db(query,data)
        
    #     user = cls(results[0])
        
    #     painting_data = {
    #                     "id" : results[0]['id'],
    #                     "title" : results[0]['title'],
    #                     "description" : results[0]['description'],
    #                     "price" : results[0]['price'],
    #                     "created_at" : results[0]['created_at'],
    #                     "updated_at" : results[0]['updated_at']
    #     }

    #     user.painting = painting.Painting(painting_data)
            
    #     return user

    #========================#
    # VALIDATE USER CREATION #
    #========================#
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if len(user['car_model']) < 10:
            flash("Car Model must be at least 10 characters","register")
            is_valid= False
        return is_valid