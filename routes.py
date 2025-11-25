# routes.py
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db, mail, socketio
from models import User, Review, Annotation, CompletedReview, CSVFile, CSVFileInvite, DeveloperFeedback, DEVELOPER_ROLE, ANNOTATOR_ROLE
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from sqlalchemy import and_
from datetime import datetime, timedelta
from sqlalchemy import or_
from flask import send_file
import io
from datetime import datetime, timezone
from flask import request, flash, redirect, url_for, render_template
import threading
from concurrent.futures import ThreadPoolExecutor
from google_play_scraper import reviews
from google_play_scraper.exceptions import NotFoundError
from flask import flash, send_file, request
from google_play_scraper import Sort
import requests
import logging
from functools import wraps
from flask import abort
from flask import session
import pickle
import re
import types
import dill
from model_loader import model
import os
from custom_transformers import OptimalSVD, BinaryToMulticlassPipeline, Word2VecTransformer
import dill
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from sqlalchemy.exc import IntegrityError
from flask_socketio import emit
import string
import random
from forms import LoginForm,OTPForm,AnnotationForm,ScrapeReviewsForm, InviteAnnotatorsForm ,  UploadCSVForm# Import the LoginForm class
from model_loader import model
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Response 
import time 
# import chardet
# Initialize model variable
model = None
vectorizer = None

main = Blueprint('main', __name__, template_folder='templates')

print_lock = threading.Lock()

SERP_API_KEY = "f7119f53588ef98d5c237d2d0f09777d4fe32afd7410e94c3b1c86cfa1bdcbd0"
# Define the path to the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'SVM_noSVD_8651_121374.dill')

# try:
#     with open(MODEL_PATH, 'rb') as file:
#         model = pickle.load(file)
#     print("[INFO] Model loaded successfully.")
# except Exception as e:
#     print("[ERROR] Failed to load model:", e)
#     model = None
# Lazy-load the model
def load_model():
    global model
    if model is None:  # Only load the model if it's not already loaded
        try:
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            print("[INFO] Model loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to load model pipeline: {e}")
            model = None
    return model


from sklearn.metrics import cohen_kappa_score



def send_invitation_email(user_email, csv_file_id):
    msg = Message("Invitation to Annotate Reviews", recipients=[user_email])
    msg.body = f"You have been invited to annotate reviews for the file with ID {csv_file_id}. Please register to access the file."
    mail.send(msg)

def preprocess_review(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'@[^\s]+', ' ', text)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower().strip()




def safe_print(message):
    """Thread-safe printing to the console."""
    with print_lock:
        print(message)

logger = logging.getLogger(__name__)




def validate_date(date_str):
    if not date_str:  # Handle missing date input
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role != role:
                flash("Unauthorized access.")
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return wrapped
    return decorator

def parse_review_date(date_str):
    """Parse a date string using multiple possible formats."""
    for fmt in ("%B %d, %Y", "%b %d, %Y"):  # Handles both full and abbreviated month names
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str}")







def scrape_google_play_reviews(app_id, start_date, end_date, lang='en', country='us', count=100):
    base_url = "https://serpapi.com/search"
    reviews = []
    total_fetched = 0
    next_page_token = None
    seen_contents = set()  # Track unique review content

    while total_fetched < count:
        params = {
            "engine": "google_play_product",
            "product_id": app_id,
            "hl": lang,
            "gl": country,
            "api_key": SERP_API_KEY,
            "store": "apps",
        }
        if next_page_token:
            params["next_page_token"] = next_page_token

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"API Error: {response.status_code} | {response.text}")
            break

        data = response.json()
        if "error" in data:
            print(f"API Error: {data['error']}")
            break

        if "reviews" not in data or not data["reviews"]:
            print("No reviews found in this page.")
            break

        for review in data["reviews"]:
            try:
                review_date = parse_review_date(review.get("date", ""))
                print(f"Review Date: {review_date}")
                if start_date <= review_date <= end_date:
                    content = review.get("snippet", "").strip()
                    if content and content not in seen_contents:
                        seen_contents.add(content)
                        reviews.append({
                            "author": review.get("title", ""),
                            "content": content,
                            "rating": review.get("rating", ""),
                            "date": review_date.strftime('%Y-%m-%d'),
                        })
                        total_fetched += 1
            except ValueError:
                print(f"Skipping review due to date parsing error: {review.get('date')}")

        next_page_token = data.get("serpapi_pagination", {}).get("next_page_token")
        if not next_page_token:
            print("No next page token; exiting pagination.")
            break

    return pd.DataFrame(reviews)




from google_play_scraper import reviews, Sort

