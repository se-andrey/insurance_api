import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgres://{DB_USER}:{DB_PASS}@db:5432/{DB_NAME}"

SECRET = os.getenv("SECRET")
