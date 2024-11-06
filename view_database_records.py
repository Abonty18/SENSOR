import sqlite3

# Connect to the SQLite database (annotations.db)
conn = sqlite3.connect('annotations.db')
cursor = conn.cursor()

# Retrieve all CSV files
cursor.execute("SELECT id, filename FROM csv_file")
csv_files = cursor.fetchall()
print("Uploaded CSV Files:")
for file in csv_files:
    print(f"ID: {file[0]}, Filename: {file[1]}")

# Retrieve all reviews and associated CSV file IDs
cursor.execute("SELECT id, text, csv_file_id FROM review")
reviews = cursor.fetchall()
print("\nReviews in the Database:")
for review in reviews:
    print(f"Review ID: {review[0]}, CSV File ID: {review[2]}, Text: {review[1][:50]}...")  # Show only first 50 chars of text

# Close the database connection
conn.close()
