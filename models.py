# models.py
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from extensions import db  # Import db from extensions, not app
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    department = db.Column(db.String(50))
    completed_courses = db.Column(db.String(150))
    experience_years = db.Column(db.Integer)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Annotator')  # New role field

# Define roles
DEVELOPER_ROLE = 'Developer'
ANNOTATOR_ROLE = 'Annotator'


class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    annotation = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_final = db.Column(db.Boolean, default=False)  # New flag to mark annotation as final


class CompletedReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    annotator_1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    annotation_1 = db.Column(db.Text)
    annotator_2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    annotation_2 = db.Column(db.Text)
    annotator_3_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    annotation_3 = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships to reference User objects (Optional)
    annotator_1 = db.relationship('User', foreign_keys=[annotator_1_id])
    annotator_2 = db.relationship('User', foreign_keys=[annotator_2_id])
    annotator_3 = db.relationship('User', foreign_keys=[annotator_3_id])


class CSVFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # New field for uploader ID
    uploader = db.relationship('User', backref='uploaded_files', lazy=True)  # Relationship to User
    reviews = db.relationship('Review', backref='csv_file_assoc', lazy=True)

  # This backref is causing the conflict


class Review(db.Model):
    __tablename__ = 'review'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    annotation_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    csv_file_id = db.Column(db.Integer, db.ForeignKey('csv_file.id'), nullable=False)
    
    # New columns for lock management
    lock_time = db.Column(db.DateTime, nullable=True)
    in_progress_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Specify 'overlaps' to avoid relationship conflict
    csv_file = relationship("CSVFile", back_populates="reviews", overlaps="csv_file_assoc")