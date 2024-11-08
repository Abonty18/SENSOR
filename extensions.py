# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
import os

db = SQLAlchemy()
login_manager = LoginManager()

def init_app(app: Flask):
    # Use DATABASE_URL as configured in Render
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Set by Render
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager.init_app(app)