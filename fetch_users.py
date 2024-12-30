import os
import requests
from requests.auth import HTTPBasicAuth
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Base URL for your Zendesk instance
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

# Define desired user attributes (adjust as needed)
user_attributes = ["id", "name", "email", "role"]

def fetch_users(max_users=10):
    """
    Fetch users from Zendesk API with an optional limit.

    Args:
        max_users (int, optional): Maximum number of users to fetch. Defaults to 10.
        Set to None for unlimited users.

    Returns:
        None
    """
    with open('zendesk_users.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(user_attributes)  # Write header row

        # Handle pagination (Zendesk API returns results in pages)
        next_page = f"{BASE_URL}/users"  # Start with users endpoint
        fetched_users = 0

        while next_page and (max_users is None or fetched_users < max_users):
            auth = HTTPBasicAuth(f'{EMAIL}/token', API_TOKEN)
            response = requests.get(next_page, auth=auth)
            data = response.json()

            # Extract user data from each page
            for user in data.get("users", []):
                if max_users is not None and fetched_users >= max_users:
                    break
                user_data = [user.get(attribute) for attribute in user_attributes]
                csv_writer.writerow(user_data)
                fetched_users += 1

            # Check for next page link
            next_page = data.get("next_page")

    print(f"Fetched {fetched_users} user(s). Data exported to 'zendesk_users.csv'")

# Main logic
if __name__ == "__main__":
    # Set a default limit to fetch 10 users
    # To fetch unlimited users, call fetch_users(max_users=None)
    fetch_users(max_users=10)
