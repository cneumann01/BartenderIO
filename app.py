from flask import Flask, render_template, request, flash, redirect, session, jsonify
from models import db, connect_db, User, Follows, Drink, FavoriteDrink, Collection, CollectionTable, FavoriteCollection
from forms import SignupForm, LoginForm
from api_client import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///BartenderIO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret_key'

connect_db(app)
with app.app_context():
    db.create_all()


# HOME/LOGIN/LOGOUT/SIGNUP
@app.route('/')
def home():
    """Redirect to /drinks"""
    return redirect('/drinks')

@app.route('/signup', methods=['GET','POST'])
def signup():
    """Sign up a user"""
    form = SignupForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        display_name = request.form.get('display_name')
        password = request.form.get('password')
        user = User.signup(username, password)
        if user:
            session['USER_ID'] = user.id
            session['username'] = user.username
            return redirect('/')
        else:
            flash('Username already taken')
            return redirect('/signup')
    else:
        return render_template('signup.html', form=form)
    
@app.route('/login', methods=['GET','POST'])
def login():
    """Login a user"""
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.authenticate(username, password)
        if user:
            session['USER_ID'] = user.id
            session['username'] = user.username
            if 'previous_page' in session:
                previous_page = session['previous_page']
                del session['previous_page']
                return redirect(previous_page)
            else:
                return redirect('/')
        else:
            flash('Invalid username/password')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    """Logout a user"""
    session.pop('USER_ID')
    session.pop('username')
    flash('Successfully logged out')
    return redirect('/')

# DRINKS
@app.route('/random-drink')
def random_drink():
    """Redirect to /drinks"""
    random_drink = get_random_drink()
    return redirect(f'/drinks/{random_drink["idDrink"]}')

@app.route('/drinks')
def show_drinks():
    """Show all drinks"""
    drinks = get_drinks_by_alcoholic()
    return render_template('drinks.html', drinks=drinks, FavoriteDrink=FavoriteDrink)

@app.route('/drinks/search' , methods=['GET','POST'])
def search_drinks():
    """Search for drinks"""
    search_query = request.form.get('search_query')
    drinks = get_drinks_by_name(search_query)
    if drinks:
        return render_template('drinks.html', drinks=drinks, FavoriteDrink=FavoriteDrink)
    else:
        flash('No drinks containing that name were found')
        return redirect('/drinks')

@app.route('/drinks/<int:drink_id>')
def show_drink(drink_id):
    """Show a drink"""
    drink = get_drink_by_id(drink_id)
    return render_template('drink.html', drink=drink, FavoriteDrink=FavoriteDrink)

@app.route('/drinks/<int:drink_id>/favorite', methods=['POST'])
def favorite_drink(drink_id):
    """Favorite a drink"""
    if not session.get('USER_ID'):
        flash('You must be logged in to favorite a drink')
        session['previous_page'] = f'/drinks/{drink_id}'
        return redirect('/login')
    else:
        favorite = FavoriteDrink.query.filter_by(api_drink_id=drink_id, user_id=session['USER_ID']).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'favorite_status': True})
        else:
            favorite_drink = FavoriteDrink(api_drink_id=drink_id, user_id=session['USER_ID'])
            db.session.add(favorite_drink)
            db.session.commit()
            return jsonify({'favorite_status': False})
        
# FAVORITES/CATEGORIES/COLLECTIONS
@app.route('/drinks/favorites')
def show_favorites():
    """Show all favorites"""
    if not session.get('USER_ID'):
        flash('You must be logged in to view favorites')
        session['previous_page'] = '/drinks/favorites'
        return redirect('/login')
    else:
        drinks = []
        favorites = FavoriteDrink.query.filter_by(user_id=session['USER_ID']).all()
        for favorite in favorites:
            drink = get_drink_by_id(favorite.api_drink_id)
            drinks.append(drink)

        if not drinks:
            flash('You have no favorites yet. Press the star next to a drink to favorite it!')
            return redirect('/drinks')
        return render_template('drinks.html', drinks=drinks, FavoriteDrink=FavoriteDrink)

@app.route('/drinks/alcoholic')
def show_alcoholic():
    drinks = get_drinks_by_alcoholic()
    return render_template('drinks.html', drinks=drinks, FavoriteDrink=FavoriteDrink)

@app.route('/drinks/non-alcoholic')
def show_non_alcoholic():
    drinks = get_drinks_by_non_alcoholic()
    return render_template('drinks.html', drinks=drinks, FavoriteDrink=FavoriteDrink)

@app.route('/drinks/category')
def show_categories():
    categories = list_categories()
    return render_template('categories.html', categories=categories)

@app.route('/drinks/category/<string:category>')
def show_category(category):
    drinks = get_drinks_by_category(category)
    return render_template('drinks.html', drinks=drinks, FavoriteDrink=FavoriteDrink)






# ERROR MESSAGES
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=404, error_text=e), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error=500, error_text=e), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error=403, error_text=e), 403

@app.errorhandler(401)
def unauthorized(e):
    return render_template('error.html', error=401, error_text=e), 401

@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html', error=400, error_text=e), 400

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html', error=405, error_text=e), 405






