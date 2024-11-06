from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import CompletedReview, User
import pandas as pd

# Database setup - replace with your actual database URL
DATABASE_URL = "sqlite:///annotations.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Query all columns for completed reviews with annotator details
completed_reviews_data = []
completed_reviews = session.query(CompletedReview).all()

for review in completed_reviews:
    # Fetch annotators based on IDs
    annotator_1 = session.query(User).filter_by(id=review.annotator_1_id).first()
    annotator_2 = session.query(User).filter_by(id=review.annotator_2_id).first()
    annotator_3 = session.query(User).filter_by(id=review.annotator_3_id).first()
    
    # Append all details into the list
    completed_reviews_data.append({
        "Review ID": review.id,
        "Review Text": review.text,
        "Annotator 1 ID": review.annotator_1_id,
        "Annotation 1": review.annotation_1,
        "Annotator 1 Name": annotator_1.name if annotator_1 else "N/A",
        "Annotator 2 ID": review.annotator_2_id,
        "Annotation 2": review.annotation_2,
        "Annotator 2 Name": annotator_2.name if annotator_2 else "N/A",
        "Annotator 3 ID": review.annotator_3_id,
        "Annotation 3": review.annotation_3,
        "Annotator 3 Name": annotator_3.name if annotator_3 else "N/A",
        "Completed At": review.completed_at.strftime("%Y-%m-%d %H:%M:%S")
    })

# Convert to DataFrame for easy display
df = pd.DataFrame(completed_reviews_data)

# Display the table (for interactive environments)
print(df)

# Save the DataFrame as an Excel file
df.to_excel("all_columns_completed_reviews.xlsx", index=False)
print("All columns from CompletedReviews saved to 'all_columns_completed_reviews.xlsx'")