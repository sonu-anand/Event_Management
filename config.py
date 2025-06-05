from urllib.parse import quote_plus

class Config:
    DEBUG = True
    DB_USER = 'root'
    DB_PASSWORD = quote_plus('dev@#2022')
    DB_HOST = 'localhost'
    DB_PORT = '3306'
    DB_NAME = 'event_management'
    SQLALCHEMY_SERVER_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    SQLALCHEMY_DATABASE_URI = f"{SQLALCHEMY_SERVER_URI}/{DB_NAME}"