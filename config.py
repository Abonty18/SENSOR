# # config.py
# import os

# class Config:
#     SECRET_KEY = os.urandom(24)
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///annotations.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
