import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify, Blueprint
from models import db, connect_db, User, Follows, Drink, FavoriteDrink, Collection, CollectionTable, FavoriteCollection
from forms import SignupForm, LoginForm, CollectionForm
from api_client import *
from api_lists import *
from sqlalchemy.exc import IntegrityError

def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SECRET_KEY'] = 'secret_key'

    connect_db(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(main)

    return app

main = Blueprint('main', __name__)

# HOME/LOGIN/LOGOUT/SIGNUP
@main.route('/')
def home():
    """Redirect to /drinks"""
    return redirect('/drinks')

@main.route('/signup', methods=['GET','POST'])
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
    
@main.route('/login', methods=['GET','POST'])
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
    
@main.route('/logout')
def logout():
    """Logout a user"""
    session.pop('USER_ID')
    session.pop('username')
    flash('Successfully logged out')
    return redirect('/')

# DRINKS
@main.route('/random-drink')
def random_drink():
    """Redirect to /drinks"""
    random_drink = get_random_drink()
    return redirect(f'/drinks/{random_drink["idDrink"]}')

@main.route('/drinks')
def show_drinks():
    """Show all drinks"""
    drinks = get_drinks_by_alcoholic()
    return render_template('drinks.html', drinks=drinks)

@main.route('/drinks/search' , methods=['GET','POST'])
def search_drinks():
    """Search for drinks"""
    search_query = request.form.get('search_query')
    drinks = get_drinks_by_name(search_query)
    if drinks:
        return render_template('drinks.html', drinks=drinks)
    else:
        flash('No drinks containing that name were found')
        return redirect('/drinks')

@main.route('/drinks/<int:drink_id>')
def show_drink(drink_id):
    """Show a drink"""
    drink = get_drink_by_id(drink_id)
    return render_template('drink.html', drink=drink)

@main.route('/drinks/<int:drink_id>/favorite', methods=['POST'])
def favorite_drink(drink_id):
    """Favorite a drink"""
    if not session.get('USER_ID'):
        flash('You must be logged in to favorite a drink')
        session['previous_page'] = f'/drinks/{drink_id}'
        return redirect('/login')
    else:
        favorite = FavoriteDrink.query.filter_by(drink_id=drink_id, user_id=session['USER_ID']).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'favorite_status': True})
        else:
            favorite_drink = FavoriteDrink(drink_id=drink_id, user_id=session['USER_ID'])
            db.session.add(favorite_drink)
            db.session.commit()
            return jsonify({'favorite_status': False})
        
# FAVORITES/CATEGORIES
@main.route('/drinks/favorites')
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
            drink = get_drink_by_id(favorite.drink_id)
            drinks.append(drink)

        if not drinks:
            flash('You have no favorites yet. Press the star next to a drink to favorite it!')
            return redirect('/drinks')
        return render_template('drinks.html', heading='Favorites', drinks=drinks)

@main.route('/drinks/alcoholic')
def show_alcoholic():
    drinks = get_drinks_by_alcoholic()
    return render_template('drinks.html', drinks=drinks)
@main.route('/drinks/non-alcoholic')
def show_non_alcoholic():
    drinks = get_drinks_by_non_alcoholic()
    return render_template('drinks.html', drinks=drinks)

@main.route('/drinks/category')
def show_categories():
    categories = list_categories()
    return render_template('categories.html', categories=categories)

@main.route('/drinks/category/<string:category>')
def show_category(category):
    drinks = get_drinks_by_category(category)
    return render_template('drinks.html', drinks=drinks)


# COLLECTIONS
@main.route('/collections')
def show_collections():
    """Show all collections"""
    if not session.get('USER_ID'):
        flash('You must be logged in to view collections')
        session['previous_page'] = '/collections'
        return redirect('/login')
    else:
        collections = Collection.query.filter_by(user_id=session['USER_ID']).all()
        if collections:
            return render_template('collections.html')
        else:
            flash('You have no collections yet. Create your first one below!')
            return redirect('/collections/new')
    
@main.route('/collections/new', methods=['GET','POST'])
def create_collection():
    """Create a collection"""
    if not session.get('USER_ID'):
        flash('You must be logged in to create a collection')
        session['previous_page'] = '/collections/new'
        return redirect('/login')
    form = CollectionForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        description = request.form.get('description')
        collection = Collection(name=name, description=description, user_id=session['USER_ID'])
        db.session.add(collection)
        db.session.commit()
        return redirect('/collections')
    else:
        return render_template('create_collection.html', form=form)
        
@main.route('/collections/<int:collection_id>')
def show_collection(collection_id):
    drinks = []
    drink_ids = CollectionTable.query.filter_by(collection_id=collection_id).with_entities(CollectionTable.drink_id).all()
    
    for drink_id in drink_ids:
            drink = get_drink_by_id(int(drink_id[0]))
            drinks.append(drink)
        
    if drinks:
        return render_template('drinks.html', drinks=drinks, heading=Collection.query.get_or_404(collection_id).name)
    else:
        flash("This collection's empty! Add some drinks with the 'View Collection' button and try again")
        return redirect('/')

