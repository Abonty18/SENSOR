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


# import chardet

main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     first_csv_file = CSVFile.query.first()
#     return render_template('home.html', csv_file_id=first_csv_file.id if first_csv_file else None)


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

# @main.route('/annotation')
# @login_required
# def annotation():
#     review = Review.query.order_by(Review.annotation_count, Review.created_at).first()
#     if review:
#         return render_template('annotation.html', review=review)
#     return "No reviews available for annotation"

# @main.route('/submit_annotation', methods=['POST'])


# @main.route('/annotation')
# @login_required
# def annotation():
#     # Get the next review that the current user hasn't annotated
#     annotated_review_ids = [annotation.review_id for annotation in Annotation.query.filter_by(user_id=current_user.id).all()]
#     review = Review.query.filter(~Review.id.in_(annotated_review_ids)).order_by(Review.annotation_count, Review.created_at).first()
    
#     if review:
#         return render_template('annotation.html', review=review)
#     else:
#         flash("No more reviews available for annotation.")
#         return redirect(url_for('main.csv_files'))


# @main.route('/submit_annotation', methods=['POST'])
# @login_required
# def submit_annotation():
#     review_id = request.form.get('review_id')
#     annotation_text = request.form.get('annotation')
#     csv_file_id = request.form.get('csv_file_id')  # Include csv_file_id in form data to redirect back correctly
    
#     # Save the new annotation
#     new_annotation = Annotation(review_id=review_id, user_id=current_user.id, annotation=annotation_text)
#     db.session.add(new_annotation)
    
#     # Update annotation count for the review
#     review = Review.query.get(review_id)
#     review.annotation_count += 1
#     db.session.commit()
    
#     flash("Annotation submitted successfully.")
    
#     # Redirect to the next available review in the same CSV file
#     return redirect(url_for('main.annotate_csv', csv_file_id=csv_file_id))





# @main.route('/upload', methods=['GET', 'POST'])
# @login_required
# def upload():
#     if current_user.role != DEVELOPER_ROLE:
#         flash("You do not have permission to access this page.")
#         return redirect(url_for('main.home'))

#     if request.method == 'POST':
#         file = request.files['file']
#         if file and file.filename.endswith('.csv'):
#             try:
#                 # Detect encoding
#                 raw_data = file.read()
#                 result = chardet.detect(raw_data)
#                 file_encoding = result['encoding']
#                 file.seek(0)  # Reset file pointer after reading

#                 # Read CSV with detected encoding
#                 data = pd.read_csv(file, encoding=file_encoding)
                
#                 # Process the CSV data and add to the database
#                 for _, row in data.iterrows():
#                     review = Review(text=row['review_text'])  # Adjust if column name is different
#                     db.session.add(review)
#                 db.session.commit()
#                 flash("CSV file uploaded successfully and reviews added.")
#                 return redirect(url_for('main.upload'))
#             except Exception as e:
#                 flash(f"Error processing file: {e}")
#                 return redirect(url_for('main.upload'))
#         else:
#             flash("Please upload a valid CSV file.")
#     return render_template('upload.html')

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




# @main.route('/csv_files')
# @login_required
# def csv_files():
#     if current_user.role == ANNOTATOR_ROLE:
#         csv_files = CSVFile.query.all()
#         return render_template('csv_files.html', csv_files=csv_files)
#     elif current_user.role == DEVELOPER_ROLE:
#         csv_files = CSVFile.query.all()
#         return render_template('csv_files_dev.html', csv_files=csv_files)  # Developer template with tracking
#     else:
#         flash("Unauthorized access.")
#         return redirect(url_for('main.home'))

# routes.py

