import requests
import json
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

# Encode email and API token for Basic Authentication
auth_string = f"{EMAIL}/token:{API_TOKEN}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

ticket_ids = [
    82294,
    82364,
    82387,
    82414,
    82450,
    82504,
    82544,
    82810,
    83093,
    83145,
    83310,
    83597,
    83654,
    83715,
    83807,
    83821,
    84075,
    84624,
    85017,
    85245,
    85594,
    86472
]

all_ticket_data = {}

for ticket_id in ticket_ids:
    ticket_url = f"{BASE_URL}/tickets/{ticket_id}.json"
    comments_url = f"{BASE_URL}/tickets/{ticket_id}/comments.json"
    headers = {"Authorization": f"Basic {auth_encoded}", "Content-Type": "application/json"}

    try:
        # Fetch ticket details
        ticket_response = requests.get(ticket_url, headers=headers)
        ticket_response.raise_for_status()
        ticket_data = ticket_response.json()["ticket"]

        # Fetch ticket comments
        comments_response = requests.get(comments_url, headers=headers)
        comments_response.raise_for_status()
        comments_data = comments_response.json()

        # Combine ticket details and comments
        all_ticket_data[ticket_id] = {
            "subject": ticket_data.get("subject"),
            "type": ticket_data.get("type"),
            "requester_id": ticket_data.get("requester_id"),
            "organization_id": ticket_data.get("organization_id"),
            "comments": comments_data
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for ticket {ticket_id}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for ticket {ticket_id}: {e}. Response text: {ticket_response.text if 'ticket_response' in locals() else ''} {comments_response.text if 'comments_response' in locals() else ''}")
    except Exception as e:
        print(f"An unexpected error occurred for ticket {ticket_id}: {e}")

# Save all ticket data to a JSON file
output_file = os.path.join(os.path.dirname(__file__), 'tickets_advanced.json')
with open(output_file, 'w') as f:
    json.dump(all_ticket_data, f, indent=4)

print(f"Data for all tickets have been saved to {output_file}")