def fetch_reviews_by_date(app_id, start_date, end_date, max_count=200):
    all_reviews = []
    seen_contents = set()
    next_token = None

    while len(all_reviews) < max_count:
        result, next_token = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=100,
            continuation_token=next_token
        )

        for r in result:
            review_date = r['at'].date()
            content = r['content'].strip()

            if review_date < start_date:
                return pd.DataFrame(all_reviews)

            if start_date <= review_date <= end_date and content not in seen_contents:
                seen_contents.add(content)
                all_reviews.append({
                    "userName": r['userName'],
                    "score": r['score'],
                    "content": content,
                    "date": review_date.strftime('%Y-%m-%d'),
                })

        if not next_token:
            break

    return pd.DataFrame(all_reviews)




from forms import ScrapeReviewsForm  # make sure this import is present
from collections import Counter

def calculate_kappa(annotations_annotator_1, annotations_annotator_2):
    # Step 1: Calculate observed agreement (Po)
    agreements = sum([1 for a1, a2 in zip(annotations_annotator_1, annotations_annotator_2) if a1 == a2])
    total_reviews = len(annotations_annotator_1)
    Po = agreements / total_reviews

    # Step 2: Calculate expected agreement (Pe)
    # Count the frequency of each category for both annotators
    count_a1 = Counter(annotations_annotator_1)
    count_a2 = Counter(annotations_annotator_2)

    p1 = count_a1["Privacy-related feature request"] / total_reviews
    p2 = count_a1["Privacy-related bug report"] / total_reviews
    p3 = count_a1["Privacy-irrelevant"] / total_reviews

    p1_ = count_a2["Privacy-related feature request"] / total_reviews
    p2_ = count_a2["Privacy-related bug report"] / total_reviews
    p3_ = count_a2["Privacy-irrelevant"] / total_reviews

    Pe = (p1 * p1_) + (p2 * p2_) + (p3 * p3_)

    kappa = (Po - Pe) / (1 - Pe)
    return round(kappa, 4)

@main.route('/')
@login_required
def home():
    scrape_form = ScrapeReviewsForm()
    invite_form = InviteAnnotatorsForm()
    upload_form = UploadCSVForm()

    if current_user.role == DEVELOPER_ROLE:
        csv_files = CSVFile.query.filter_by(is_active=True, uploaded_by=current_user.id).all()

        file_progress_data = []
        for file in csv_files:
      
            total = Review.query.filter_by(csv_file_id=file.id).count()
            done = Review.query.filter_by(csv_file_id=file.id, annotation_count=2).count()  # ✅ Done = 2 annotations
            by_2 = done  # ✅ All done are by 2 users now
            by_1 = Review.query.filter_by(csv_file_id=file.id, annotation_count=1).count()
            percent = (done / total * 100) if total else 0

            # Retrieve the user ids for all annotators for this file
            annotators = [annotator.user_id for annotator in Annotation.query.filter(Review.csv_file_id == file.id).join(Review).distinct()]

            # Collect annotations for all annotators
            annotations = {user_id: [] for user_id in annotators}

            for annotator in annotators:
                annotations[annotator] = [annotation.annotation for annotation in Annotation.query.filter(
                    Annotation.user_id == annotator, Review.csv_file_id == file.id).join(Review).all()]

            # Calculate Kappa between all pairs of annotators
            kappa_values = {}
            for annotator_1 in annotators:
                for annotator_2 in annotators:
                    if annotator_1 < annotator_2:  # To avoid duplicates (since kappa is symmetric)
                        kappa = calculate_kappa(annotations[annotator_1], annotations[annotator_2])
                        kappa_values[(annotator_1, annotator_2)] = kappa

            assigned_users = [invite.user.name for invite in file.csv_file_invites]
            
            file_progress_data.append({
                'file': file,
                'total': total,
                'done': done,
                'by_2': by_2,
                'by_1': by_1,
                'percent': percent,
                'kappa_values': kappa_values,
                'assigned_users': assigned_users,
               
            })


        return render_template(
            'home.html',
            upload_form=upload_form,
            developer_view=True,
            file_progress_data=file_progress_data,
            form=scrape_form,
            invite_form=invite_form,
            file_name=session.get('file_name')
        )

    elif current_user.role == ANNOTATOR_ROLE:
        invited_files = [f for f in current_user.invited_files if f.is_active]  # ✅ Only active files

        user_annotation_counts = {}
        for csv_file in invited_files:
            total_reviews = Review.query.filter_by(csv_file_id=csv_file.id).count()
            user_count = Annotation.query.join(Review).filter(
                Annotation.user_id == current_user.id,
                Review.csv_file_id == csv_file.id
            ).count()
            completed = user_count == total_reviews

            user_annotation_counts[csv_file.id] = {
                'count': user_count,
                'completed': completed
            }

        return render_template(
            'home.html',
            developer_view=False,
            csv_files=invited_files,
            user_annotation_counts=user_annotation_counts
        )

    else:
        flash("Unauthorized access.")
        return redirect(url_for('main.login'))







# Helper function to generate OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))  # 6-digit OTP

# Helper function to send OTP email
def send_otp_email(user_email, otp):
    msg = Message("Your OTP Code", recipients=[user_email])
    msg.body = f"Your OTP code is {otp}. It will expire in 5 minutes."
    mail.send(msg)


