from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from extensions import db  # Import db from extensions, not app
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
# Define roles
DEVELOPER_ROLE = 'Developer'
ANNOTATOR_ROLE = 'Annotator'

# # Define CSVFileInvite class first (before CSVFile class)
# class CSVFileInvite(db.Model):
#     __tablename__ = 'csv_file_invite'  # Add table name explicitly if missing
#     id = db.Column(db.Integer, primary_key=True)
#     csv_file_id = db.Column(db.Integer, db.ForeignKey('csv_file.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     invited_at = db.Column(db.DateTime, default=datetime.utcnow)

#     # Define relationships to CSVFile and User
#     csv_file = db.relationship('CSVFile', back_populates='csv_file_invites')
#     user = db.relationship('User', back_populates='csv_file_invites_list')


# # Define User class
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     department = db.Column(db.String(50))
#     completed_courses = db.Column(db.String(150))
#     experience_years = db.Column(db.Integer)
#     password = db.Column(db.String(150), nullable=False)
#     role = db.Column(db.String(50), nullable=False, default='Annotator')  # Role field
#     is_verified = db.Column(db.Boolean, default=False)  # Field for OTP verification flag

#     # Password hashing methods
#     def set_password(self, password):
#         self.password = generate_password_hash(password)
    
#     def check_password(self, password):
#         return check_password_hash(self.password, password)

#     # Relationship to invited csv_files
#     csv_file_invites_list = db.relationship('CSVFileInvite', back_populates='user')

#     # Fix the many-to-many relationship
#     invited_files = db.relationship('CSVFile', secondary='csv_file_invite', back_populates='invited_annotators')




# # Define CSVFile class
# class CSVFile(db.Model):
#     __tablename__ = 'csv_file'  # Add this line explicitly if missing
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(150), nullable=False)
#     uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     is_active = db.Column(db.Boolean, default=True)

#     # Relationships
#     uploader = db.relationship('User', backref='uploaded_files', lazy=True)
#     reviews = db.relationship('Review', backref='csv_file_assoc', lazy=True)

#     # Relationship to invited annotators
#     csv_file_invites = db.relationship('CSVFileInvite', back_populates='csv_file')

#     # Correct way to reference invited annotators
#     invited_annotators = db.relationship('User', secondary='csv_file_invite', back_populates='invited_files')



# class Annotation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     annotation = db.Column(db.String(50))
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
#     is_final = db.Column(db.Boolean, default=False)  # New flag to mark annotation as final


# class CompletedReview(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     csv_file_id = db.Column(db.Integer, db.ForeignKey('csv_file.id'), nullable=False)  # Add this line
#     annotator_1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     annotation_1 = db.Column(db.Text)
#     annotator_2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     annotation_2 = db.Column(db.Text)
#     annotator_3_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     annotation_3 = db.Column(db.Text)
#     completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


# class Review(db.Model):
#     __tablename__ = 'review'
#     __table_args__ = {'extend_existing': True}

#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     annotation_count = db.Column(db.Integer, default=0)
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
#     csv_file_id = db.Column(db.Integer, db.ForeignKey('csv_file.id'), nullable=False)
#     completed = db.Column(Boolean, default=False)  # Add column to mark review as completed
    
#     # New columns for lock management
#     lock_time = db.Column(db.DateTime, nullable=True)
#     in_progress_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

