import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, 'database', 'food_expiry.db')

SECRET_KEY = 'food_expiry_secret_key'

DEBUG = True