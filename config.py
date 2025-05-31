# import os

# class Config:
#     SECRET_KEY = os.urandom(24)
#     WTF_CSRF_ENABLED = True  # Make sure CSRF is enabled
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/annotations.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # Email settings for Flask-Mail
#     MAIL_SERVER = 'smtp.gmail.com'  # Use your SMTP provider (e.g., Gmail, SendGrid)
#     MAIL_PORT = 465
#     MAIL_USE_SSL = True
#     MAIL_USERNAME = 'labibafarah2998@gmail.com'  # Replace with your email
#     MAIL_PASSWORD = 'pvku snzy zota syxk'  # Replace with your email password or app-specific password
#     MAIL_DEFAULT_SENDER = 'labibafarah2998@gmail.com'
    
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    WTF_CSRF_ENABLED = True  # CSRF protection enabled
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/annotations.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email settings for Flask-Mail, using environment variables for safety
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Set in environment variables
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Set in environment variables
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')  # Set in environment variables
