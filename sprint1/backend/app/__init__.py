from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    jwt = JWTManager(app)  # Initialize JWTManager with the app

    from app.routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
