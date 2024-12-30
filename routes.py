# routes.py
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db
from models import User, Review, Annotation, CompletedReview, CSVFile, DEVELOPER_ROLE, ANNOTATOR_ROLE  # Import CSVFile
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



# import chardet

main = Blueprint('main', __name__)

print_lock = threading.Lock()

SERP_API_KEY = "f7119f53588ef98d5c237d2d0f09777d4fe32afd7410e94c3b1c86cfa1bdcbd0"

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

def scrape_google_play_reviews(app_id, start_date, end_date, lang, country, count):
    """Scrape reviews from Google Play using SerpAPI."""
    base_url = "https://serpapi.com/search"
    reviews = []
    next_page_token = None
    total_fetched = 0

    while total_fetched < count:
        params = {
            "engine": "google_play_product",
            "product_id": app_id,
            "hl": lang,
            "gl": country,
            "api_key": SERP_API_KEY,
            "store": "apps",  # Added store parameter
            "next_page_token": next_page_token,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if "error" in data:
            print(f"Error from API: {data['error']}")
            break

        if "reviews" not in data:
            print("No reviews found in response.")
            break

        for review in data.get("reviews", []):
            try:
                review_date = parse_review_date(review.get("date", ""))
                if start_date <= review_date <= end_date:
                    reviews.append({
                        "author": review.get("title", ""),
                        "content": review.get("snippet", ""),
                        "rating": review.get("rating", ""),
                        "date": review.get("iso_date", ""),
                    })
                    total_fetched += 1
                    if total_fetched >= count:
                        break
            except ValueError as e:
                print(f"Failed to parse date: {review.get('date')}, error: {e}")

        next_page_token = data.get("serpapi_pagination", {}).get("next_page_token")
        if not next_page_token:
            break

    df = pd.DataFrame(reviews)
    return df

def fetch_reviews_with_date_filter(app_id, start_date, end_date, lang='en', country='us', count=100):
    try:
        all_reviews = []
        next_page_token = None

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        while len(all_reviews) < count:
            params = {
                "engine": "google_play_product",
                "product_id": app_id,
                "hl": lang,
                "gl": country,
                "api_key": SERP_API_KEY,
                "next_page_token": next_page_token
            }

            print("[DEBUG] Request Params:", params)  # Debug the request parameters

            response = requests.get("https://serpapi.com/search.json", params=params)
            response_data = response.json()

            # Debug API response
            print("[DEBUG] API Response:", response_data)

            if "reviews" not in response_data:
                print("[DEBUG] No reviews found in response.")
                break

            reviews_data = response_data["reviews"]
            filtered_reviews = []

            for review in reviews_data:
                try:
                    review_date = parse_review_date(review["date"])
                    if start_date <= review_date <= end_date:
                        filtered_reviews.append(review)
                except ValueError as e:
                    print(f"[ERROR] Failed to parse date: {review['date']}, error: {e}")

            all_reviews.extend(filtered_reviews)
            print(f"[DEBUG] Total reviews fetched so far: {len(all_reviews)}")

            next_page_token = response_data.get("next_page_token")
            if not next_page_token:
                print("[DEBUG] No next page token, ending pagination.")
                break

        print("[DEBUG] Final fetched reviews count:", len(all_reviews))
        return pd.DataFrame(all_reviews)

    except Exception as e:
        print(f"[ERROR] Failed to fetch reviews: {e}")
        return pd.DataFrame()





@main.route('/')
def home():
    first_csv_file = CSVFile.query.first()

    # Pass a flag for developers to view CSV files
    if current_user.is_authenticated and current_user.role == DEVELOPER_ROLE:
        return render_template('home.html', csv_file_id=first_csv_file.id if first_csv_file else None, developer_view=True)
    else:
        return render_template('home.html', csv_file_id=first_csv_file.id if first_csv_file else None)




@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')



        role = request.form.get('role', ANNOTATOR_ROLE)  # Default to 'Annotator' if no role selected

        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            # Debugging Statements
            print("User authenticated:", current_user.is_authenticated)
            print("User role:", user.role)
            
            # Redirect based on role
            if user.role == DEVELOPER_ROLE:
                print("Redirecting to home page")
                return redirect(url_for('main.home'))
            elif user.role == ANNOTATOR_ROLE:
                print("Redirecting to annotation page")
                return redirect(url_for('main.csv_files'))
        else:
            flash('Login failed. Check your email and password and try again.')
    
    return render_template('login.html')




@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))



