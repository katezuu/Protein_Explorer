import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv('SECRET_KEY', 'replace-this-with-a-secure-key')
CACHE_DIR = os.path.join(BASE_DIR, 'data', 'cifs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