from forms import RegistrationForm


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Get data from the form
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        role = form.role.data

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('main.login'))

        # Generate OTP and send email
        otp = generate_otp()
        send_otp_email(email, otp)

        # Save the OTP and timestamp in the session
        session['otp'] = otp
        session['otp_expiry'] = datetime.utcnow() + timedelta(minutes=5)
        session['user_data'] = {'name': name, 'email': email, 'password': password, 'role': role}

        print(f"DEBUG: OTP is {session['otp']} and expires at {session['otp_expiry']}")  # Add this line to check OTP in session
        return redirect(url_for('main.verify_otp'))

    return render_template('register.html', form=form)



@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create the form instance

    if form.validate_on_submit():  # Check if the form is valid on POST request
        email = form.email.data  # Access form fields using form.field_name
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()  # Query the user by email
        
        if user and check_password_hash(user.password, password):  # Check password
            # Check if the user has verified their OTP
            if not user.is_verified:  # Assuming `is_verified` field is in the User model
                flash('Please verify your OTP first before logging in.')
                return redirect(url_for('main.verify_otp'))  # Redirect to OTP verification page

            login_user(user)  # Log the user in
            print("User authenticated:", current_user.is_authenticated)
            print("User role:", user.role)

            if user.role == 'Developer':
                print("Redirecting to home page")
                return redirect(url_for('main.home'))  # Redirect to home for developers
            elif user.role == 'Annotator':
                print("Redirecting to annotation page")
                return redirect(url_for('main.csv_files'))  # Redirect to annotation page for annotators
        else:
            flash('Login failed. Check your email and password and try again.')

    return render_template('login.html', form=form)  # Pass the form to the template



@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

from forms import UploadCSVForm  # Make sure this is imported

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.role != DEVELOPER_ROLE:
        return redirect(url_for('main.home'))

    form = UploadCSVForm()

    if form.validate_on_submit():
        file = form.file.data

        if not file or file.filename == '':
            flash("No file selected for upload.")
            return redirect(url_for('main.upload'))

        if not (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
            flash("Please upload a valid .xlsx or .csv file.")
            return redirect(url_for('main.upload'))

        try:
            if file.filename.endswith('.xlsx'):
                print("Processing .xlsx file")
                data = pd.read_excel(file, engine='openpyxl')
            elif file.filename.endswith('.csv'):
                print("Processing .csv file")
                data = pd.read_csv(file)

            # Standardize column names for easier matching
            data.columns = [str(col).strip().lower() for col in data.columns]

            # Try to locate a "content" column first
            if "content" in data.columns:
                print("Using 'content' column")
                content_only = data["content"].dropna().astype(str).tolist()
            elif data.shape[1] >= 3:
                print("No 'content' column found. Using 3rd column as fallback.")
                content_only = data.iloc[:, 2].dropna().astype(str).tolist()
            else:
                flash("CSV must include a 'content' column or at least 3 columns (with reviews in the 3rd).", "danger")
                return redirect(url_for('main.upload'))

            # Save file and reviews
            csv_file = CSVFile(filename=file.filename, uploaded_by=current_user.id)
            db.session.add(csv_file)
            db.session.flush()

            for review_text in content_only:
                db.session.add(Review(text=review_text, csv_file_id=csv_file.id))

            db.session.commit()
            flash(f"{len(content_only)} reviews processed and uploaded for annotation.", "success")
            return redirect(url_for('main.home'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error processing file: {e}", "danger")
            print(f"[UPLOAD ERROR] {e}")
            return redirect(url_for('main.upload'))



    return render_template('upload.html', form=form)


@main.route('/csv_files')
@login_required
def csv_files():
    print("Template Path:", os.path.abspath("templates/csv_files_dev.html"))

    if current_user.role == ANNOTATOR_ROLE:
        # Fetch files the annotator is invited to and active
        invited_files = CSVFile.query.join(CSVFileInvite).filter(
            CSVFileInvite.user_id == current_user.id,
            CSVFile.is_active == True
        ).all()
        print(f"[DEBUG] {current_user.email} invited files: {[f.filename for f in invited_files]}")

        user_annotation_counts = {}
        for csv_file in invited_files:
            total_reviews = Review.query.filter_by(csv_file_id=csv_file.id).count()
            user_count = Annotation.query.join(Review).filter(
                Annotation.user_id == current_user.id,
                Review.csv_file_id == csv_file.id
            ).count()
            completed = user_count == total_reviews  # Change to 2 annotators' condition
            user_annotation_counts[csv_file.id] = {
                'count': user_count,
                'completed': completed
            }

        return render_template(
            'csv_files.html',
            csv_files=invited_files,
            user_annotation_counts=user_annotation_counts
        )

    elif current_user.role == DEVELOPER_ROLE:
        print("Template Path:", os.path.join(main.template_folder, 'csv_files_dev.html'))

        # Developer sees all active files
        csv_files = CSVFile.query.filter_by(is_active=True).all()

        file_progress_data = []
        for csv_file in csv_files:
            total_reviews = Review.query.filter_by(csv_file_id=csv_file.id).count()
            completed_reviews = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=2).count()  # Only count reviews annotated by exactly 2 annotators
            annotated_by_2_users = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=2).count()  # Count reviews annotated by 2 users
            annotated_by_1_user = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=1).count()
            progress_percentage = (completed_reviews / total_reviews * 100) if total_reviews > 0 else 0

            file_progress_data.append({
                'file': csv_file,
                'total_reviews': total_reviews,
                'completed_reviews': completed_reviews,
                'annotated_by_2_users': annotated_by_2_users,
                'annotated_by_1_user': annotated_by_1_user,
                'progress_percentage': progress_percentage,
                'uploader_name': csv_file.uploader.name if csv_file.uploader else "Unknown"
            })

        return render_template('csv_files_dev.html', file_progress_data=file_progress_data)

    else:
        flash("Unauthorized access.")
        return redirect(url_for('main.home'))





