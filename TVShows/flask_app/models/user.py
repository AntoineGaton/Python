from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import show
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shows = []
    
    @classmethod
    def create(cls , data):
        query = "INSERT INTO users (first_name , last_name , email , password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL('exam_schema').query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be at least two characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least two characters", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['passwordc'] != user['password']:
            flash("Password confirmation must match password", "register")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("exam_schema").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        result = connectToMySQL("exam_schema").query_db(query,data)
        user = cls(result[0])
        return user

    @classmethod
    def get_user_with_shows(cls,data):
        query1 = "SELECT * FROM users JOIN shows ON users.id = shows.user_id WHERE users.id = %(user_id)s"
        result1 = connectToMySQL("exam_schema").query_db(query1,data)
        #Using two queries in case our user does not have any shows
        query2 = "SELECT * FROM users WHERE users.id = %(user_id)s"
        result2 = connectToMySQL("exam_schema").query_db(query2,data)
        user = cls(result2[0])
        for row in result1:
            show_data = {
            "id" : row['shows.id'],
            "title" : row['title'],
            "network" : row['network'],
            "release_date" : row['release_date'],
            "description" : row['description'],
            "created_at" : row['shows.created_at'],
            "updated_at" : row['shows.updated_at'],
            }
            user.shows.append(show.Show(show_data))
        return user

    @classmethod
    def like_show(cls, data):
        query = "INSERT INTO likes (user_id, show_id) VALUES (%(user_id)s, %(show_id)s)"
        return connectToMySQL('exam_schema').query_db(query, data)

    @classmethod
    def is_liked(cls, data):
        query = "SELECT * FROM likes WHERE user_id = %(user_id)s"
        results = connectToMySQL('exam_schema').query_db(query, data)
        liked = []
        for row in results:
            liked.append(row['show_id'])
        return liked
    
    @classmethod
    def unlike_show(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND show_id = %(show_id)s"
        connectToMySQL('exam_schema').query_db(query, data)

