import requests

# Hardcoded Zendesk API credentials
SUBDOMAIN = "spreedly"
EMAIL = "ken@spreedly.com"
API_TOKEN = "123FAKEID!"
BASE_URL = f"https://spreeedly.zendesk.com/api/v2"

# List of conversation IDs (replace with your actual IDs)
conversation_ids = [
    "67909695dadbdc774386df3e",
]

# Function to fetch conversation details
def fetch_conversation(conversation_id):
    url = f"{BASE_URL}/conversations/{conversation_id}.json"
    response = requests.get(url, auth=(f"{EMAIL}/token", API_TOKEN))
    
    if response.status_code == 200:
        conversation = response.json()["conversation"]
        print(f"Conversation ID: {conversation_id}")
        print(f"Status: {conversation['status']}")
        print(f"Created At: {conversation['created_at']}")
        print("Participants:")
        for participant in conversation["participants"]:
            print(f"  - Name: {participant['name']}, Email: {participant['email']}")
        print("Messages:")
        for message in conversation["messages"]:
            print(f"  - {message['body']}")
        print("-" * 40)
    else:
        print(f"Failed to fetch conversation {conversation_id}. Status code: {response.status_code}")

# Loop through conversation IDs and fetch details
for conversation_id in conversation_ids:
    fetch_conversation(conversation_id)