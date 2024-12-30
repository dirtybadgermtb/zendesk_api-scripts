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

# Fetch tickets function
def fetch_tickets(max_tickets=100):
    try:
        url = f"{BASE_URL}/tickets.json"
        all_tickets = []

        while url and len(all_tickets) < max_tickets:
            response = requests.get(url, auth=HTTPBasicAuth(f"{EMAIL}/token", API_TOKEN))

            if response.status_code == 200:
                data = response.json()
                tickets = data.get("tickets", [])

                # Filter tickets with status 'open', 'pending', or 'hold' and missing category
                filtered_tickets = [
                    ticket for ticket in tickets 
                    if ticket.get("status") in {"open", "pending", "hold"} and not ticket.get("ticket_category")
                ]

                remaining_slots = max_tickets - len(all_tickets)
                all_tickets.extend(filtered_tickets[:remaining_slots])
                print(f"Fetched {len(filtered_tickets[:remaining_slots])} valid tickets.")

                # Get the next page URL
                url = data.get("next_page")
            else:
                print(f"Failed to fetch tickets: {response.status_code} - {response.text}")
                break

        print(f"Total tickets fetched: {len(all_tickets)}")
        return all_tickets

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Save tickets to a JSON file
def save_tickets_to_json(tickets, file_name="tickets_missing_category.json"):
    try:
        with open(file_name, "w") as file:
            json.dump(tickets, file, indent=4)
        print(f"Tickets saved to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving the JSON file: {e}")

# Save tickets to a CSV file
def save_tickets_to_csv(tickets, file_name="tickets_missing_category.csv"):
    try:
        if tickets:
            # Define the headers to include
            headers = [
                "url", "id", "created_at", "updated_at", "type", "subject", "description", "priority", 
                "status", "organization_id", "tags", "custom_fields", "satisfaction_rating", "fields", 
                "from_messaging_channel"
            ]

            with open(file_name, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()

                # Write filtered ticket data
                for ticket in tickets:
                    writer.writerow({key: ticket.get(key, None) for key in headers})

            print(f"Tickets saved to {file_name}")
        else:
            print("No tickets available to save to CSV.")
    except Exception as e:
        print(f"An error occurred while saving the CSV file: {e}")

# Main logic
if __name__ == "__main__":
    tickets = fetch_tickets(max_tickets=100)     # Set a limit on the number of tickets fetched (default: 100).
    # To fetch unlimited tickets, modify the parameter as follows:
    # tickets = fetch_tickets(max_tickets=None)
    if tickets:
        save_tickets_to_json(tickets)
        save_tickets_to_csv(tickets)
