from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

my_db = "artists_paintings"

class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.artist_id = data['artist_id']
    
    @classmethod
    def read_all(cls):
        query = "SELECT * FROM paintings;"
        results = connectToMySQL(my_db).query_db(query)
        all_paintings = []
        for row in results:
            all_paintings.append( cls(row) )
        return all_paintings

    @classmethod
    def create(cls, data):
        query = "INSERT INTO paintings (title, description, price, artist_id) VALUES (%(title)s, %(description)s, %(price)s, %(artist_id)s);"
        results = connectToMySQL(my_db).query_db(query, data)
        return results
    
    @classmethod
    def read_by_id(cls, data):
        query = "SELECT * FROM paintings WHERE id=%(id)s;"
        results = connectToMySQL(my_db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s,  description=%(description)s, price=%(price)s, artist_id=%(artist_id)s, updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL(my_db).query_db(query, data)
        

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM paintings WHERE id=%(id)s;"
        return connectToMySQL(my_db).query_db(query, data)
    

