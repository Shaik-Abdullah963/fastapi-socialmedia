from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings
from urllib.parse import quote_plus
encoded_password = quote_plus(settings.database_password)

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# dependency
def get_db():
    db = SessionLocal()
    try:

        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'Asif@09060456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connecion was Successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ",error)
        time.sleep(2)