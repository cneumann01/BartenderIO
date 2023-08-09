import requests
from api_client import BASE_URL

def list_categories():
    """List categories"""
    r = requests.get(f'{BASE_URL}/list.php?c=list')
    return r.json()['drinks']

def list_glasses():
    """List glasses"""
    r = requests.get(f'{BASE_URL}/list.php?g=list')
    return r.json()['drinks']

def list_ingredients():
    """List ingredients"""
    r = requests.get(f'{BASE_URL}/list.php?i=list')
    return r.json()['drinks']