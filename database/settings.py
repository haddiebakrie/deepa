from dotenv import load_dotenv
import os

load_dotenv()

PG_PLAIN = os.getenv("PG_PLAIN")
PG_OBSCURE = os.getenv("PG_OBSCURE")
PG_PORT = os.getenv("PG_PORT")
PG_HOST = os.getenv("PG_HOST")
VERSION = os.getenv("VERSION")
TITLE = os.getenv("TITLE")
DEEPA_DB_URL = os.getenv("DEEPA_URL")
DEV_MODE = os.getenv("DEV_MODE")

if not all([PG_PLAIN, PG_OBSCURE, VERSION, TITLE]):
    raise ValueError("Some environment variables are missing. Please check your .env file.")
