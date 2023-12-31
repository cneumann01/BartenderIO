import requests
import os
BASE_URL = f'https://www.thecocktaildb.com/api/json/{os.getenv("API_KEY", default="/v1/1")}'

def get_drink_by_id(drink_id):
    """Get a drink by its id"""
    r = requests.get(f'{BASE_URL}/lookup.php?i={drink_id}')
    return r.json()['drinks'][0]

def get_random_drink():
    """Get a random drink"""
    r = requests.get(f'{BASE_URL}/random.php')
    return r.json()['drinks'][0]

def get_drinks_by_name(name):
    """Get drinks by name"""
    r = requests.get(f'{BASE_URL}/search.php?s={name}')
    return r.json()['drinks']

def get_drinks_by_first_letter(letter):
    """Get drinks by first letter"""
    r = requests.get(f'{BASE_URL}/search.php?f={letter}')
    return r.json()['drinks']

def get_drinks_by_alcoholic():
    """Get drinks by alcoholic"""
    r = requests.get(f'{BASE_URL}/filter.php?a=Alcoholic')
    return r.json()['drinks']

def get_drinks_by_non_alcoholic():
    """Get drinks by non alcoholic"""
    r = requests.get(f'{BASE_URL}/filter.php?a=Non_Alcoholic')
    return r.json()['drinks']

def get_drinks_by_category(category):
    """Get drinks by category"""
    r = requests.get(f'{BASE_URL}/filter.php?c={category}')
    return r.json()['drinks']

def get_drinks_by_glass(glass):
    """Get drinks by glass"""
    r = requests.get(f'{BASE_URL}/filter.php?g={glass}')
    return r.json()['drinks']

def get_drinks_by_ingredient(ingredient):
    """Get drinks by ingredient"""
    r = requests.get(f'{BASE_URL}/filter.php?i={ingredient}')
    return r.json()['drinks']



# Premium API Services
def get_drinks_by_popular():
    """Get popular drinks"""
    r = requests.get(f'{BASE_URL}/popular.php')
    return r.json()['drinks']

def get_drinks_by_latest():
    """Get 9 latest drinks"""
    r = requests.get(f'{BASE_URL}/latest.php')
    return r.json()['drinks'][:9]

def get_drinks_by_random():
    """Get 9 random drinks"""
    r = requests.get(f'{BASE_URL}/randomselection.php')
    return r.json()['drinks'][:9]