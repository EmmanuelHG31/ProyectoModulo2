import os

from dotenv import load_dotenv 

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('Lacontraseñasecretadeflask', 'esteesunrespaldoporsielarchivoenvnocargarynotengollavesecreta') 
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    DATABASE = os.getenv('DATABASE_PATH', 'datebase.db')