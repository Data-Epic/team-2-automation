# Importing necessary libraries
import gspread  # For working with Google Sheets
from oauth2client.service_account import ServiceAccountCredentials  # For Google API auth
import cohere  # For AI processing with Cohere
import matplotlib.pyplot as plt  # For creating the pie chart
import time

# Step 1: Authenticating with Google Sheets using service account
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

# Step 2: Opening the Google Sheet and the specific worksheet
spreadsheet = client.open("Redmi Reviews - Team 2")
sheet = spreadsheet.worksheet("Redmi6")

# Step 3: Reading reviews (from column 2), excluding the header
reviews = sheet.col_values(2)[1:]
unique_reviews = list(set(reviews))  # Remove duplicates

# Step 4: Initializing Cohere API
co = cohere.Client("20rc2Yw4NcBmVJSAxjzOsuqiXx0KKIQt3yPJRhR5")  # Your Cohere API key

# Step 5: Preparing the lists to collect results
sentiments = []
summaries = []
actions = []

# Step 6: Processing each review with the Cohere `chat` API
for i, review in enumerate(reviews):
    if not review.strip():
        continue  # Skip empty cells

    # Building the message prompt for chat
    message = f"""Analyze the following customer review:
    Review: "{review}"
    Tasks:
    1. Determine if the sentiment is Positive, Negative, or Neutral.
    2. Provide a one-sentence summary of the review.
    Respond in this format:
    Sentiment: <Positive/Negative/Neutral>
    Summary: <One sentence summary>
    """

    try:
        # Using chat endpoint
        response = co.chat(
            model="command-r-plus",  # Changed it to the latest supported model
            message=message,
            temperature=0.3
        )

        result = response.text.strip()
        print(f"\nCohere chat response for row {i+2}:\n{result}\n")

        # Extracting the sentiment and summary from responses
        sentiment_line = [line for line in result.splitlines() if "Sentiment:" in line][0]
        summary_line = [line for line in result.splitlines() if "Summary:" in line][0]

        sentiment = sentiment_line.replace("Sentiment:", "").strip()
        summary = summary_line.replace("Summary:", "").strip()

        # Using the original text as summary if it is too short to summarize
        if len(review.split()) < 6:
            summary = review

        #  "Yes" for action if Negative sentiment
        action_needed = "Yes" if sentiment.lower() == "negative" else "No"

        # Write AI results to Google Sheet
       # Updating Google Sheet 
        sheet.update_cell(i + 2, 4, sentiment)       # Column D = AI Sentiment
        sheet.update_cell(i + 2, 5, summary)         # Column E = AI Summary
        sheet.update_cell(i + 2, 6, action_needed)   # Column F = Action Needed?


        # Store results
        sentiments.append(sentiment)
        summaries.append(summary)
        actions.append(action_needed)

        # Adding a 6 seconds delay because of the 10 calls per minute rate limits
        time.sleep(6)


    except Exception as e:
        print(f"⚠️ Error processing row {i + 2}: {e}")