@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.role != DEVELOPER_ROLE:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        file = request.files['file']
        if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
            try:
                # Debug: Print filename to confirm upload
                print(f"File uploaded: {file.filename}")
                
                # Load file based on its extension
                if file.filename.endswith('.xlsx'):
                    print("Processing .xlsx file")  # Debug
                    data = pd.read_excel(file, header=None, engine='openpyxl')
                elif file.filename.endswith('.csv'):
                    print("Processing .csv file")  # Debug
                    data = pd.read_csv(file, header=None, encoding="utf-16", errors="ignore")

                # Create a new CSVFile record with uploader ID and save it in the database
                csv_file = CSVFile(filename=file.filename, uploaded_by=current_user.id)  # Set uploader ID
                db.session.add(csv_file)
                db.session.flush()  # Get CSVFile ID before committing
                print(f"CSVFile record created with ID: {csv_file.id}")

                # Process and save each review linked to the CSV file
                review_count = 0
                for _, row in data.iterrows():
                    review_text = row[0]  # Assuming the first column contains the review text
                    if pd.notna(review_text):  # Ensure it's not empty
                        review = Review(text=review_text, csv_file_id=csv_file.id)
                        db.session.add(review)
                        review_count += 1
                db.session.commit()  # Commit both CSV file and reviews

                print(f"{review_count} reviews added for file {csv_file.filename}")  # Debug statement

                flash("File uploaded successfully and reviews added.")
                return redirect(url_for('main.csv_files'))
            except Exception as e:
                db.session.rollback()
                flash(f"Error processing file: {e}")
                print(f"Error during upload: {e}")  # Debug for errors
                return redirect(url_for('main.upload'))
        else:
            flash("Please upload a valid .xlsx or .csv file.")
    return render_template('upload.html')




@main.route('/csv_files')
@login_required
def csv_files():
    if current_user.role == ANNOTATOR_ROLE:
        csv_files = CSVFile.query.filter_by(is_active=True).all()


        # Dictionary to store the annotation count and completion status for the current user per file
        user_annotation_counts = {}
        for csv_file in csv_files:
            # Count total reviews for this file
            total_reviews = Review.query.filter_by(csv_file_id=csv_file.id).count()
            # Count annotations made by the current user on this file
            user_count = Annotation.query.join(Review).filter(
                Annotation.user_id == current_user.id,
                Review.csv_file_id == csv_file.id
            ).count()
            # Check if the annotator has completed all reviews
            completed = user_count == total_reviews
            user_annotation_counts[csv_file.id] = {
                'count': user_count,
                'completed': completed
            }

        return render_template('csv_files.html', csv_files=csv_files, user_annotation_counts=user_annotation_counts)

    elif current_user.role == DEVELOPER_ROLE:
        # Developer logic remains unchanged
        csv_files = CSVFile.query.filter_by(is_active=True).all()

        file_progress_data = []

        for csv_file in csv_files:
            total_reviews = Review.query.filter_by(csv_file_id=csv_file.id).count()
            completed_reviews = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=3).count()
            annotated_by_2_users = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=2).count()
            annotated_by_1_user = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=1).count()
            progress_percentage = (completed_reviews / total_reviews * 100) if total_reviews > 0 else 0
            print(f"File: {csv_file.filename} | Total Reviews: {total_reviews} | Completed Reviews: {completed_reviews}")

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



@main.route('/annotate_csv/<int:csv_file_id>')
@login_required
def annotate_csv(csv_file_id):
    if current_user.role != ANNOTATOR_ROLE:
        return redirect(url_for('main.home'))

    # Lock expired time (e.g., 2 minutes)
    lock_expire_time = datetime.now(timezone.utc) - timedelta(minutes=2)

    # Release locks that have expired
    Review.query.filter(Review.lock_time < lock_expire_time).update({"in_progress_by": None, "lock_time": None})
    db.session.commit()

    # Fetch reviews not yet annotated by the current user
    annotated_review_ids = [annotation.review_id for annotation in Annotation.query.filter_by(user_id=current_user.id).all()]

    # Get the next unannotated review
    review = (Review.query
              .filter(and_(
                  Review.csv_file_id == csv_file_id,
                  Review.id.notin_(annotated_review_ids),  # Exclude reviews already annotated by this user
                  Review.annotation_count < 3,
                  or_(Review.in_progress_by == None, Review.in_progress_by == current_user.id)))
              .order_by(Review.annotation_count)
              .first())

    if review:
        # Lock review for this user
        review.in_progress_by = current_user.id
        review.lock_time = datetime.now(timezone.utc)
        db.session.commit()

        # Calculate the annotation count for the current user on this CSV file
        annotation_count = Annotation.query.join(Review).filter(
            Annotation.user_id == current_user.id,
            Review.csv_file_id == csv_file_id
        ).count()

        return render_template('annotation.html', review=review, csv_file_id=csv_file_id, annotation_count=annotation_count)
    else:
        flash("No more reviews available for annotation in this file.")
        return redirect(url_for('main.csv_files'))

    

