from app import db
from models import CSVFile  # Adjust import paths as needed
from flask import Flask

app = Flask(__name__)
app.config.from_object("config.Config")  # Ensure you load your app's config

# Set the default user ID you want to assign to `uploaded_by` column
default_user_id = 1  # Replace with the actual ID of the user you want as the default

with app.app_context():
    # Update all rows where `uploaded_by` is currently NULL
    CSVFile.query.filter(CSVFile.uploaded_by == None).update({CSVFile.uploaded_by: default_user_id})
    db.session.commit()
    print("Uploaded_by column updated successfully for existing rows.")
