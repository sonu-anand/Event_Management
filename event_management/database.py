from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()
Session = None

def init_db(app):
    server_engine = create_engine(app.config['SQLALCHEMY_SERVER_URI'])
        
    if not database_exists(server_engine.url.set(database=app.config['DB_NAME'])):
        create_database(server_engine.url.set(database=app.config['DB_NAME']))

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    
    global Session
    Session = scoped_session(sessionmaker(bind=engine))
    
    Base.metadata.create_all(bind=engine)