@main.route('/annotate_csv/<int:csv_file_id>', methods=['GET', 'POST'])
@login_required
def annotate_csv(csv_file_id):
    # Check if the current user is an annotator
    if current_user.role != ANNOTATOR_ROLE:
        return redirect(url_for('main.home'))

    # Fetch the CSV file, only allow annotation if it is active
    csv_file = CSVFile.query.filter_by(id=csv_file_id, is_active=True).first()

    if not csv_file:
        flash("This file is no longer active or available for annotation.")
        return redirect(url_for('main.csv_files'))

    # Proceed with the rest of the annotation flow...


    # Lock expired time (e.g., 2 minutes)
    lock_expire_time = datetime.now(timezone.utc) - timedelta(minutes=2)

    # Release locks that have expired
    Review.query.filter(Review.lock_time < lock_expire_time).update({"in_progress_by": None, "lock_time": None})
    db.session.commit()

    # Fetch reviews not yet annotated by the current user
    annotated_review_ids = [annotation.review_id for annotation in Annotation.query.filter_by(user_id=current_user.id).all()]

    review = (Review.query
            .filter(and_(
                Review.csv_file_id == csv_file_id,
                Review.id.notin_(annotated_review_ids),
                Review.annotation_count < 2,  # ✅ now using 2
                or_(Review.in_progress_by == None, Review.in_progress_by == current_user.id)))
            .order_by(Review.annotation_count)
            .first())

    # Check if a review is available
    if review:
        # Lock review for this user
        review.in_progress_by = current_user.id
        review.lock_time = datetime.now(timezone.utc)
        db.session.commit()

        # Create the form instance
        form = AnnotationForm()

        # Handle form submission
        if form.validate_on_submit():
            # Save the annotation
            annotation_text = form.annotation.data
            new_annotation = Annotation(
                review_id=review.id,
                user_id=current_user.id,
                annotation=annotation_text
            )
            db.session.add(new_annotation)
            review.annotation_count += 1  # Update the annotation count for the review

            # Mark as completed if 3 annotations are made
            if review.annotation_count == 2:  # ✅ instead of 3
                review.completed = True

            db.session.commit()

            # Redirect to the next review
            flash("Annotation submitted successfully!")
            return redirect(url_for('main.annotate_csv', csv_file_id=csv_file_id))

        # Calculate the annotation count for the current user on this CSV file
        annotation_count = Annotation.query.join(Review).filter(
            Annotation.user_id == current_user.id,
            Review.csv_file_id == csv_file_id
        ).count()

        # Render the annotation template
        return render_template('annotation.html', review=review, csv_file_id=csv_file_id, annotation_count=annotation_count, form=form)

    else:
        # No more reviews available for annotation in this file
        flash("No more reviews available for annotation in this file.")
        return redirect(url_for('main.csv_files'))


@main.route('/submit_annotation', methods=['POST'])
@login_required
def submit_annotation():
    review_id = request.form.get('review_id')
    annotation_text = request.form.get('annotation')
    csv_file_id = request.form.get('csv_file_id')

    review = Review.query.filter_by(id=review_id).with_for_update().first()

    if not review:
        flash("This review is no longer available for annotation.")
        return redirect(url_for('main.csv_files'))

    # Save the annotation
    new_annotation = Annotation(
        review_id=review.id,
        user_id=current_user.id,
        annotation=annotation_text
    )
    db.session.add(new_annotation)

    # Update review metadata
    review.annotation_count += 1
    review.in_progress_by = None
    review.lock_time = None

    # Only proceed if this makes the second annotation
    if review.annotation_count == 2:
        review.completed = True

        # Get the two most recent annotations by different users
        annotations = Annotation.query.filter_by(review_id=review.id).order_by(Annotation.created_at).all()

        if len(annotations) >= 2:
            user_ids = set([a.user_id for a in annotations])
            if len(user_ids) >= 2:
                # Use first two distinct-user annotations
                first = annotations[0]
                second = next((a for a in annotations if a.user_id != first.user_id), None)

                if second:
                    # Ensure not already created
                    existing = CompletedReview.query.filter_by(text=review.text, csv_file_id=review.csv_file_id).first()
                    if not existing:
                        completed = CompletedReview(
                            text=review.text,
                            annotator_1_id=first.user_id,
                            annotation_1=first.annotation,
                            annotator_2_id=second.user_id,
                            annotation_2=second.annotation,
                            csv_file_id=review.csv_file_id
                        )
                        db.session.add(completed)

    try:
        db.session.commit()
        flash("Annotation submitted successfully!")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}")

    return redirect(url_for('main.annotate_csv', csv_file_id=csv_file_id))




