import os
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from time import sleep
import sys
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Credentials and base URL
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

def fetch_automations(max_automations=10):
    """
    Fetches automations from Zendesk using cursor pagination with an optional limit.

    Args:
        max_automations (int, optional): Maximum number of automations to fetch. Defaults to 10.
        Set to None for unlimited automations.

    Returns:
        list: List of automations fetched from Zendesk
    """
    automations = []
    url = f"{BASE_URL}/automations"
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(f'{EMAIL}/token', API_TOKEN)

    params = {
        'sort_by': 'created_at',
        'sort_order': 'desc',
        'include': 'usage_1h,usage_24h,usage_7d,usage_30d'
    }

    while url and (max_automations is None or len(automations) < max_automations):
        try:
            response = requests.get(url, auth=auth, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Add automations from the current page
            for automation in data.get('automations', []):
                if max_automations is not None and len(automations) >= max_automations:
                    break
                automations.append(automation)

            # Check if 'links' key exists and get the next page URL if it exists
            url = data.get('links', {}).get('next')

            # Rate limiting: Sleep for 0.5 seconds between requests
            sleep(0.5)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            sys.exit(1)

    return automations

def flatten_automation(automation):
    """
    Flattens the automation dictionary for CSV export
    """
    flat_dict = {
        'id': automation.get('id'),
        'title': automation.get('title'),
        'active': automation.get('active'),
        'created_at': automation.get('created_at'),
        'updated_at': automation.get('updated_at'),
        'position': automation.get('position'),
        'usage_1h': automation.get('usage_1h', 0),
        'usage_24h': automation.get('usage_24h', 0),
        'usage_7d': automation.get('usage_7d', 0),
        'usage_30d': automation.get('usage_30d', 0)
    }

    # Add conditions and actions as JSON strings
    flat_dict['conditions'] = json.dumps(automation.get('conditions', {}))
    flat_dict['actions'] = json.dumps(automation.get('actions', []))

    return flat_dict

def main():
    # Fetch automations with a default limit of 10
    # To fetch unlimited automations, call fetch_automations(max_automations=None)
    print("Fetching automations...")
    automations = fetch_automations(max_automations=10)

    if not automations:
        print("No automations found!")
        return

    # Flatten the automation data
    flattened_data = [flatten_automation(automation) for automation in automations]

    # Convert to DataFrame and export to CSV
    df = pd.DataFrame(flattened_data)

    # Sort by position
    df = df.sort_values('position')

    # Export to CSV
    output_file = 'zendesk_automations.csv'
    df.to_csv(output_file, index=False)
    print(f"Successfully exported {len(automations)} automations to {output_file}")

if __name__ == "__main__":
    main()
