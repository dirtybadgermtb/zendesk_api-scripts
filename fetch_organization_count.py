import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

email_address = os.getenv('EMAIL_ADDRESS')
api_token = os.getenv('API_TOKEN')
subdomain = os.getenv('SUBDOMAIN')  # Add subdomain to .env

# Construct the URL with the subdomain
url = f"https://{subdomain}.zendesk.com/api/v2/organizations/count"

headers = {
    "Content-Type": "application/json",
}

# Use basic authentication
auth = HTTPBasicAuth(f'{email_address}/token', api_token)

try:
    response = requests.get(url, auth=auth, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    print(response.text)

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response text: {response.text}")  # Print the response text for more details
except Exception as e:
    print(f"An error occurred: {e}")