"""
Instructions for Using the add_tags.py Script:

1.  Prerequisites:
    *   Python 3 installed on your system.
    *   The following Python packages installed:
        *   requests: `pip install requests`
        *   python-dotenv: `pip install python-dotenv`
    *   A Zendesk account with API access.
    *   A `.env` file in the same directory as this script containing your Zendesk credentials:
        ```
        ZENDESK_SUBDOMAIN=your_subdomain
        ZENDESK_EMAIL=your_email@example.com
        ZENDESK_API_TOKEN=your_api_token
        ```
        (Replace the placeholders with your actual credentials.)
    * A CSV file called add_tags.csv in the same directory.

2.  Preparing the CSV File (add_tags.csv):
    *   Create a CSV file named `add_tags.csv` in the same directory as this script (`add_tags.py`).
    *   The CSV file should contain the following columns:
        *   **Ticket ID:** The ID of the Zendesk ticket (e.g., 12345). This is a required field.
        *   **Tag:** The tag you want to add to the tickets. This is a required field. You can leave this field empty on some rows, and it will use the tag of another row.
        * For example:
          ```csv
          Ticket ID,Tag
          61348,csat_invalid
          65171,csat_invalid
          65356,csat_invalid
          101112,
          ```
    *   Each row in the CSV represents a ticket that will be updated.
    *   The first row in the csv will be ignored.
    *   Save the `add_tags.csv` file.

3.  Running the Script:
    *   Open your terminal or command prompt.
    *   Navigate to the directory where you saved `add_tags.py` and `add_tags.csv`.
    *   Execute the script:
        ```bash
        python add_tags.py
        ```
        Or if you use a virtual environement:
        ```bash
        /path/to/your/virtual_env/bin/python add_tags.py
        ```

4.  Checking the Results:
    *   The script will print messages to the console indicating whether the tags were successfully added or if there were any errors.
    *   Log in to your Zendesk account and verify that the specified tags have been added to the correct tickets.
    * If there is an error, the script will provide you with an error message.

5. Additional info:
    * If you renamed the script for any reason (e.g., update_tickets.py), you can simply create a update_tickets.csv and the script will now look for that file. No code change required.

"""
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import json
import csv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")

# Zendesk API endpoint for updating tickets
TICKETS_ENDPOINT = f"https://{SUBDOMAIN}.zendesk.com/api/v2/tickets/update_many"

# Authentication
auth = HTTPBasicAuth(f"{EMAIL}/token", API_TOKEN)

def add_tag_to_tickets(ticket_ids, tag_to_add):
    """
    Adds a specified tag to a list of Zendesk tickets.

    Args:
        ticket_ids (list): A list of Zendesk ticket IDs (integers or strings).
        tag_to_add (str): The tag to add to the tickets.
    """

    if not ticket_ids:
        print("Error: No ticket IDs provided.")
        return

    if not tag_to_add:
        print("Error: No tag provided.")
        return

    # Validate ticket ids and convert to strings
    try:
        ticket_ids_str = [str(int(ticket_id)) for ticket_id in ticket_ids]  # Convert to string
        
    except ValueError as e:
        print(f"Error: Invalid ticket ID format. Must be an integer: {e}")
        return
    
    #Join the id with a comma    
    ticket_ids_str = ",".join(ticket_ids_str)

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "ids": ticket_ids_str, #Now a string
        "ticket": {
            "tags": [tag_to_add]
        }
    }
    
    response = requests.put(
        TICKETS_ENDPOINT, auth=auth, headers=headers, data=json.dumps(payload)
    )

    if response.status_code == 200:
        print(f"Successfully added tag '{tag_to_add}' to tickets: {ticket_ids}")
        # Optionally print the response details for more information
        #print("Response details:", response.json())
    elif response.status_code == 422:
        print(f"Error: {response.status_code}")
        response_data = response.json()
        if 'details' in response_data:
          for detail in response_data['details']:
            print(f"  - Ticket: {detail} Errors: {response_data['details'][detail][0]['description']}")
        else:
          print(response.text)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def load_tickets_and_tag_from_csv(filename):
    """
    Loads ticket IDs and the tag from a CSV file.
    
    The CSV should be formatted with the first column as the ticket ID and the second as the Tag to add.
    If the second column in each row is empty, it will use the tag in the "tag" variable.

    Args:
      filename (str): The path to the CSV file.

    Returns:
        tuple: A tuple containing a list of ticket IDs and the tag to add.
               Returns None, None if the file is not found or is invalid.
    """
    ticket_ids = []
    tag = ""
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip the header row if there is one
            for row in reader:
                try:
                  ticket_ids.append(row[0])
                  if len(row)> 1:
                    tag= row[1]
                except IndexError:
                  print(f"Invalid row in the CSV: {row}. Skipping.")
                  continue
        if not tag:
          print("Error: no tag found in the CSV")
          return None, None

        return ticket_ids, tag
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{filename}'")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

# --- Main Execution ---
if __name__ == "__main__":
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    csv_filename = f"{script_name}.csv"  # Name of your CSV file
    ticket_ids, tag = load_tickets_and_tag_from_csv(csv_filename)
    
    if ticket_ids and tag:
        add_tag_to_tickets(ticket_ids, tag)
    else:
        print("Failed to load data from CSV, check for any error.")
