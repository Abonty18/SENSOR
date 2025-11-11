# # from google_play_scraper import Sort, reviews
# # from datetime import datetime
# # import pandas as pd

# # # Function to filter reviews based on date range
# # def filter_reviews_by_date(reviews, start_date, end_date):
# #     filtered_reviews = []
# #     unique_contents = set()

# #     for review in reviews:
# #         try:
# #             # Parse the review date
# #             review_date = datetime.strptime(review['at'].strftime('%Y-%m-%d'), '%Y-%m-%d')

# #             # Check if the review date is within the specified range
# #             if start_date <= review_date <= end_date:
# #                 content = review['content'].strip()

# #                 # Check for duplicate reviews
# #                 if content not in unique_contents:
# #                     unique_contents.add(content)
# #                     filtered_reviews.append({
# #                         'Author': review['userName'],
# #                         'Content': content,
# #                         'Rating': review['score'],
# #                         'Date': review_date.strftime('%Y-%m-%d'),
# #                     })
# #         except Exception as e:
# #             print(f"[ERROR] Failed to process review: {e}")

# #     return filtered_reviews

# # # Main function to scrape and process reviews
# # from google_play_scraper import reviews
# # import pandas as pd
# # from datetime import datetime

# # def scrape_and_filter_reviews():
# #     app_id = input("Enter the app package name (e.g., com.whatsapp): ")
# #     start_date_str = input("Enter the start date (YYYY-MM-DD): ")
# #     end_date_str = input("Enter the end date (YYYY-MM-DD): ")
# #     num_reviews = int(input("Enter the number of reviews to scrape: "))
    
# #     # Validate dates
# #     try:
# #         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
# #         end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
# #         if end_date.date() != datetime.today().date():
# #             print("[ERROR] End date must be today's date.")
# #             return
# #     except ValueError:
# #         print("[ERROR] Invalid date format. Please use YYYY-MM-DD.")
# #         return
    
# #     print("[INFO] Starting to fetch reviews...")
# #     all_reviews = []
    
# #     try:
# #         fetched_reviews, _ = reviews(app_id, count=num_reviews, lang="en", country="us")
# #         print(f"[DEBUG] Fetched {len(fetched_reviews)} reviews.")
        
# #         for review in fetched_reviews:
# #             # Convert date and filter
# #             review_date = datetime.strptime(review['at'].strftime('%Y-%m-%d'), "%Y-%m-%d")
# #             if start_date <= review_date <= end_date:
# #                 all_reviews.append({
# #                     "Author": review['userName'],
# #                     "Content": review['content'],
# #                     "Rating": review['score'],
# #                     "Date": review_date.strftime("%Y-%m-%d")
# #                 })
# #     except Exception as e:
# #         print(f"[ERROR] Failed to fetch reviews: {e}")
# #         return
    
# #     # Remove duplicates
# #     df = pd.DataFrame(all_reviews).drop_duplicates(subset="Content")
# #     print(f"[INFO] Total filtered reviews: {len(df)}")
    
# #     # Save to CSV
# #     filename = f"{app_id}_{start_date_str}_{end_date_str}.csv"
# #     df.to_csv(filename, index=False)
# #     print(f"[INFO] Reviews saved to {filename}")

# # if __name__ == "__main__":
# #     scrape_and_filter_reviews()
# import pandas as pd
# from datetime import datetime
# from google_play_scraper import reviews

# def scrape_reviews_without_date_filter():
#     app_id = input("Enter the app package name (e.g., com.whatsapp): ")
#     num_reviews = int(input("Enter the number of reviews to scrape: "))

#     print("[INFO] Starting to fetch reviews...")
#     all_reviews = []

#     try:
#         fetched_reviews, _ = reviews(app_id, count=num_reviews, lang="en", country="us")
#         print(f"[DEBUG] Fetched {len(fetched_reviews)} reviews.")

#         for review in fetched_reviews:
#             all_reviews.append({
#                 "Author": review['userName'],
#                 "Content": review['content'],
#                 "Rating": review['score'],
#                 "Date": review['at'].date()
#             })
#     except Exception as e:
#         print(f"[ERROR] Failed to fetch reviews: {e}")
#         return

#     # Remove duplicates
#     df = pd.DataFrame(all_reviews).drop_duplicates(subset="Content")
#     print(f"[INFO] Total filtered reviews: {len(df)}")

#     # Save to CSV
#     filename = f"{app_id}_reviews.csv"
#     df.to_csv(filename, index=False)
#     print(f"[INFO] Reviews saved to {filename}")

# if __name__ == "__main__":
#     scrape_reviews_without_date_filter()
# import requests
# from datetime import datetime
# import csv

# def fetch_reviews(app_id, batch_size=100, next_token=None):
#     base_url = "https://play.google.com/store/apps/details"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     params = {"id": app_id, "hl": "en", "gl": "us"}
#     if next_token:
#         params["continueToken"] = next_token

#     try:
#         response = requests.get(base_url, headers=headers, params=params, verify=False)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"[ERROR] Request failed: {e}")
#         return [], None

#     # Mock data for demonstration purposes
#     reviews = [
#         {"content": "Sample review", "date": "2025-01-01", "rating": 5},
#         {"content": "Another review", "date": "2024-12-30", "rating": 4}
#     ]
#     next_token = None  # Replace with actual token if available
#     return reviews, next_token

