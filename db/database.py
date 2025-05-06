import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

is_loaded = load_dotenv()
if not is_loaded:
    print("Environment variables not loaded. Check your .env file.")

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST", "localhost")
port = os.getenv("POSTGRES_PORT", "5432")
db = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)