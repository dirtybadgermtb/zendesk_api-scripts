import os
import requests
import json
from base64 import b64encode
import csv
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Zendesk Configuration
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

def get_zendesk_triggers(export_to_csv=True):
    """
    Retrieve all triggers from Zendesk using the API and export to CSV with cleaned formatting.
    
    Args:
        export_to_csv (bool): Whether to export the results to a CSV file
    
    Returns:
        list: List of triggers with their details
    """
    # Create the authentication string
    auth = f"{EMAIL}/token:{API_TOKEN}"
    encoded_auth = b64encode(auth.encode('utf-8')).decode('utf-8')
    
    # Set up the request headers
    headers = {
        'Authorization': f'Basic {encoded_auth}',
        'Content-Type': 'application/json'
    }
    
    # Construct the URL
    url = f"{BASE_URL}/triggers"
    
    try:
        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        triggers = response.json()['triggers']
        
        # Print trigger details
        print(f"\nFound {len(triggers)} triggers:\n")
        for trigger in triggers:
            print(f"Trigger ID: {trigger['id']}")
            print(f"Title: {trigger['title']}")
            print(f"Active: {trigger['active']}")
            print(f"Position: {trigger['position']}")
            print("\nConditions:")
            print(json.dumps(trigger['conditions'], indent=2))
            print("\nActions:")
            print(json.dumps(trigger['actions'], indent=2))
            print("\n" + "="*50 + "\n")
        
        # Export to CSV if requested
        if export_to_csv:
            export_triggers_to_csv(triggers)
            
        return triggers
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing Zendesk API: {e}")
        return None

def export_triggers_to_csv(triggers):
    """
    Export triggers to a CSV file with timestamp in the filename.
    Includes cleaned formatting for IDs and dates.
    
    Args:
        triggers (list): List of trigger dictionaries from Zendesk API
    """
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'zendesk_triggers_{timestamp}.csv'
    
    # Define CSV headers
    headers = [ 
        'Trigger ID',
        'Title',
        'Active',
        'Position',
        'Created At',
        'Updated At',
        'Conditions',
        'Actions'
    ]
    
    # Prepare the data with proper formatting
    rows = []
    for trigger in triggers:
        # Convert dates to mm/dd/yyyy format
        created_at = datetime.strptime(trigger.get('created_at', ''), '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y') if trigger.get('created_at') else ''
        updated_at = datetime.strptime(trigger.get('updated_at', ''), '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y') if trigger.get('updated_at') else ''
        
        row = {
            'Trigger ID': str(trigger['id']),  # Format as string to prevent scientific notation
            'Title': trigger['title'],
            'Active': trigger['active'],
            'Position': trigger['position'],
            'Created At': created_at,
            'Updated At': updated_at,
            'Conditions': json.dumps(trigger['conditions']),
            'Actions': json.dumps(trigger['actions'])
        }
        rows.append(row)
    
    try:
        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                
        print(f"\nSuccessfully exported triggers to {filename}")
        
        # Clean up the CSV using pandas
        clean_csv_formatting(filename)
        
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def clean_csv_formatting(filename):
    """
    Clean up the CSV file formatting using pandas.
    
    Args:
        filename (str): Name of the CSV file to clean
    """
    # Read the CSV
    df = pd.read_csv(filename)
    
    # Ensure Trigger ID is formatted as full number
    df['Trigger ID'] = df['Trigger ID'].astype(str)
    
    # Save the cleaned CSV
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    triggers = get_zendesk_triggers()