@main.route('/check_csv_files')
def check_csv_files():
    csv_files = CSVFile.query.filter_by(is_active=True).all()

    for file in csv_files:
        print("CSV File:", file.filename)
    return "Check your console for CSV files."




@main.route('/check_review_counts')
def check_review_counts():
    # Query all CSV files and check associated reviews
    csv_files = CSVFile.query.filter_by(is_active=True).all()

    review_data = []
    for file in csv_files:
        # Count reviews linked to each CSV file
        review_count = Review.query.filter_by(csv_file_id=file.id).count()
        review_data.append((file.filename, file.id, review_count))
        print(f"CSV File: {file.filename} (ID: {file.id}) has {review_count} associated reviews.")
    return "Check the console output for CSV file review counts."


# routes.py
@main.route('/track_progress/<int:csv_file_id>')
@login_required
def track_progress(csv_file_id):
    # Fetch the CSV file
    csv_file = CSVFile.query.filter_by(id=csv_file_id, is_active=True).first()

    if not csv_file:
        flash("This file is no longer active.")
        return redirect(url_for('main.csv_files'))

    # Count total reviews in the file
    total_reviews = Review.query.filter_by(csv_file_id=csv_file_id).count()

    # Updated logic for 2 annotators
    completed_reviews = Review.query.filter_by(csv_file_id=csv_file_id, annotation_count=2).count()
    annotated_by_2_users = completed_reviews  # same meaning now
    annotated_by_1_user = Review.query.filter_by(csv_file_id=csv_file_id, annotation_count=1).count()

    # Calculate progress based on 2 annotations (not 3)
    progress_percentage = (completed_reviews / total_reviews * 100) if total_reviews > 0 else 0

    return render_template(
        'track_progress.html',
        csv_file=csv_file,
        total_reviews=total_reviews,
        completed_reviews=completed_reviews,
        annotated_by_2_users=annotated_by_2_users,
        annotated_by_1_user=annotated_by_1_user,
        progress_percentage=progress_percentage
    )


from flask import send_file
import pandas as pd
import io

@main.route('/download_annotated_csv/<int:csv_file_id>', methods=['GET'])
@login_required
def download_annotated_csv(csv_file_id):
    csv_file = CSVFile.query.get_or_404(csv_file_id)

    completed_reviews = CompletedReview.query.filter_by(csv_file_id=csv_file_id).all()
    
    if not completed_reviews:
        flash("No completed reviews found for this file.", "danger")
        print(f"[DEBUG] No CompletedReview entries for file ID {csv_file_id}")
        return redirect(url_for('main.home'))

    data = [{
        'Review Text': review.text,
        'Annotation 1': review.annotation_1,
        'Annotation 2': review.annotation_2
    } for review in completed_reviews]

    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name=f"{csv_file.filename}_annotated.csv",
        mimetype='text/csv'
    )





@main.route('/delete_files', methods=['POST'])
@login_required
def delete_files():
    if current_user.role != DEVELOPER_ROLE:
        flash("Unauthorized access.")
        return redirect(url_for('main.csv_files'))

    # Get the list of file IDs to delete
    file_ids = request.form.getlist('delete_files')

    # Update only files uploaded by the current user
    files_to_update = CSVFile.query.filter(CSVFile.id.in_(file_ids), CSVFile.uploaded_by == current_user.id).all()
    if not files_to_update:
        flash("No files selected or you cannot delete files you did not upload.")
        return redirect(url_for('main.csv_files'))

    # Mark the files as inactive
    for file in files_to_update:
        file.is_active = False

    db.session.commit()
    flash(f"{len(files_to_update)} file(s) marked as inactive successfully.")
    return redirect(url_for('main.home'))


import os
from flask import current_app
from datetime import datetime
from flask import make_response
import io
import csv
from datetime import datetime
from flask import current_app  # already imported if you're using Flask