@main.route('/csv_files')
@login_required
def csv_files():
    if current_user.role == ANNOTATOR_ROLE:
        csv_files = CSVFile.query.all()
        
        # Dictionary to store the annotation count for the current user per file
        user_annotation_counts = {}
        for csv_file in csv_files:
            # Count annotations made by the current user on reviews linked to this CSV file
            user_count = Annotation.query.join(Review).filter(
                Annotation.user_id == current_user.id,
                Review.csv_file_id == csv_file.id
            ).count()
            user_annotation_counts[csv_file.id] = user_count

        return render_template('csv_files.html', csv_files=csv_files, user_annotation_counts=user_annotation_counts)

    elif current_user.role == DEVELOPER_ROLE:
        csv_files = CSVFile.query.all()
        file_progress_data = []

        for csv_file in csv_files:
            # Count total reviews and annotation progress details for the developer view
            total_reviews = Review.query.filter_by(csv_file_id=csv_file.id).count()
            completed_reviews = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=3).count()
            annotated_by_2_users = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=2).count()
            annotated_by_1_user = Review.query.filter_by(csv_file_id=csv_file.id, annotation_count=1).count()
            progress_percentage = (completed_reviews / total_reviews * 100) if total_reviews > 0 else 0

            # Append progress data for each file
            file_progress_data.append({
                'file': csv_file,
                'total_reviews': total_reviews,
                'completed_reviews': completed_reviews,
                'annotated_by_2_users': annotated_by_2_users,
                'annotated_by_1_user': annotated_by_1_user,
                'progress_percentage': progress_percentage,
                'uploader_name': csv_file.uploader.name if csv_file.uploader else "Unknown"  # Add uploader's name
            })

        return render_template('csv_files_dev.html', file_progress_data=file_progress_data)

    else:
        flash("Unauthorized access.")
        return redirect(url_for('main.home'))



@main.route('/annotate_csv/<int:csv_file_id>')
@login_required
def annotate_csv(csv_file_id):
    if current_user.role != ANNOTATOR_ROLE:
        # flash("You do not have permission to access this page.")
        return redirect(url_for('main.home'))

    # Lock expired time (e.g., 2 minutes)
    lock_expire_time = datetime.now(timezone.utc) - timedelta(minutes=2)

    # Release locks that have expired
    Review.query.filter(Review.lock_time < lock_expire_time).update({"in_progress_by": None, "lock_time": None})
    db.session.commit()

    # Get reviews annotated by less than 3 users and not locked by others
    review = (Review.query
              .filter(and_(
                  Review.csv_file_id == csv_file_id,
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

    if review:
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

    # Ensure the review is still available and locked by this user
    review = Review.query.filter_by(id=review_id, in_progress_by=current_user.id).first()
    if not review:
        flash("This review is no longer available for annotation.")
        return redirect(url_for('main.csv_files'))

    # Save the new annotation
    new_annotation = Annotation(review_id=review_id, user_id=current_user.id, annotation=annotation_text, is_final=True)
    db.session.add(new_annotation)
    
    # Update annotation count for the review
    review.annotation_count += 1
    review.in_progress_by = None  # Unlock the review
    review.lock_time = None       # Clear the lock time

    # If the review has received three annotations, mark it as complete
    if review.annotation_count >= 3:
        # Fetch the annotations for this review
        annotations = Annotation.query.filter_by(review_id=review_id).order_by(Annotation.created_at).limit(3).all()

        # Create a CompletedReview entry with annotations from each annotator
        completed_review = CompletedReview(
            text=review.text,
            annotator_1_id=annotations[0].user_id,
            annotation_1=annotations[0].annotation,
            annotator_2_id=annotations[1].user_id,
            annotation_2=annotations[1].annotation,
            annotator_3_id=annotations[2].user_id,
            annotation_3=annotations[2].annotation
        )
        db.session.add(completed_review)

        # Remove the review from active reviews to prevent reassignment
        db.session.delete(review)

    db.session.commit()

    return redirect(url_for('main.annotate_csv', csv_file_id=csv_file_id))





@main.route('/check_csv_files')
def check_csv_files():
    csv_files = CSVFile.query.all()
    for file in csv_files:
        print("CSV File:", file.filename)
    return "Check your console for CSV files."




@main.route('/check_review_counts')
def check_review_counts():
    # Query all CSV files and check associated reviews
    csv_files = CSVFile.query.all()
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
    # Fetch the completed reviews associated with the given CSV file
    reviews = CompletedReview.query.filter_by(csv_file_id=csv_file_id).all()

    # Check if there are any completed reviews
    if not reviews:
        flash("No completed annotations available for download.")
        return redirect(url_for('main.csv_files'))

    # Create a DataFrame to organize annotations
    data = [{
        'Review Text': review.text,
        'Annotation 1': review.annotation_1,
        'Annotation 2': review.annotation_2,
        'Annotation 3': review.annotation_3
    } for review in reviews]
    df = pd.DataFrame(data)

    # Save DataFrame to a CSV in memory
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    # Send the CSV as a downloadable file
    filename = f"annotated_{csv_file_id}.csv"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='text/csv')