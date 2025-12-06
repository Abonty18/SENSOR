# app.py
import eventlet
eventlet.monkey_patch()  # MUST be before any other imports
import os
from flask import Flask
from config import Config
from extensions import db, login_manager, mail, socketio
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

# Security defaults (env can override)
app.config.setdefault("SECRET_KEY", os.environ.get("SECRET_KEY", os.urandom(24)))
app.config.setdefault("WTF_CSRF_ENABLED", True)

# ---- Init extensions with this app ----
csrf = CSRFProtect(app)

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
socketio.init_app(app)

migrate = Migrate(app, db)
login_manager.login_view = 'main.login'

# Temp folder
app.config.setdefault('TEMP_FOLDER', os.path.join(os.getcwd(), 'temp'))
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)


# User loader
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


# Register blueprints
def register_blueprints():
    from routes import main    # now safe: routes imports only from extensions
    app.register_blueprint(main)


register_blueprints()


@app.get("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