#     # Specify 'overlaps' to avoid relationship conflict
#     csv_file = relationship("CSVFile", back_populates="reviews", overlaps="csv_file_assoc")
class CSVFileInvite(db.Model):
    __tablename__ = 'csv_file_invite'
    id = db.Column(db.Integer, primary_key=True)
    csv_file_id = db.Column(db.Integer, db.ForeignKey('csv_file.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    invited_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime, nullable=True)

    csv_file = db.relationship('CSVFile', back_populates='csv_file_invites', overlaps="invited_annotators")
    user = db.relationship('User', back_populates='csv_file_invites_list', overlaps="invited_files")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    department = db.Column(db.String(50))
    completed_courses = db.Column(db.String(150))
    experience_years = db.Column(db.Integer)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Annotator')
    is_verified = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    csv_file_invites_list = db.relationship('CSVFileInvite', back_populates='user', overlaps="invited_files")
    invited_files = db.relationship('CSVFile', secondary='csv_file_invite', back_populates='invited_annotators', overlaps="csv_file_invites_list")
    # Feedback the developer has submitted on model annotations
    feedbacks = db.relationship(
        'DeveloperFeedback',
        back_populates='user',
        cascade='all, delete-orphan'
    )

# class CSVFile(db.Model):
#     __tablename__ = 'csv_file'
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(150), nullable=False)
#     uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     is_active = db.Column(db.Boolean, default=True)

#     uploader = db.relationship('User', backref='uploaded_files', lazy=True)
#     reviews = db.relationship('Review', backref='csv_file_assoc', lazy=True, overlaps="csv_file")

#     csv_file_invites = db.relationship('CSVFileInvite', back_populates='csv_file', overlaps="invited_annotators")
#     invited_annotators = db.relationship('User', secondary='csv_file_invite', back_populates='invited_files', overlaps="csv_file,csv_file_invites")
class CSVFile(db.Model):
    __tablename__ = 'csv_file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # NEW: Flag to track if model annotation is done
    # model_annotation_done = db.Column(db.Boolean, default=False)

    uploader = db.relationship('User', backref='uploaded_files', lazy=True)
    reviews = db.relationship('Review', backref='csv_file_assoc', lazy=True, overlaps="csv_file")

    csv_file_invites = db.relationship('CSVFileInvite', back_populates='csv_file', overlaps="invited_annotators")
    invited_annotators = db.relationship('User', secondary='csv_file_invite', back_populates='invited_files', overlaps="csv_file,csv_file_invites")

# Define roles
DEVELOPER_ROLE = 'Developer'
ANNOTATOR_ROLE = 'Annotator'

# Define CSVFile class
# class CSVFile(db.Model):
#     __tablename__ = 'csv_file'  # Table name
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(150), nullable=False)
#     uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     is_active = db.Column(db.Boolean, default=True)

#     # Relationships
#     uploader = db.relationship('User', backref='uploaded_files', lazy=True)
#     reviews = db.relationship('Review', backref='csv_file_assoc', lazy=True)

#     # Relationship to invited annotators
#     csv_file_invites = db.relationship('CSVFileInvite', back_populates='csv_file')

#     # Correct way to reference invited annotators
#     invited_annotators = db.relationship('User', secondary='csv_file_invite', back_populates='invited_files')


class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    annotation = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_final = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='pending')

    # ✅ Add this relationship
    review = db.relationship('Review', backref='annotations')
    # All “not agree” clicks against this annotation
    developer_feedbacks = db.relationship(
        'DeveloperFeedback',
        back_populates='annotation',
        cascade='all, delete-orphan'
    )



class CompletedReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    csv_file_id = db.Column(db.Integer, db.ForeignKey('csv_file.id'), nullable=False)  
    annotator_1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    annotation_1 = db.Column(db.Text)
    annotator_2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    annotation_2 = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Review(db.Model):
    __tablename__ = 'review'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    annotation_count = db.Column(db.Integer, default=0)  # Track the annotation count
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    csv_file_id = db.Column(db.Integer, db.ForeignKey('csv_file.id'), nullable=False)
    completed = db.Column(Boolean, default=False)  # Mark review as completed

    # New columns for lock management
    lock_time = db.Column(db.DateTime, nullable=True)
    in_progress_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Specify 'overlaps' to avoid relationship conflict
    csv_file = relationship("CSVFile", back_populates="reviews", overlaps="csv_file_assoc")

class DeveloperFeedback(db.Model):
    __tablename__ = 'developer_feedback'
    id = db.Column(db.Integer, primary_key=True)

    # which model‐generated annotation the dev is disagreeing with
    annotation_id = db.Column(
        db.Integer,
        db.ForeignKey('annotation.id'),
        nullable=False
    )

    # which developer clicked “not agree”
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.utcnow()
    )

    # relationships back to Annotation and User
    annotation = db.relationship(
        'Annotation',
        back_populates='developer_feedbacks'
    )
    user = db.relationship(
        'User',
        back_populates='feedbacks'
    )