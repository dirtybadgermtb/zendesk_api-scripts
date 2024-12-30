import requests
import csv
import os

# Replace these with your Zendesk account details
ZENDESK_SUBDOMAIN = os.getenv('ZENDESK_SUBDOMAIN')
ZENDESK_EMAIL = os.getenv('ZENDESK_EMAIL')
ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN')

# API endpoint to retrieve custom fields
url = f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/ticket_fields.json'

# Basic authentication
auth = (f'{ZENDESK_EMAIL}/token', ZENDESK_API_TOKEN)

# Make the API request
response = requests.get(url, auth=auth)

if response.status_code == 200:
    data = response.json()
    custom_fields = data.get('ticket_fields', [])

    # Specify the CSV file path
    csv_file_path = 'custom_fields.csv'

    # Define the CSV headers
    headers = ['id', 'title', 'type', 'description', 'required', 'active', 'created_at', 'updated_at']

    # Write data to CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for field in custom_fields:
            writer.writerow({
                'id': field.get('id'),
                'title': field.get('title'),
                'type': field.get('type'),
                'description': field.get('description'),
                'required': field.get('required'),
                'active': field.get('active'),
                'created_at': field.get('created_at'),
                'updated_at': field.get('updated_at')
            })

    print(f"Custom fields have been exported to {csv_file_path}")
else:
    print(f"Failed to retrieve custom fields. Status code: {response.status_code}")
