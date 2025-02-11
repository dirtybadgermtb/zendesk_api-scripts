import requests
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug prints
email_address = os.getenv('ZENDESK_EMAIL')
api_token = os.getenv('ZENDESK_API_TOKEN')
subdomain = os.getenv('ZENDESK_SUBDOMAIN')

print(f"Email: {email_address}")
print(f"API Token: {api_token}")
print(f"Subdomain: {subdomain}")

# Encode email and API token for Basic Authentication
auth_string = f"{email_address}/token:{api_token}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

# List of ticket IDs
ticket_ids = [
    83071, 84364, 84926, 84957, 85006, 85012, 85013, 85017, 85019, 85021, 85029
]

headers = {
    "Authorization": f"Basic {auth_encoded}",
    "Content-Type": "application/json",
}

for ticket_id in ticket_ids:
    url = f"https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}/incidents"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Incidents for ticket {ticket_id}:")
        print(response.json())
    else:
        print(f"Error fetching incidents for ticket {ticket_id}: {response.status_code}")
        print(response.text)