@main.route('/collections/<int:collection_id>/edit', methods=['GET','POST'])
def edit_collection(collection_id):
    """Edit a collection"""
    if not session.get('USER_ID'):
        flash('You must be logged in to edit a collection')
        session['previous_page'] = f'/collections/{collection_id}/edit'
        return redirect('/login')
    else:
        collection = Collection.query.get_or_404(collection_id)
        if collection.user_id != session['USER_ID']:
            flash('You can only edit your own collections')
            return redirect('/collections')
        form = CollectionForm()
        if form.validate_on_submit():
            form.populate_obj(collection)
            db.session.commit()
            return redirect('/collections')
        else:
            return render_template('edit_collection.html', form=form, collection=collection)
        
@main.route('/collections/<int:collection_id>/delete', methods=['POST'])
def delete_collection(collection_id):
    """Delete a collection"""
    if not session.get('USER_ID'):
        flash('You must be logged in to delete a collection')
        session['previous_page'] = f'/collections/{collection_id}/delete'
        return redirect('/login')
    else:
        collection = Collection.query.get_or_404(collection_id)
        if collection.user_id != session['USER_ID']:
            flash('You can only delete your own collections')
            return redirect('/collections')
        db.session.delete(collection)
        db.session.commit()
        flash(f'{collection.name} deleted')
        return redirect('/collections')
    
@main.route('/collections/update-drinks', methods=['POST'])
def update_collection_drinks():
    """Update the drinks in collections"""
    if not session.get('USER_ID'):
        flash('You must be logged in to add or remove a drink from a collection')
        return redirect('/login')
    else:
        data = request.json
        drink_id = data.get('drinkId')
        selected_collections = data.get('collections')

        # Get the drink instance from the database
        drink = Drink.query.filter_by(id=drink_id).first()
        print(f'DRINK INSTANCE FOUND: {drink}')

        # If the drink doesn't exist in the database, fetch its details from the API
        if not drink:
            print('DRINK DOES NOT EXIST IN DATABASE')
            print('FETCHING DRINK DETAILS FROM API')
            drink_details = get_drink_by_id(drink_id)

            # Create a new Drink instance using the fetched details
            drink = Drink(
                id = drink_details['idDrink'],
                name=drink_details['strDrink'],
                thumb_url=drink_details['strDrinkThumb']
            )

            try:
                db.session.add(drink)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                flash('Error creating the drink. Please try again later')
                return redirect('/collections')

        # Now that we have the drink instance, we can proceed to add it to the collections
        for collection_id in selected_collections:
            collection = Collection.query.get_or_404(collection_id)

            if collection.user_id != session['USER_ID']:
                flash('You can only update your own collections')
                return redirect('/collections')

            try:
                collection_table_entry = CollectionTable.query.filter_by(collection_id=collection_id, drink_id=drink.id).first()

                if collection_table_entry:
                    db.session.delete(collection_table_entry)
                    flash(f'{drink.name} removed from {collection.name}')
                else:
                    new_collection_table_entry = CollectionTable(collection_id=collection_id, drink_id=drink.id)
                    db.session.add(new_collection_table_entry)
                    flash(f'{drink.name} added to {collection.name}')
                db.session.commit()

            except Exception as e:
                print(f'Error updating collections: {e}')
                db.session.rollback()
                flash('Error updating collections. Please try again later')
                return redirect('/')

        return 'success'

@main.route('/collections/selected', methods=['POST'])
def get_selected_collections():
    """Get the collections selected on the update collections modal"""
    if not session.get('USER_ID'):
        flash('You must be logged in to add or remove a drink from a collection')
        return redirect('/login')
    else:
        data = request.json
        drink_id = data.get('drinkId')

        selected_collection_entries = CollectionTable.query.filter_by(drink_id=drink_id).all()
        selected_collections = [entry.collection_id for entry in selected_collection_entries]

        return jsonify({'drinkId': drink_id, 'collections': selected_collections})


# APP CONTEXT PROCESSORS
@main.context_processor
def collections_processor():
    """Make user's collections available to all templates"""
    if not session.get('USER_ID'):
        collections = []
    else:
        collections = Collection.query.filter(Collection.user_id == session.get('USER_ID')).all()
    return dict(collections=collections)

@main.context_processor
def favorites_processor():
    """Make FavoriteDrink available to all templates for querying"""
    return dict(FavoriteDrink=FavoriteDrink)

# ERROR MESSAGES
@main.route('/login-error')
def login_error():
    """Show error message for login required"""
    flash ('You must be logged in to view that page')
    return redirect('/login')

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error=500, error_text=e), 500

@main.errorhandler(400)
def bad_request(e):
    return render_template('error.html', error=400, error_text=e), 400

@main.errorhandler(401)
def unauthorized(e):
    return render_template('error.html', error=401, error_text=e), 401

@main.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error=403, error_text=e), 403

@main.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=404, error_text=e), 404

@main.errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html', error=405, error_text=e), 405