@main.route('/submit_annotation', methods=['POST'])
@login_required
def submit_annotation():
    review_id = request.form.get('review_id')
    annotation_text = request.form.get('annotation')
    csv_file_id = request.form.get('csv_file_id')

    # Start a transaction and lock the review for update
    review = Review.query.filter_by(id=review_id).with_for_update().first()

    # Ensure the review exists
    if not review:
        flash("This review is no longer available for annotation.")
        return redirect(url_for('main.csv_files'))

    # Save the new annotation
    new_annotation = Annotation(review_id=review.id, user_id=current_user.id, annotation=annotation_text)
    db.session.add(new_annotation)

    # Update annotation count
    review.annotation_count += 1

    # Unlock the review
    review.in_progress_by = None
    review.lock_time = None

    # If the review has 3 annotations, mark it as complete
    if review.annotation_count >= 3:
        review.completed = True  # Mark the review as completed\
        print(f"Fetching annotations for Review ID {review.id}...")
        annotations = Annotation.query.filter_by(review_id=review.id).order_by(Annotation.created_at).limit(3).all()
        print(f"Annotations fetched: {annotations}")
        # annotations = Annotation.query.filter_by(review_id=review.id).order_by(Annotation.created_at).limit(3).all()
        print(f"Creating CompletedReview entry for Review ID {review.id}")
        completed_review = CompletedReview(
            text=review.text,
            annotator_1_id=annotations[0].user_id,
            annotation_1=annotations[0].annotation,
            annotator_2_id=annotations[1].user_id,
            annotation_2=annotations[1].annotation,
            annotator_3_id=annotations[2].user_id,
            annotation_3=annotations[2].annotation,
            csv_file_id=review.csv_file_id  # Ensure csv_file_id is set
        )
        db.session.add(completed_review)



    # Commit the transaction
    db.session.commit()
    print("Database changes committed.")

    # Redirect to the next annotation
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
    csv_file = CSVFile.query.get_or_404(csv_file_id)

    # Count the total number of reviews in the CSV file
    total_reviews = Review.query.filter_by(csv_file_id=csv_file_id).count()

    # Count the reviews based on their annotation progress
    completed_reviews = Review.query.filter_by(csv_file_id=csv_file_id, annotation_count=3).count()
    annotated_by_2_users = Review.query.filter_by(csv_file_id=csv_file_id, annotation_count=2).count()
    annotated_by_1_user = Review.query.filter_by(csv_file_id=csv_file_id, annotation_count=1).count()

    # Calculate the progress percentage
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



@main.route('/download_annotated_csv/<int:csv_file_id>')
@login_required
def download_annotated_csv(csv_file_id):
    try:
        print(f"Initiating download for CSV File ID: {csv_file_id}")
        reviews = CompletedReview.query.filter_by(csv_file_id=csv_file_id).all()
        print(f"Fetched reviews for CSV ID {csv_file_id}: {len(reviews)}")

        if not reviews:
            flash("No completed annotations available for download.")
            print(f"No completed reviews for CSV ID {csv_file_id}")
            return redirect(url_for('main.csv_files'))

        data = [{
            'Review Text': review.text,
            'Annotation 1': review.annotation_1,
            'Annotation 2': review.annotation_2,
            'Annotation 3': review.annotation_3
        } for review in reviews]
        print(f"Data to be written: {data}")

        df = pd.DataFrame(data)
        buffer = io.StringIO()
        df.to_csv(buffer, index=False, encoding='utf-8')
        buffer.seek(0)
        print("CSV buffer created successfully.")

        filename = f"annotated_{csv_file_id}.csv"
        return send_file(
            io.BytesIO(buffer.getvalue().encode('utf-8')),
            as_attachment=True,
            download_name=filename,  # Updated parameter
            mimetype='text/csv'
        )

    except Exception as e:
        print(f"Error while generating download: {str(e)}")
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('main.csv_files'))








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
    return redirect(url_for('main.csv_files'))


@main.route('/scrape_reviews', methods=['GET', 'POST'])
@login_required
@role_required(DEVELOPER_ROLE)
def scrape_reviews():
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        lang = request.form.get('lang', 'en')
        country = request.form.get('country', 'us')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        count = int(request.form.get('count', 100))

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.")
            return redirect(url_for('main.scrape_reviews'))  # Fixed endpoint

        if start_date > end_date:
            flash("Start date cannot be after end date.")
            return redirect(url_for('main.scrape_reviews'))  # Fixed endpoint

        try:
            reviews_df = scrape_google_play_reviews(app_id, start_date, end_date, lang, country, count)

            if reviews_df.empty:
                flash("No reviews found for the given parameters.")
                return redirect(url_for('main.scrape_reviews'))  # Fixed endpoint

            buffer = io.StringIO()
            reviews_df.to_csv(buffer, index=False, encoding='utf-8')
            buffer.seek(0)
            filename = f"{app_id}_reviews_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"

            return send_file(
                io.BytesIO(buffer.getvalue().encode('utf-8')),
                as_attachment=True,
                download_name=filename,  # Corrected parameter name
                mimetype='text/csv'
            )

        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('main.scrape_reviews'))  # Fixed endpoint

    return render_template('scrape_reviews.html')