@main.route('/scrape_reviews', methods=['GET', 'POST'])
@login_required
@role_required(DEVELOPER_ROLE)
def scrape_reviews():
    form = ScrapeReviewsForm()

    if form.validate_on_submit():
        app_id = form.app_id.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()

        if start_date > end_date:
            flash("Start date cannot be after end date.")
            return redirect(url_for('main.home'))

        try:
            reviews_df = fetch_reviews_by_date(app_id, start_date, end_date)

            if reviews_df.empty:
                flash("No reviews found for the given parameters.")
                return redirect(url_for('main.home'))

            output = io.StringIO()
            reviews_df.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)

            filename = f"{app_id}_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
            response.headers["Content-Type"] = "text/csv"
            return response

        except Exception as e:
            flash(f"An error occurred while scraping: {str(e)}")
            return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))


@main.route('/save_temp_file')
def save_temp_file():
    # Example of saving a file to the TEMP_FOLDER
    temp_file_path = os.path.join(current_app.config['TEMP_FOLDER'], 'example.csv')
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write('Sample data for temporary file')

    return f"File saved at {temp_file_path}"


@main.route('/download', methods=['POST'])
@login_required
def download_file():
    file_path = session.get('file_path')
    file_name = session.get('file_name')

    if not file_path or not os.path.exists(file_path):
        flash("No file available for download.")
        return redirect(url_for('main.scrape_reviews'))

    return send_file(
        file_path,
        as_attachment=True,
        download_name=file_name,
        mimetype='text/csv'
    )


@main.route('/model_annotation/<int:csv_file_id>', methods=['POST'])
@login_required
@role_required(DEVELOPER_ROLE)
def model_annotation(csv_file_id):
    print(f"[DEBUG] Received request to annotate file ID: {csv_file_id}")
    
    from model_loader import model  # Ensure you're importing the correct pipeline

    if not model:
        print("[ERROR] Model not loaded.")
        return "Model not loaded", 500

    print("✅ model_annotation endpoint hit for file_id", csv_file_id)

    file = CSVFile.query.get_or_404(csv_file_id)
    reviews = Review.query.filter_by(csv_file_id=csv_file_id, completed=False).all()

    if not reviews:
        flash("No unannotated reviews found.", "warning")
        return "", 204  # No content

    try:
        texts = [r.text for r in reviews]
        predictions = model.predict(texts)

        label_map = {
            0: "Privacy-related feature request",
            1: "Privacy-related bug report",
            2: "Privacy-irrelevant"
        }

        for review, pred in zip(reviews, predictions):
            db.session.add(Annotation(
                review_id=review.id,
                user_id=current_user.id,
                annotation=label_map.get(pred, str(pred)),
                is_final=True,
                status='model'
            ))
            review.completed = True


        db.session.commit()
        print(f"[INFO] Annotated {len(reviews)} reviews successfully.")
        return "", 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed model annotation: {e}")
        return f"Server Error: {e}", 500


@main.route('/start_annotation/<int:csv_file_id>', methods=['GET'])
@login_required
@role_required('Developer')
def start_annotation(csv_file_id):
    # Render the intermediate page for annotation
    return render_template('start_annotation.html', csv_file_id=csv_file_id)


@main.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    form = OTPForm()  # Initialize the OTPForm

    if form.validate_on_submit():  # Check if the form is submitted and valid
        entered_otp = form.otp.data  # Access the OTP from the form

        # Debug: Log the OTP entered and stored OTP
        print(f"DEBUG: Entered OTP: {entered_otp}")  # Log the entered OTP
        if 'otp' in session:
            otp = session['otp']
            print(f"DEBUG: Stored OTP: {otp}")  # Log the OTP stored in session

            # Get the expiry time and make it timezone-aware
            otp_expiry = session.get('otp_expiry')
            if otp_expiry and datetime.utcnow().replace(tzinfo=timezone.utc) > otp_expiry:
                flash('OTP expired. Please try registering again.')
                return redirect(url_for('main.register'))

            # Compare the entered OTP with the session OTP
            if entered_otp == otp:
                user_data = session.get('user_data')
                if user_data:
                    # Check if the user already exists (to avoid duplicate users)
                    existing_user = User.query.filter_by(email=user_data['email']).first()
                    if existing_user:
                        flash('User with this email already exists.')
                        return redirect(url_for('main.login'))

                    # Create a new user and mark them as verified
                    new_user = User(name=user_data['name'], email=user_data['email'], password=user_data['password'], role=user_data['role'], is_verified=True)
                    db.session.add(new_user)
                    db.session.commit()

                    # Clear OTP session data after successful registration
                    session.pop('otp', None)
                    session.pop('otp_expiry', None)
                    session.pop('user_data', None)

                    flash('Registration successful! You can now log in.')
                    return redirect(url_for('main.login'))
                else:
                    flash('Error: User data not found. Please try again.')
            else:
                flash('Invalid OTP. Please try again.')

        else:
            flash('No OTP found. Please register again.')

    return render_template('verify_otp.html', form=form)  # Pass the form to the template

from flask import flash

