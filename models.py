from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    display_name = db.Column(db.String)
    password_hash = db.Column(db.String)

class Follows(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    user_following = db.Column(db.String)
    user_followed = db.Column(db.String)

class Drink(db.Model):
    __tablename__ = 'drinks'
    id = db.Column(db.Integer, primary_key=True)
    api_drink_id = db.Column(db.Integer)
    name = db.Column(db.String)
    thumb_url = db.Column(db.String)

class FavoriteDrink(db.Model):
    __tablename__ = 'favorite_drinks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id'))

class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class CollectionTable(db.Model):
    __tablename__ = 'collections_table'
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id'))

class FavoriteCollection(db.Model):
    __tablename__ = 'favorite_collections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))

    def connect_db(app):
        db.app = app
        db.init_app(app)