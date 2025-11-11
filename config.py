# import os

# class Config:
#     SECRET_KEY = os.urandom(24)
#     WTF_CSRF_ENABLED = True  # Make sure CSRF is enabled
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///annotations.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # Email settings for Flask-Mail
#     MAIL_SERVER = 'smtp.gmail.com'  # Use your SMTP provider (e.g., Gmail, SendGrid)
#     MAIL_PORT = 465
#     MAIL_USE_SSL = True
#     MAIL_USERNAME = 'labibafarah2998@gmail.com'  # Replace with your email
#     MAIL_PASSWORD = 'pvku snzy zota syxk'  # Replace with your email password or app-specific password
#     MAIL_DEFAULT_SENDER = 'labibafarah2998@gmail.com'
    
# config.py
# config.py
import os
from dotenv import load_dotenv

# --- Load .env file automatically if present ---
load_dotenv()

class Config:
    """Base configuration for Flask app."""

    # --- Security ---
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    WTF_CSRF_ENABLED = True

    # --- Database ---
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///annotations.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Mail settings (Gmail or another SMTP provider) ---
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "465"))  # default SSL port

    # Default: SSL ON (since Gmail prefers 465 for app passwords)
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "true").lower() == "true"
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "false").lower() == "true"

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")  # e.g. your Gmail address
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # 16-char App Password
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # --- Optional debug settings ---
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