@main.route('/invite_annotators/<int:csv_file_id>', methods=['POST'])
@login_required
@role_required(DEVELOPER_ROLE)
def invite_annotators(csv_file_id):
    form = InviteAnnotatorsForm(request.form)
    
    # Check if the form is valid
    if not form.validate_on_submit():
        flash("Invalid form submission.", "danger")
        return redirect(url_for('main.home'))

    # Fetch the CSV file to check its current invited annotators
    csv_file = CSVFile.query.get_or_404(csv_file_id)
    
    # Ensure the current user is the uploader
    if csv_file.uploaded_by != current_user.id:
        flash("You can only invite annotators for your own files.", "danger")
        return redirect(url_for('main.home'))

    # Get emails of the invited annotators
    # Clean up submitted emails
    emails = [email.strip() for email in form.invited_annotators_emails.data.split(',') if email.strip()]

    # Get current annotators already invited for the file
    current_invites = CSVFileInvite.query.filter_by(csv_file_id=csv_file.id).all()
    current_invited_ids = [invite.user_id for invite in current_invites]

    # Count how many are already invited
    if len(current_invited_ids) >= 2:
        flash("You have already invited the maximum of 2 annotators for this file.", "warning")
        return redirect(url_for('main.home'))

    # Check how many new annotators will be added
    new_invites = 0
    for email in emails:
        annotator = User.query.filter_by(email=email).first()
        if annotator and annotator.id not in current_invited_ids:
            new_invites += 1

    if len(current_invited_ids) + new_invites > 2:
        flash("You can only have a maximum of 2 annotators per file. Adjust your invitation list.", "danger")
        return redirect(url_for('main.home'))


    # Invite each annotator and send email
    for email in emails:
        email = email.strip()
        annotator = User.query.filter_by(email=email).first()
        
        if annotator:
            # Ensure the annotator isn't already invited
            existing_invite = CSVFileInvite.query.filter_by(csv_file_id=csv_file.id, user_id=annotator.id).first()
            if not existing_invite:
                invite = CSVFileInvite(csv_file_id=csv_file.id, user_id=annotator.id)
                db.session.add(invite)
                send_invitation_email(email, csv_file.id)
                flash(f"✅ Invitation sent to {email}.", "success")
            else:
                flash(f"⚠️ {email} has already been invited.", "warning")
        else:
            flash(f"❌ No user with email {email} found.", "danger")

    db.session.commit()
    return redirect(url_for('main.home'))

@main.route('/download_model_annotations/<int:csv_file_id>', methods=['GET'])
@login_required
@role_required(DEVELOPER_ROLE)
def download_model_annotations(csv_file_id):
    file = CSVFile.query.get_or_404(csv_file_id)
    annotations = (db.session.query(Annotation)
                   .join(Review)
                   .filter(Review.csv_file_id == csv_file_id,
                           Annotation.status == 'model',
                           Annotation.is_final == True)
                   .all())

    if not annotations:
        flash("No model-generated annotations found for this file.", "warning")
        return redirect(url_for('main.home'))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Review ID', 'Text', 'Annotation'])

    for ann in annotations:
        writer.writerow([ann.review.id, ann.review.text, ann.annotation])

    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=model_annotations_{file.filename}"}
    )


@main.route('/dashboard')
@login_required
def dashboard():
    csv_files = CSVFile.query.filter_by(is_active=True).all()

    user_annotation_counts = {}
    file_progress_data = []

    for file in csv_files:
        # User-specific annotation status
        user_count = Annotation.query.join(Review).filter(
            Annotation.user_id == current_user.id,
            Review.csv_file_id == file.id
        ).count()
        total_reviews = Review.query.filter_by(csv_file_id=file.id).count()
        completed = user_count == total_reviews

        user_annotation_counts[file.id] = {
            'count': user_count,
            'completed': completed
        }

        # Developer file progress — updated to 2-annotator system
        completed_reviews = Review.query.filter_by(csv_file_id=file.id, annotation_count=2).count()
        annotated_by_2 = completed_reviews
        annotated_by_1 = Review.query.filter_by(csv_file_id=file.id, annotation_count=1).count()
        percent = (completed_reviews / total_reviews) * 100 if total_reviews else 0

        file_progress_data.append({
            'file': file,
            'total': total_reviews,
            'done': completed_reviews,
            'by_2': annotated_by_2,
            'by_1': annotated_by_1,
            'percent': percent
        })

    form = ScrapeReviewsForm()

    return render_template('dashboard.html',
                           csv_files=csv_files,
                           user_annotation_counts=user_annotation_counts,
                           file_progress_data=file_progress_data,
                           form=form)

from flask import jsonify

