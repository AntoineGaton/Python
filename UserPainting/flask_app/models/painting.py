from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash #userd to validate

class Painting:
    db = 'user_painting'
    def __init__(self, data):
        self.id =data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = {}
    @classmethod
    def save(cls,data):
        query = "INSERT INTO paintings (title, description, price, created_at, updated_at, user_id) VALUES (%(title)s,%(description)s,%(price)s,NOW(), NOW(),%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_paintings = []
        for row in results:
            all_paintings.append(cls(row))
        return all_paintings
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_painter(cls):
        query = "SELECT * FROM paintings LEFT JOIN users ON users.id = user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        
        all_paintings = []
        
        for row in results:
            painting = cls(row)
        
        user_data = {
                        "id" : row['id'],
                        "first_name" : row['first_name'],
                        "last_name" : row['last_name'],
                        "email" : row['email'],
                        "password" : row['password'],
                        "created_at" : row['created_at'],
                        "updated_at" : row['updated_at']
        }

        painting.user = user.User(user_data)
        all_paintings.append(painting)
        
        return all_paintings

    @staticmethod
    def validate_painting(painting):
        is_valid = True
        if len(painting['title']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters","painting")
        if len(painting['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters","painting")
        if int(painting['price']) <= 0:
            is_valid = False
            flash("Price must be more than $0!","painting")
        return is_valid