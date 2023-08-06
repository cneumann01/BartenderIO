from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)

    @classmethod
    def signup(cls, username, password):
        """Sign up a user"""
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user"""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        else:
            return False
        

class Follows(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    user_following = db.Column(db.String)
    user_followed = db.Column(db.String)

class Drink(db.Model):
    __tablename__ = 'drinks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    thumb_url = db.Column(db.String)

class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    collections_table_entries = db.relationship('CollectionTable', backref='collections', cascade='all, delete-orphan')

class CollectionTable(db.Model):
    __tablename__ = 'collections_table'
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, nullable=False)
    drink_id = db.Column(db.Integer, nullable=False)

    collection = db.relationship('Collection', backref='collections_table')

    __table_args__ = (
        db.ForeignKeyConstraint([collection_id], [Collection.id], ondelete='CASCADE'),
        db.ForeignKeyConstraint([drink_id], [Drink.id]),
    )

class FavoriteDrink(db.Model):
    __tablename__ = 'favorite_drinks'
    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class FavoriteCollection(db.Model):
    __tablename__ = 'favorite_collections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))

def connect_db(app):
    db.app = app
    db.init_app(app)