import requests
import json
import base64
import os
from dotenv import load_dotenv
from datetime import datetime
import csv

# Load environment variables
load_dotenv()

SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

# Authentication
auth_string = f"{EMAIL}/token:{API_TOKEN}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

ticket_ids = [
   82504,
   83310
]

all_ticket_data = []

def get_organization_name(org_id, headers):
    """Fetches the organization name from the Zendesk API."""
    if not org_id:
        return None
    org_url = f"{BASE_URL}/organizations/{org_id}.json"
    try:
        response = requests.get(org_url, headers=headers)
        response.raise_for_status()
        org_data = response.json()["organization"]
        return org_data.get("name")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching organization {org_id}: {e}")
        return "Error fetching organization name"
    except KeyError:
        print(f"Organization data not found for ID {org_id}")
        return "Organization data not found"
    except Exception as e:
        print(f"An unexpected error occurred while getting organization {org_id}: {e}")
        return "Error fetching organization name"

def calculate_resolution_time(created_at, solved_at):
    """Calculates the resolution time."""
    if not solved_at:
        return None

    created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    solved_dt = datetime.fromisoformat(solved_at.replace("Z", "+00:00"))
    return str(solved_dt - created_dt)  # Return as string

for ticket_id in ticket_ids:
    ticket_url = f"{BASE_URL}/tickets/{ticket_id}.json"
    headers = {"Authorization": f"Basic {auth_encoded}", "Content-Type": "application/json"}

    try:
        # Fetch ticket details
        ticket_response = requests.get(ticket_url, headers=headers)
        ticket_response.raise_for_status()
        ticket_data = ticket_response.json()["ticket"]

        # Get Organization Name
        organization_name = get_organization_name(ticket_data.get("organization_id"), headers)

        # Calculate Resolution Time
        created_at = ticket_data.get("created_at")
        solved_at = ticket_data.get("updated_at") #changed solved_at with updated_at, since there isn't a solved_at field.
        resolution_time = calculate_resolution_time(created_at, solved_at)

        # Combine all data
        all_ticket_data.append({
            "ticket_id": ticket_id,
            "created_at": created_at,
            "solved_at": solved_at,
            "resolution_time": resolution_time,
            "organization_name": organization_name,
        })

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for ticket {ticket_id}: {e}")
        all_ticket_data.append({"ticket_id": ticket_id, "error": str(e)})
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for ticket {ticket_id}: {e}. Response text: {ticket_response.text if 'ticket_response' in locals() else ''}")
        all_ticket_data.append({"ticket_id": ticket_id, "error": str(e)})
    except Exception as e:
        print(f"An unexpected error occurred for ticket {ticket_id}: {e}")
        all_ticket_data.append({"ticket_id": ticket_id, "error": str(e)})

# Define CSV file path
output_file = os.path.join(os.path.dirname(__file__), 'tickets_basic76_end.csv')

# Define CSV header
csv_header = ["ticket_id", "created_at", "solved_at", "resolution_time", "organization_name"]

# Write data to CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_header)
    writer.writeheader()
    for data in all_ticket_data:
        writer.writerow(data)

print(f"Data for all tickets have been saved to {output_file}")