import os
import requests
import json
from base64 import b64encode
import pandas as pd
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Zendesk Configuration
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

def delete_triggers_from_csv(csv_file='delete_triggers.csv'):
    """
    Delete triggers from Zendesk based on Trigger IDs provided in a CSV file.

    Args:
        csv_file (str): Path to CSV file containing trigger IDs. Default is 'delete_triggers.csv'.

    Instructions:
        - Create a CSV file named 'delete_triggers.csv' in the same directory as this script.
        - The file should have a single column named 'Trigger_deletion' with trigger IDs to delete.
        - Example format:

          Trigger_deletion
          12345678
          87654321
    """
    # Create the authentication string
    auth = f"{EMAIL}/token:{API_TOKEN}"
    encoded_auth = b64encode(auth.encode('utf-8')).decode('utf-8')
    
    # Set up the request headers
    headers = {
        'Authorization': f'Basic {encoded_auth}',
        'Content-Type': 'application/json'
    }

    # Read trigger IDs from CSV
    try:
        df = pd.read_csv(csv_file)
        trigger_ids = df['Trigger_deletion'].astype(str).tolist()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    print(f"Found {len(trigger_ids)} triggers to delete")
    
    # Create log file for results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'trigger_deletion_log_{timestamp}.csv'
    
    results = []
    
    # Delete each trigger
    for trigger_id in trigger_ids:
        url = f"{BASE_URL}/triggers/{trigger_id}"
        
        try:
            print(f"Attempting to delete trigger {trigger_id}...")
            response = requests.delete(url, headers=headers)
            
            result = {
                'Trigger_deletion': trigger_id,
                'Status': 'Success' if response.status_code == 204 else 'Failed',
                'Response Code': response.status_code,
                'Error Message': response.text if response.status_code != 204 else ''
            }
            
            if response.status_code == 204:
                print(f"Successfully deleted trigger {trigger_id}")
            else:
                print(f"Failed to delete trigger {trigger_id}. Status code: {response.status_code}")
                print(f"Error: {response.text}")
                
            results.append(result)
            
            # Add a small delay to prevent rate limiting
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            print(f"Error deleting trigger {trigger_id}: {e}")
            results.append({
                'Trigger_deletion': trigger_id,
                'Status': 'Failed',
                'Response Code': 'Error',
                'Error Message': str(e)
            })
    
    # Save results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv(log_filename, index=False)
    print(f"\nDeletion results have been saved to {log_filename}")
    
    # Print summary
    success_count = len(results_df[results_df['Status'] == 'Success'])
    fail_count = len(results_df[results_df['Status'] == 'Failed'])
    print(f"\nDeletion Summary:")
    print(f"Successfully deleted: {success_count}")
    print(f"Failed to delete: {fail_count}")

if __name__ == "__main__":
    delete_triggers_from_csv()
