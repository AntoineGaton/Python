from datetime import date
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import flask_app.models.user as usr # Fixed circular dependency...
import re

class Magazine:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.added_by_id = data["added_by_id"]

    #########################################################
    # Instance Methods: What our magazines can do
    #########################################################

    def get_subscribers(self):
        query = "SELECT * FROM users JOIN subscribers ON subscribers.user_id = users.id WHERE subscribers.magazine_id = %(id)s"
        data = {"id": self.id}
        subscribers_in_db = connectToMySQL("python_black_belt").query_db(query, data)
        subscribers = []
        for sub in subscribers_in_db:
            subscribers.append(usr.User(sub))
        return subscribers

    def get_num_subscribers(self):
        return len(self.get_subscribers())

    def get_added_by_full_name(self):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {"id": self.added_by_id}
        user_in_db = connectToMySQL("python_black_belt").query_db(query, data)
        if len(user_in_db) < 1:
            return None
        return usr.User(user_in_db[0]).get_full_name()

    def is_subscribed(self, user_id):
        query = "SELECT * FROM subscribers WHERE user_id = %(user_id)s AND magazine_id = %(id)s"
        data = {"id": self.id, "user_id": user_id}
        subscriber = connectToMySQL("python_black_belt").query_db(query, data)
        return False if len(subscriber) < 1 else True


    #########################################################
    # Class Methods
    #########################################################

    @classmethod
    def create_magazine(cls, data):
        query = "INSERT INTO magazines (title, description, added_by_id) VALUES (%(title)s, %(description)s, %(added_by_id)s)"
        return connectToMySQL("python_black_belt").query_db(query, data)
    
    @classmethod
    def update_magazine(cls, data):
        query = "UPDATE magazines SET title = %(title)s, description = %(description)s, added_by_id = %(added_by_id)s WHERE id = %(id)s"
        return connectToMySQL("python_black_belt").query_db(query, data)

    @classmethod
    def get_magazine(cls, data):
        query = "SELECT * FROM magazines WHERE id = %(id)s"
        magazine_in_db = connectToMySQL("python_black_belt").query_db(query, data)
        if len(magazine_in_db) < 1:
            return None
        return cls(magazine_in_db[0])

    @classmethod
    def get_all_magazines(cls):
        query = "SELECT * FROM magazines;"
        magazine_in_db = connectToMySQL("python_black_belt").query_db(query)
        magazines = []
        for mag in magazine_in_db:
            magazines.append(cls(mag))
        return magazines

    @classmethod
    def get_users_magazines(cls, data):
        query = "SELECT * FROM magazines WHERE added_by_id = %(added_by_id)s"
        magazines_in_db = connectToMySQL("python_black_belt").query_db(query, data)
        magazines = []
        for mag in magazines_in_db:
            magazines.append(cls(mag))
        return magazines

    @classmethod
    def delete_magazine(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s"
        connectToMySQL("python_black_belt").query_db(query, data)

        query = "DELETE FROM subscribers WHERE magazine_id = %(id)s"
        connectToMySQL("python_black_belt").query_db(query, data)

    @classmethod
    def subscribe(cls, data):
        query = "INSERT INTO subscribers (user_id, magazine_id) VALUES (%(user_id)s, %(id)s)"
        connectToMySQL("python_black_belt").query_db(query, data)

    @classmethod
    def unsubscribe(cls, data):
        query = "DELETE FROM subscribers WHERE user_id = %(user_id)s AND magazine_id = %(id)s"
        connectToMySQL("python_black_belt").query_db(query, data)