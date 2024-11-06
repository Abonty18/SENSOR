from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Review, Annotation, CompletedReview, User

# Database connection
engine = create_engine("sqlite:///annotations.db")  # Update with your actual database URI
Session = sessionmaker(bind=engine)
session = Session()

# Fetch all reviews with annotations and completion status
reviews = (
    session.query(Review, Annotation, User)
    .outerjoin(Annotation, Review.id == Annotation.review_id)
    .outerjoin(User, Annotation.user_id == User.id)
    .all()
)

# Dictionary to store progress of each review
review_progress = {}
for review, annotation, user in reviews:
    if review.id not in review_progress:
        review_progress[review.id] = {
            "review_text": review.text,
            "annotators": [],
            "annotation_count": review.annotation_count,
            "is_completed": False
        }
    
    if annotation:
        review_progress[review.id]["annotators"].append({
            "user_name": user.name if user else "Unknown",
            "annotation": annotation.annotation if annotation else "None"
        })

# Check if reviews are completed
completed_reviews = session.query(CompletedReview).all()
for completed_review in completed_reviews:
    if completed_review.id in review_progress:
        review_progress[completed_review.id]["is_completed"] = True

# Display the review progress
print("Review ID  | Review Text                              | Annotators                | Annotation Count | Completed")
print("="*100)
for review_id, details in review_progress.items():
    annotators = ", ".join([f"{a['user_name']} ({a['annotation']})" for a in details["annotators"]])
    print(f"{review_id:<10} | {details['review_text'][:40]:<40} | {annotators:<25} | {details['annotation_count']}               | {'Yes' if details['is_completed'] else 'No'}")
