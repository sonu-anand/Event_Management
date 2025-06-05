from flask import Flask, g
from . import database


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    with app.app_context():
        from event_management import models
        database.init_db(app)
    
    from event_management import routes
    routes.register_routes(app)
    
    
    return app

