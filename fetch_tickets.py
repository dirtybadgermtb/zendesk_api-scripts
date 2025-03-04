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
    86472
]

all_comments = {}

for ticket_id in ticket_ids:
    url = f"{BASE_URL}/tickets/{ticket_id}/comments.json"
    headers = {"Authorization": f"Basic {auth_encoded}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        comments_data = response.json()
        all_comments[ticket_id] = comments_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments for ticket {ticket_id}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for ticket {ticket_id}: {e}. Response text: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred for ticket {ticket_id}: {e}")

# Save all comments to a JSON file
output_file = os.path.join(os.path.dirname(__file__), 'ticket_comments.json')
with open(output_file, 'w') as f:
    json.dump(all_comments, f, indent=4)

print(f"Comments for all tickets have been saved to {output_file}")