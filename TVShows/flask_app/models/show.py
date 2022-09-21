from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
class Show:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = {}

    @classmethod
    def create(cls , data):
        query = "INSERT INTO shows (title, network, release_date, description, created_at, updated_at, user_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, NOW(), NOW(), %(user_id)s)"
        return connectToMySQL('exam_schema').query_db(query, data)

    @classmethod
    def get_show_by_id(cls,data):
        query = "SELECT * FROM shows WHERE id = %(show_id)s"
        result = connectToMySQL("exam_schema").query_db(query,data)
        show = cls(result[0])
        return show

    @classmethod
    def get_show_with_user(cls, data):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id WHERE shows.id = %(show_id)s"
        results = connectToMySQL("exam_schema").query_db(query,data)
        show = cls(results[0])
        user_data = {
        "id" : results[0]['users.id'],
        "first_name" : results[0]['first_name'],
        "last_name" : results[0]['last_name'],
        "email" : results[0]['email'],
        "password" : results[0]['password'],
        "created_at" : results[0]['users.created_at'],
        "updated_at" : results[0]['users.updated_at']
        }
        show.user = user.User(user_data)
        return show

    @classmethod
    def update_show(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE id = %(id)s"
        connectToMySQL("exam_schema").query_db(query,data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s"
        connectToMySQL("exam_schema").query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows"
        return connectToMySQL("exam_schema").query_db(query)

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['release_date']) < 1:
            flash("All fields required", "show")
            is_valid = False
        if len(show['title']) < 3:
            flash("Title must be at least 3 characters", "show")
            is_valid = False
        if len(show['network']) < 3:
            flash("Network must be at least 3 characters", "show")
            is_valid = False
        if len(show['description']) < 3:
            flash("Description must be at least 3 characters", "show")
            is_valid = False
        return is_valid

    @classmethod
    def count_likes(cls, data):
        query = "SELECT * FROM likes WHERE show_id = %(show_id)s"
        results = connectToMySQL("exam_schema").query_db(query,data)
        likes = 0
        for row in results:
            likes = likes + 1
        return likes
