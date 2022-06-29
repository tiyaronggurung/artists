from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Artist:
    db_name = "artists_paintings"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = "INSERT INTO artists (first_name,last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def read_all(cls):
        query = "SELECT * FROM artists;"
        results = connectToMySQL(cls.db_name).query_db(query)
        artists = []
        for row in results:
            artists.append( cls(row))
        return artists

    @classmethod
    def read_by_email(cls,data):
        query = "SELECT * FROM artists WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def read_by_id(cls,data):
        query = "SELECT * FROM artists WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(artist):
        is_valid = True
        query = "SELECT * FROM artists WHERE email = %(email)s;"
        results = connectToMySQL(Artist.db_name).query_db(query,artist)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(artist['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(artist['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(artist['last_name']) < 2:
            flash("Last name must be atleast 2 characters","register")
            is_valid= False
        if len(artist['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if artist['password'] != artist['confirm']:
            flash("Passwords don't match","register")
        return is_valid