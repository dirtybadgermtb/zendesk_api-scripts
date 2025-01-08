# delete_tickets.py

import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import requests

# Load the environment variables from zd.env
load_dotenv(".env")

# Fetch the environment variables
ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_TOKEN = os.getenv("ZENDESK_API_TOKEN")

# Construct the base URL
base_url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2"

# List of ticket IDs to delete
ticket_ids = [
    84651, 84654, 84856, 84857, 84902, 84903, 85053, 85054, 85059, 85127, 85128, 85129, 85130, 85131, 85132, 85249, 85250, 85257, 85258, 85259, 85260, 85261, 85262, 85267, 85269, 85270, 85738, 84885, 84652, 84653, 84672, 84673, 84552, 80353, 76504, 66942
]

# Headers for the request
headers = {
    "Content-Type": "application/json"
}

# Use basic authentication
auth = HTTPBasicAuth(f"{ZENDESK_EMAIL}/token", ZENDESK_TOKEN)

def delete_ticket(ticket_id):
    url = f"{base_url}/tickets/{ticket_id}.json"
    response = requests.delete(url, auth=auth, headers=headers)
    if response.status_code == 204:
        print(f"Ticket ID {ticket_id} deleted successfully.")
    else:
        print(
            f"Failed to delete Ticket ID {ticket_id}: "
            f"{response.status_code} - {response.text}"
        )

if __name__ == "__main__":
    # Iterate over the ticket IDs and delete each one
    for ticket_id in ticket_ids:
        delete_ticket(ticket_id)
