# # app.py
# from flask import Flask
# from config import Config
# from extensions import db, login_manager
# from flask_migrate import Migrate
# import os
# from flask_mail import Mail
# from flask_wtf.csrf import CSRFProtect  # Import CSRF protection
# from flask_socketio import SocketIO
# app = Flask(__name__)
# socketio = SocketIO(app)
# app.config['DEBUG'] = True
# app.config.from_object(Config)

# # Initialize Mail instance
# mail = Mail(app)



# # Set a SECRET_KEY for session management
# app.config['SECRET_KEY'] = '18ea7aabc0425006f029df4890ace6f45a897cd6a41e6d5f3810ace252e84e9d'  # Replace with a secure key in production
# # CSRF protection
# csrf = CSRFProtect(app)
# # Configure TEMP_FOLDER
# app.config['TEMP_FOLDER'] = os.path.join(os.getcwd(), 'temp')  # Define the temp folder
# if not os.path.exists(app.config['TEMP_FOLDER']):  # Create the folder if it doesn't exist
#     os.makedirs(app.config['TEMP_FOLDER'])

# # Initialize extensions
# db.init_app(app)
# migrate = Migrate(app, db)
# login_manager.init_app(app)
# login_manager.login_view = 'main.login'

# # User loader for login manager
# @login_manager.user_loader
# def load_user(user_id):
#     from models import User  # Import User model lazily to avoid circular import
#     return User.query.get(int(user_id))

# # Register Blueprints
# def register_blueprints():
#     from routes import main  # Import main blueprint here to avoid circular imports
#     app.register_blueprint(main)

# # Call the function to register blueprints
# register_blueprints()

# # if __name__ == "__main__":
# #     app.run(debug=True)
# if __name__ == "__main__":
#     import os
#     app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
# app.py
import os
from flask import Flask
from config import Config
from extensions import db, login_manager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)

# ---- Security / prod toggles (let env control these) ----
# Do NOT hardcode SECRET_KEY or DEBUG here; Config pulls from env.
# You can override locally with environment variables if needed.
app.config.setdefault("SECRET_KEY", os.environ.get("SECRET_KEY", os.urandom(24)))
app.config.setdefault("WTF_CSRF_ENABLED", True)

# ---- Extensions ----
csrf = CSRFProtect(app)
mail = Mail(app)                    # <- routes import this (from app import mail)
db.init_app(app)
migrate = Migrate(app, db)

# Socket.IO (eventlet in production)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"  # requires eventlet installed; see Gunicorn cmd below
)

login_manager.init_app(app)
login_manager.login_view = 'main.login'

# Temp folder (ephemeral on Koyeb; fine for scratch files)
app.config.setdefault('TEMP_FOLDER', os.path.join(os.getcwd(), 'temp'))
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

# User loader
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Register blueprints late to avoid circular imports
def register_blueprints():
    from routes import main
    app.register_blueprint(main)

register_blueprints()

# Optional: a simple health check route for Koyeb
@app.get("/health")
def health():
    return {"status": "ok"}, 200

# Local dev entrypoint
if __name__ == "__main__":
    # For local testing with socket.io, run the socketio server
    socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
