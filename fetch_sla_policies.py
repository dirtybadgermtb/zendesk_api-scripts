import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")

if not SUBDOMAIN or not EMAIL or not API_TOKEN:
    print("Error: Zendesk credentials not found in environment variables.")
    print("Please ensure you have set ZENDESK_SUBDOMAIN, ZENDESK_EMAIL, and ZENDESK_API_TOKEN in your .env file.")
    exit()

url = f"https://{SUBDOMAIN}.zendesk.com/api/v2/slas/policies.json"  # Corrected endpoint and added .json
headers = {
    "Content-Type": "application/json",
}

# Use basic authentication
auth = HTTPBasicAuth(f'{EMAIL}/token', API_TOKEN)

try:
    response = requests.get(
        url,
        auth=auth,
        headers=headers
    )

    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

    sla_policies_data = response.json()

    # Write the JSON response to a file
    with open('sla_policies.json', 'w') as json_file:
        json.dump(sla_policies_data, json_file, indent=2)

    print("SLA policies have been written to sla_policies.json")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
except requests.exceptions.RequestException as req_err:
    print(f"Request error occurred: {req_err}")
except json.JSONDecodeError as json_err:
    print(f"JSON Decode error occurred: {json_err}")
    print(f"Response text: {response.text}") # Print the raw response in case of JSON decode error