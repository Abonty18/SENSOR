# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

# 👇 Important: force threading mode, not eventlet/gevent
socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="threading"
)
