import os

class Config:
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True  # Make sure CSRF is enabled
    SQLALCHEMY_DATABASE_URI = 'sqlite:///annotations.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email settings for Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'  # Use your SMTP provider (e.g., Gmail, SendGrid)
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'labibafarah2998@gmail.com'  # Replace with your email
    MAIL_PASSWORD = 'pvku snzy zota syxk'  # Replace with your email password or app-specific password
    MAIL_DEFAULT_SENDER = 'labibafarah2998@gmail.com'
    