import requests
import json
import base64
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from textblob import TextBlob
from bs4 import BeautifulSoup
import nltk

# Download necessary NLTK data (only needs to be done once)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:    
    nltk.download('punkt')

# Load environment variables
load_dotenv()

SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

# Authentication
auth_string = f"{EMAIL}/token:{API_TOKEN}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

ticket_ids = [
    82294, 82364, 82387, 82414, 82450, 82504, 82544, 82810, 83093,
    83145, 83310, 83597, 83654, 83715, 83807, 83821, 84075, 84624,
    85017, 85245, 85594, 86472
]  #  Consider loading from a config file or command-line arguments for larger lists

all_ticket_data = {}

def get_organization_name(org_id, headers):
    """Fetches the organization name from the Zendesk API."""
    if not org_id:
        return None  # No organization associated with the ticket

    org_url = f"{BASE_URL}/organizations/{org_id}.json"
    try:
        response = requests.get(org_url, headers=headers)
        response.raise_for_status()
        org_data = response.json()["organization"]
        return org_data.get("name")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching organization {org_id}: {e}")
        return "Error fetching organization name"
    except KeyError:
        print(f"Organization data not found for ID {org_id}")
        return "Organization data not found"
    except Exception as e:
        print(f"An unexpected error occurred while getting organization {org_id}: {e}")
        return "Error fetching organization name"

def analyze_sentiment(comments):
    """Performs sentiment analysis on the combined comments."""
    if not comments or not comments.get("comments"):
        return "No comments available"

    all_comments_text = ""
    for comment in comments["comments"]:
        if 'body' in comment:
          # Extract text, handling HTML
          soup = BeautifulSoup(comment['body'], 'html.parser')
          all_comments_text += soup.get_text() + " "  # Add space between comments

    if not all_comments_text.strip():  # Check if text is empty after stripping
        return "No comments available"

    analysis = TextBlob(all_comments_text)
    return analysis.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)

def calculate_resolution_time(created_at, solved_at):
    """Calculates the resolution time in days."""
    if not solved_at:
        return None  # Ticket not yet solved

    created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    solved_dt = datetime.fromisoformat(solved_at.replace("Z", "+00:00"))
    return (solved_dt - created_dt).days

for ticket_id in ticket_ids:
    ticket_url = f"{BASE_URL}/tickets/{ticket_id}.json"
    comments_url = f"{BASE_URL}/tickets/{ticket_id}/comments.json"
    headers = {"Authorization": f"Basic {auth_encoded}", "Content-Type": "application/json"}

    try:
        # Fetch ticket details
        ticket_response = requests.get(ticket_url, headers=headers)
        ticket_response.raise_for_status()
        ticket_data = ticket_response.json()["ticket"]

        # Fetch ticket comments
        comments_response = requests.get(comments_url, headers=headers)
        comments_response.raise_for_status()
        comments_data = comments_response.json()

        # Get Organization Name
        organization_name = get_organization_name(ticket_data.get("organization_id"), headers)

        # Calculate Resolution Time
        resolution_time = calculate_resolution_time(ticket_data.get("created_at"), ticket_data.get("updated_at")) #changed solved_at with updated_at, since there isn't a solved_at field.

        # Analyze Sentiment
        sentiment = analyze_sentiment(comments_data)

        # Combine all data
        all_ticket_data[ticket_id] = {
            "subject": ticket_data.get("subject"),
            "short_summary": TextBlob(ticket_data.get("description", "")).sentences[0].string if ticket_data.get("description") else "No description available",  # First sentence as summary
            "type": ticket_data.get("type"),
            "category": ticket_data.get("tags"),  # Using tags as a proxy for category
            "requester_id": ticket_data.get("requester_id"),
            "organization_id": ticket_data.get("organization_id"),
            "organization_name": organization_name,
            "resolution_time_days": resolution_time,
            "sentiment": sentiment,
            "comments": comments_data,  # Keep the full comments as well
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for ticket {ticket_id}: {e}")
        all_ticket_data[ticket_id] = {"error": str(e)} # Store error message
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for ticket {ticket_id}: {e}.  Response text: {ticket_response.text if 'ticket_response' in locals() else ''} {comments_response.text if 'comments_response' in locals() else ''}")
        all_ticket_data[ticket_id] = {"error": str(e)} # Store error message
    except Exception as e:
        print(f"An unexpected error occurred for ticket {ticket_id}: {e}")
        all_ticket_data[ticket_id] = {"error": str(e)} # Store error message

# Save all ticket data to a JSON file
output_file = os.path.join(os.path.dirname(__file__), 'tickets_advanced.json')
with open(output_file, 'w') as f:
    json.dump(all_ticket_data, f, indent=4)

print(f"Data for all tickets have been saved to {output_file}")