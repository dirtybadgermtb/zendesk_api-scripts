import os
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# List of automation IDs to delete
automation_ids = [
    1234,
    2345
   ]

# Prepare the IDs to be used in the DELETE request
ids_str = ",".join(map(str, automation_ids))

# Define the Zendesk API endpoint for bulk deletion
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"
url = f"{BASE_URL}/automations/destroy_many?ids={ids_str}"

# Define headers and authentication
headers = {
    "Content-Type": "application/json",
}

# Use basic authentication
auth = HTTPBasicAuth(f'{EMAIL}/token', API_TOKEN)

# Send the DELETE request with SSL verification off
response = requests.request(
    "DELETE",
    url,
    auth=auth,
    headers=headers,
    verify=False  # Disable SSL verification if needed
)

# Print the response
print(response.text)
