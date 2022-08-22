from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Trip:
    db = 'expedition_buddy'
    def __init__(self, data):
        self.id =data['id']
        self.name = data['name']
        self.start_address = data['start_address']
        self.end_address = data['end_address']
        self.trip_start = data['trip_start']
        self.trip_end = data['trip_end']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

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