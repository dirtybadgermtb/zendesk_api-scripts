import os
import requests
import json
import csv
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Credentials and base URL
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

# Fetch ticket fields function
def fetch_ticket_fields():
    try:
        url = f"{BASE_URL}/ticket_fields.json"
        response = requests.get(url, auth=HTTPBasicAuth(f"{EMAIL}/token", API_TOKEN))

        if response.status_code == 200:
            fields = response.json().get("ticket_fields", [])
            print(f"Fetched {len(fields)} ticket fields.")
            return fields
        else:
            print(f"Failed to fetch ticket fields: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Save ticket fields to a JSON file
def save_fields_to_json(fields, file_name="ticket_fields.json"):
    try:
        with open(file_name, "w") as file:
            json.dump(fields, file, indent=4)
        print(f"Ticket fields saved to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving the JSON file: {e}")

# Save ticket fields to a CSV file
def save_fields_to_csv(fields, file_name="ticket_fields.csv"):
    try:
        if fields:
            # Define the headers for the CSV file
            headers = ["id", "type", "title", "raw_title", "description", "raw_description", "active", "required", "options", "created_at", "updated_at"]

            with open(file_name, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()

                # Write field data, including options as a serialized string
                for field in fields:
                    writer.writerow({
                        "id": field.get("id"),
                        "type": field.get("type"),
                        "title": field.get("title"),
                        "raw_title": field.get("raw_title"),
                        "description": field.get("description"),
                        "raw_description": field.get("raw_description"),
                        "active": field.get("active"),
                        "required": field.get("required"),
                        "options": json.dumps(field.get("custom_field_options", [])),
                        "created_at": field.get("created_at"),
                        "updated_at": field.get("updated_at")
                    })

            print(f"Ticket fields saved to {file_name}")
        else:
            print("No fields available to save to CSV.")
    except Exception as e:
        print(f"An error occurred while saving the CSV file: {e}")

# Main logic
if __name__ == "__main__":
    fields = fetch_ticket_fields()
    if fields:
        save_fields_to_json(fields)
        save_fields_to_csv(fields)