# def scrape_reviews(app_id, start_date, end_date, review_count):
#     all_reviews = []
#     next_token = None
#     batch_size = 100

#     while len(all_reviews) < review_count:
#         print(f"[DEBUG] Fetching batch... Total fetched so far: {len(all_reviews)}")
#         reviews, next_token = fetch_reviews(app_id, batch_size=batch_size, next_token=next_token)

#         if not reviews:
#             print("[DEBUG] No more reviews available.")
#             break

#         filtered_reviews = filter_reviews_by_date(reviews, start_date, end_date)
#         all_reviews.extend(filtered_reviews)

#         print(f"[DEBUG] Batch size: {len(reviews)} reviews fetched. Filtered: {len(filtered_reviews)}")

#         if not next_token:
#             print("[DEBUG] No next token available. Stopping fetch.")
#             break

#         if len(all_reviews) < review_count:
#             batch_size *= 2  # Increase the batch size for the next fetch to collect more data
#             print(f"[DEBUG] Insufficient reviews. Increasing batch size to {batch_size}.")

#     print(f"[INFO] Total scraped reviews: {len(all_reviews)}")
#     save_reviews_to_csv(all_reviews[:review_count], app_id, start_date, end_date)

# def filter_reviews_by_date(reviews, start_date, end_date):
#     filtered = []
#     for review in reviews:
#         review_date = datetime.strptime(review["date"], "%Y-%m-%d")
#         if start_date <= review_date <= end_date:
#             filtered.append(review)
#     return filtered

# def save_reviews_to_csv(reviews, app_id, start_date, end_date):
#     filename = f"{app_id}_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.csv"
#     with open(filename, "w", newline="", encoding="utf-8") as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=["content", "date", "rating"])
#         writer.writeheader()
#         writer.writerows(reviews)
#     print(f"[INFO] Reviews saved to {filename}")

# if __name__ == "__main__":
#     app_id = input("Enter the app package name (e.g., com.whatsapp): ")
#     start_date_str = input("Enter the start date (YYYY-MM-DD): ")
#     end_date_str = input("Enter the end date (YYYY-MM-DD): ")
#     review_count = int(input("Enter the number of reviews to scrape: "))

#     start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
#     end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

#     if end_date > datetime.today():
#         print("[ERROR] End date must not exceed today's date.")
#     else:
#         scrape_reviews(app_id, start_date, end_date, review_count)
from google_play_scraper import reviews
from datetime import datetime
import csv


def fetch_reviews(app_id, batch_size=100):
    """
    Fetch reviews in batches using google-play-scraper.
    """
    result, continuation_token = reviews(
        app_id,
        lang="en",  # English reviews
        country="us",  # US store
        count=batch_size,  # Max reviews in one batch
    )
    return result, continuation_token


def filter_reviews_by_date(all_reviews, start_date, end_date):
    """
    Filter reviews based on the provided date range.
    """
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    filtered = []

    for review in all_reviews:
        review_date = review['at']  # Datetime object
        if start_date_obj <= review_date <= end_date_obj:
            filtered.append(review)

    return filtered


def scrape_and_filter_reviews(app_id, start_date, end_date, total_reviews):
    """
    Scrape and filter reviews until the required number of filtered reviews is met.
    """
    all_reviews = []
    filtered_reviews = []
    continuation_token = None

    while len(filtered_reviews) < total_reviews:
        print(f"[INFO] Fetching batch... Current total filtered: {len(filtered_reviews)}")
        try:
            batch_reviews, continuation_token = reviews(
                app_id,
                continuation_token=continuation_token,
                lang="en",
                country="us",
                count=100,  # Fetch in batches of 100
            )
        except Exception as e:
            print(f"[ERROR] Failed to fetch reviews: {e}")
            break

        if not batch_reviews:
            print("[INFO] No more reviews available.")
            break

        all_reviews.extend(batch_reviews)

        # Filter by date
        filtered = filter_reviews_by_date(batch_reviews, start_date, end_date)
        filtered_reviews.extend(filtered)

        # Remove duplicates
        filtered_reviews = list({rev['reviewId']: rev for rev in filtered_reviews}.values())

    return filtered_reviews[:total_reviews]


def save_to_csv(reviews, file_name):
    """
    Save reviews to a CSV file.
    """
    keys = ['reviewId', 'userName', 'at', 'score', 'content']
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for review in reviews:
            writer.writerow({
                'reviewId': review['reviewId'],
                'userName': review['userName'],
                'at': review['at'].strftime("%Y-%m-%d"),
                'score': review['score'],
                'content': review['content'],
            })


def main():
    app_id = input("Enter the app package name (e.g., com.whatsapp): ").strip()
    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
    total_reviews = int(input("Enter the number of reviews to scrape: ").strip())

    print("[INFO] Starting the scraping process...")
    filtered_reviews = scrape_and_filter_reviews(app_id, start_date, end_date, total_reviews)

    if filtered_reviews:
        file_name = f"{app_id}_{start_date}_{end_date}.csv"
        save_to_csv(filtered_reviews, file_name)
        print(f"[INFO] Scraped {len(filtered_reviews)} reviews. Saved to {file_name}.")
    else:
        print("[INFO] No reviews found for the given date range.")


if __name__ == "__main__":
    main()