@main.route('/model_annotation_summary/<int:csv_file_id>', methods=['GET'])
@login_required
@role_required(DEVELOPER_ROLE)
def model_annotation_summary(csv_file_id):
    """
    Returns summary counts of annotation categories for ML-annotated reviews
    for the given CSV file (as JSON).
    """
    # Query only model-generated final annotations for this file
    annotations = (Annotation.query
                   .join(Review)
                   .filter(Review.csv_file_id == csv_file_id,
                           Annotation.status == 'model',
                           Annotation.is_final == True)
                   .all())
    total = len(annotations)
    # Counter to count the annotation categories
    from collections import Counter
    counter = Counter([a.annotation for a in annotations])

    # Adjust category names if needed
    summary = {
        "total": total,
        "privacy_irrelevant": counter.get("Privacy-irrelevant", 0),
        "privacy_bug": counter.get("Privacy-related bug report", 0),
        "privacy_feature": counter.get("Privacy-related feature request", 0),

    }
    return jsonify(summary)

from forms import ReviewFeedbackForm  # ← import your new tiny form

# @main.route('/review_feedback/<int:csv_file_id>', methods=['GET','POST'])
# @login_required
# @role_required(DEVELOPER_ROLE)
# def review_feedback(csv_file_id):
#     csv_file = CSVFile.query.get_or_404(csv_file_id)
#     form = ReviewFeedbackForm()

#     # Only proceed if CSRF passes
#     if form.validate_on_submit():
#         # 1) Just picked the dropdown?
#         if 'filter_type' in request.form and 'submit_feedback' not in request.form:
#             filter_type = request.form['filter_type']
#             cats = (
#                 ["Privacy-related bug report","Privacy-related feature request"]
#                 if filter_type=='privacy'
#                 else ["Privacy-irrelevant"]
#             )
#             anns = (Annotation.query
#                     .join(Review)
#                     .filter(
#                         Review.csv_file_id==csv_file_id,
#                         Annotation.status=='model',
#                         Annotation.is_final==True,
#                         Annotation.annotation.in_(cats))
#                     .all())
#             return render_template(
#                 'review_feedback.html',
#                 csv_file=csv_file,
#                 form=form,
#                 annotations=anns,
#                 filter_type=filter_type
#             )

#         # 2) Submitted “not agree” feedback?
#         elif 'submit_feedback' in request.form:
#             disagree_ids = request.form.getlist('not_agree')
#             for ann_id in disagree_ids:
#                 fb = DeveloperFeedback(
#                     annotation_id=int(ann_id),
#                     user_id=current_user.id
#                 )
#                 db.session.add(fb)
#             db.session.commit()
#             flash(f"Recorded feedback for {len(disagree_ids)} reviews.", "success")
#             return redirect(url_for('main.home'))

#     # GET or CSRF failure: show initial dropdown
#     return render_template(
#         'review_feedback.html',
#         csv_file=csv_file,
#         form=form,
#         annotations=None,
#         filter_type=None
#     )
from flask import Response

@main.route('/review_feedback/<int:csv_file_id>', methods=['GET', 'POST'])
@login_required
@role_required(DEVELOPER_ROLE)
def review_feedback(csv_file_id):
    csv_file = CSVFile.query.get_or_404(csv_file_id)
    form = ReviewFeedbackForm()

    if form.validate_on_submit():
        action = request.form.get('action')
        filter_type = request.form.get('filter_type')

        # Determine annotation categories based on filter
        if filter_type == 'privacy':
            cats = ["Privacy-related bug report", "Privacy-related feature request"]
        else:
            cats = ["Privacy-irrelevant"]

        if action == 'load_reviews':
            anns = (Annotation.query
                    .join(Review)
                    .filter(
                        Review.csv_file_id == csv_file_id,
                        Annotation.status == 'model',
                        Annotation.is_final == True,
                        Annotation.annotation.in_(cats))
                    .all())
            return render_template(
                'review_feedback.html',
                csv_file=csv_file,
                form=form,
                annotations=anns,
                filter_type=filter_type
            )

        elif action == 'download':
            anns = (Annotation.query
                    .join(Review)
                    .filter(
                        Review.csv_file_id == csv_file_id,
                        Annotation.status == 'model',
                        Annotation.is_final == True,
                        Annotation.annotation.in_(cats))
                    .all())

            if not anns:
                flash("No annotated reviews found for selected category.", "warning")
                return redirect(url_for('main.review_feedback', csv_file_id=csv_file_id))

            # Prepare CSV data
            output = io.StringIO()
            output.write("Review Text,Annotation\n")
            for ann in anns:
                # Escape quotes and commas if necessary
                text = ann.review.text.replace('"', '""')
                annotation = ann.annotation.replace('"', '""')
                output.write(f'"{text}","{annotation}"\n')
            output.seek(0)

            filename = f"{csv_file.filename}_{filter_type}_annotations.csv"

            return Response(
                output,
                mimetype="text/csv",
                headers={"Content-Disposition": f"attachment;filename={filename}"}
            )

        else:
            flash("Invalid action.", "danger")
            return redirect(url_for('main.review_feedback', csv_file_id=csv_file_id))

    # GET request or initial form display
    return render_template(
        'review_feedback.html',
        csv_file=csv_file,
        form=form,
        annotations=None,
        filter_type=None
    )
