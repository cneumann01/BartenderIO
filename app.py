from flask import Flask, render_template, request, flash, redirect, session
from models import db, connect_db, User, Follows, Drink, FavoriteDrink, Collection, CollectionTable, FavoriteCollection

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///BartenderIO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret_key'

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    """Redirect to /drinks"""
    return redirect('/drinks')

@app.route('/drinks')
def show_drinks():
    """Show all drinks"""
    drinks = Drink.query.all()
    return render_template('drinks.html', drinks=drinks)

@app.route('/drinks/<int:drink_id>')
def show_drink(drink_id):
    """Show a drink"""
    drink = Drink.query.get_or_404(drink_id)
    return render_template('drink.html', drink=drink)




