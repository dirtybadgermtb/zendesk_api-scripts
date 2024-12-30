#!/usr/bin/env python3
# fetch_orgs.py

import os
import csv
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from zd.env
load_dotenv('.env')

def get_organizations(limit=10):
    """
    Fetch up to `limit` organizations from Zendesk.
    For unlimited, remove the slicing or (better yet) implement pagination
    by following `next_page` links in the response.
    """
    email_address = os.getenv('ZENDESK_EMAIL')
    api_token = os.getenv('ZENDESK_API_TOKEN')   
    subdomain = os.getenv('ZENDESK_SUBDOMAIN')

    if not all([email_address, api_token, subdomain]):
        print(
            "Your zd.env file is missing something. Check that you have "
            "ZENDESK_EMAIL, ZENDESK_API_TOKEN, and ZENDESK_SUBDOMAIN configured."
        )
        return []

    url = f'https://{subdomain}.zendesk.com/api/v2/organizations'
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(f'{email_address}/token', api_token)

    # Request the first page
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        print(f"Error fetching orgs: {response.status_code} - {response.text}")
        return []

    data = response.json()
    organizations = data.get("organizations", [])

    # Limit to 10 for demonstration
    organizations = organizations[:limit]

    return organizations

def write_orgs_to_csv(organizations, filename='zendesk_orgs.csv'):
    """
    Writes the given organizations to a CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header row
        headers = [
            "ID",
            "Name",
            "Created At",
            "Updated At",
            "Domain Names",
            "Account Classification",
            "Account Owner SF",
            "Account Type SF",
            "Billing Org ID",
            "Salesforce Account Stage",
            "Service Level",
            "SFDC Account ID",
            "Sync To Zendesk",
            "Website"
        ]
        writer.writerow(headers)

        # Write each organization's row
        for org in organizations:
            fields = org.get("organization_fields", {})
            row = [
                org.get("id"),
                org.get("name"),
                org.get("created_at"),
                org.get("updated_at"),
                ", ".join(org.get("domain_names", [])),
                fields.get("account_classification"),
                fields.get("account_owner_sf_"),
                fields.get("account_type_sf_"),
                fields.get("billing_org_id"),
                fields.get("salesforce_account_stage"),
                fields.get("service_level"),
                fields.get("sfdc_account_id"),
                fields.get("sync_to_zendesk"),
                fields.get("webste"),
            ]
            writer.writerow(row)

def main():
    # Step 1: Get the orgs
    organizations = get_organizations(limit=10)  # Currently grabbing 10
    if organizations:
        # Step 2: Write them to CSV
        write_orgs_to_csv(organizations, 'zendesk_orgs.csv')
        print("All done! Check 'zendesk_orgs.csv' for your results.")
    else:
        print("No organizations returned or an error occurred.")

if __name__ == '__main__':
    main()
