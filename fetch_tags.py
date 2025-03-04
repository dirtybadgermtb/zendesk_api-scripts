import requests
from requests.auth import HTTPBasicAuth
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")

url = f"https://{SUBDOMAIN}.zendesk.com/api/v2/tags"
headers = {
    "Content-Type": "application/json",
}
# Use basic authentication
auth = HTTPBasicAuth(f'{EMAIL}/token', API_TOKEN)

response = requests.request(
    "GET",
    url,
    auth=auth,
    headers=headers
)

# Process the response
if response.status_code == 200:
    tags = response.json()
    print(f"Total tags found: {len(tags['tags'])}")
    
    # Get the script name without .py extension and create filename with timestamp
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')  # Removed seconds
    filename = f"{script_name}_{timestamp}.csv"
    
    # Write to CSV
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Tag Name', 'Count'])
        # Write data
        for tag in tags['tags']:
            writer.writerow([tag['name'], tag['count']])
    
    print(f"\nData exported to {filename}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

