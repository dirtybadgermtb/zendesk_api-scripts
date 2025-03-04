import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

def get_organization_count():
    """Fetches the total count of organizations from Zendesk."""
    load_dotenv()

    # Fetch environment variables
    email_address = os.getenv('ZENDESK_EMAIL')
    api_token = os.getenv('ZENDESK_API_TOKEN')   
    subdomain = os.getenv('ZENDESK_SUBDOMAIN')

    if not all([email_address, api_token, subdomain]):
        print("Your .env file is missing some credentials. Please check ZENDESK_EMAIL, ZENDESK_API_TOKEN, and ZENDESK_SUBDOMAIN.")
        return None

    # Define API endpoint
    url = f'https://{subdomain}.zendesk.com/api/v2/organizations/count.json'
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(f'{email_address}/token', api_token)

    # API request
    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        count = response.json().get("count", {}).get("value", 0)
        print(f"Total organizations: {count}")
        return count
    else:
        print(f"Error fetching organization count: {response.status_code} - {response.text}")
        return None

if __name__ == '__main__':
    get_organization_count()
