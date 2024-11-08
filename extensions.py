# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
import os

db = SQLAlchemy()
login_manager = LoginManager()

def init_app(app: Flask):
    # Use the DATABASE_URL environment variable provided by Render for configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Set by Render for PostgreSQL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
#DATABASE_URL
#postgres://sensor_odz0_user:BHCLVpLtEYyTuKFgUKLwBpT4oLOiHfrj@dpg-csmtch0gph6c73fpl000-a:5432/sensor_odz0
