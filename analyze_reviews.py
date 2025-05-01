# analyze_reviews.py

import gspread  # For Google Sheets interaction
from oauth2client.service_account import ServiceAccountCredentials  # For Google Auth
import cohere  # Cohere AI API
import matplotlib.pyplot as plt  # For pie chart
import time
from dotenv import load_dotenv  # For loading environment variables
import os

# Loading environment variables from .env file
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
FINE_TUNED_MODEL_ID = os.getenv("FINE_TUNED_MODEL_ID")  # Store your model ID in .env too

# Step 1: Authenticating Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

# Step 2: Opening the specific Google Sheet and worksheet
spreadsheet = client.open("Redmi Reviews - Team 2")
sheet = spreadsheet.worksheet("Redmi6")

# Step 3: Initializing Cohere API
co = cohere.Client(COHERE_API_KEY)

# Step 4: Set row range (row 12 to 21 means = 11 to 20 in Python)
start_row = 11
end_row = 20

# Storing the results for pie chart
sentiments = []
summaries = []
actions = []


# Step 5: Processing each assigned review
for i in range(start_row, end_row + 1):
    try:
        # Reading the review from column 2 (B)
        review = sheet.cell(i + 1, 2).value

        if not review or not review.strip():
            print(f"Skipping empty row {i + 1}")
            continue

        # Sentiment Classification using Fine-Tuned Model
        classification = co.classify(
            model=FINE_TUNED_MODEL_ID,
            inputs=[review]
        )
        sentiment = classification.classifications[0].prediction
        sentiments.append(sentiment)

        # Summarizing using Cohere Summarize endpoint
        if len(review) < 250:
           summary = review  # original text if too short 
        else:
           summary_response = co.summarize(
           text=review,
           length="short",
           format="paragraph",
           model="command",
           additional_command="Summarize this in one sentence"
            )
           summary = summary_response.summary


        # Action Needed?
        action_needed = "Yes" if sentiment.lower() == "negative" else "No"

        # Writing AI results to Google Sheet (for row i + 1)
        sheet.update_cell(i + 1, 4, sentiment)       # Column D (index 4): AI Sentiment
        sheet.update_cell(i + 1, 5, summary)         # Column E (index 5): AI Summary
        sheet.update_cell(i + 1, 6, action_needed)   # Column F (index 6): Action Needed?

        # Storing the results for pie chart and reference 
        sentiments.append(sentiment)
        summaries.append(summary)
        actions.append(action_needed)


        print(f"✅ Row {i + 1} processed")

        # Pausing by 6 secs to respect Cohere's rate limits (10 calls/minute)
        # time.sleep(6)

    except Exception as e:
        print(f"⚠️ Error on row {i + 1}: {e}")

import json

# Saving results to JSON file
results = {
    "sentiments": sentiments,
    "summaries": summaries,
    "actions": actions
}

with open("results.json", "w") as f:
    json.dump(results, f)

print("📁 Results saved to results.json")


# Step 6: Generate Pie Chart
# Count sentiment types
# labels = list(set(sentiments))
# sizes = [sentiments.count(label) for label in labels]

# Plotting
# plt.figure(figsize=(6, 6))
# plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
# plt.title("Sentiment Breakdown (Rows 11–21)")
# plt.axis('equal')
# plt.savefig("sentiment_pie_chart.png")  # Saves locally

# print("📊 Pie chart saved as 'sentiment_pie_chart.png'. You can upload this to your sheet if needed.")
