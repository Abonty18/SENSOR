# app.py
from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main
from flask_migrate import Migrate
from extensions import init_app



app = Flask(__name__)
app.config.from_object(Config)



# Ensure that a SECRET_KEY is set for session management
app.config['SECRET_KEY'] = '18ea7aabc0425006f029df4890ace6f45a897cd6a41e6d5f3810ace252e84e9d'  # Replace with a secure key in production

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)
login_manager.login_view = 'main.login'

# Register Blueprints
app.register_blueprint(main)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)

# # app.py
# from flask import Flask
# from config import Config
# from extensions import db, login_manager, init_app  # Make sure to import init_app from extensions
# from routes import main
# from flask_migrate import Migrate

# app = Flask(__name__)
# app.config.from_object(Config)

# # Initialize extensions using init_app from extensions
# init_app(app)
# migrate = Migrate(app, db)  # Migrate should work now with db initialized by init_app

# # Register Blueprints
# app.register_blueprint(main)

# # Define user loader for Flask-Login
# @login_manager.user_loader
# def load_user(user_id):
#     from models import User
#     return User.query.get(int(user_id))

# if __name__ == "__main__":
#     app.run(debug=True)