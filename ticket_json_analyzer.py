import json
import os
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Load the JSON data
input_file = os.path.join(os.path.dirname(__file__), 'tickets_advanced.json')
with open(input_file, 'r') as f:
    data = json.load(f)

# Function to calculate sentiment
def calculate_sentiment(text):
    sentiment_scores = sid.polarity_scores(text)
    return sentiment_scores['compound']

# Function to calculate resolution time in days
def calculate_resolution_time(comments):
    if not comments:
        return None
    created_at = datetime.strptime(comments[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    resolved_at = datetime.strptime(comments[-1]['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    resolution_time = (resolved_at - created_at).days
    return resolution_time

# Process each ticket
summary_data = []
for ticket_id, ticket_info in data.items():
    comments = ticket_info['comments']['comments']
    if not comments:
        continue

    # Calculate sentiment for each comment
    sentiments = [calculate_sentiment(comment['body']) for comment in comments if 'body' in comment]
    average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

    # Calculate resolution time
    resolution_time = calculate_resolution_time(comments)

    # Extract required information
    summary = {
        'ticket_id': ticket_id,
        'subject': ticket_info.get('subject', 'N/A'),
        'category': ticket_info.get('type', 'N/A'),
        'organization_id': ticket_info.get('organization_id', 'N/A'),
        'resolution_time_days': resolution_time,
        'average_sentiment': average_sentiment
    }
    summary_data.append(summary)

# Save the summary data to a new JSON file
output_file = os.path.join(os.path.dirname(__file__), 'tickets_summary.json')
with open(output_file, 'w') as f:
    json.dump(summary_data, f, indent=4)

print(f"Summary data has been saved to {output_file}")