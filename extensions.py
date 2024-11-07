# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
import os

db = SQLAlchemy()
login_manager = LoginManager()
def init_app(app: Flask):
    # Use the DATABASE_URI environment variable for configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///default.db')  # fallback to SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)