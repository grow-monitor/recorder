import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT", 1234))
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
DB_URL = os.environ.get("DB_URL")
TABLE = os.environ.get("TABLE")
