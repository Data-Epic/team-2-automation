#  Redmi 6 Review Analysis Automation

This project automates the sentiment analysis and summarization of Redmi 6 customer reviews using AI. It reads reviews from a Google Sheet, uses the Cohere API for analysis, updates the sheet with results, and generates a pie chart summarizing sentiment distribution.

## Project Overview

 - Authenticate with Google Sheets using a service account.

 - Read customer reviews from the sheet.

 - Use Cohere AI (command-r-plus model) to:

 -  Analyze review sentiment (Positive, Negative, Neutral).

 - Summarize each review in one sentence.

 - Write the AI-generated results back into the Google Sheet.

 - Generate a pie chart visualizing sentiment distribution.


## Technologies Used

  - Python

  - gspread

  - Cohere API

  - Matplotlib

  -Google Sheets API

  - OAuth2Client
    

## How to Run

1. Clone the repository.

2.  Install the required Python packages:

```python 
pip install gspread oauth2client cohere matplotlib
```

3. Add your service_account.json credentials file.

4. Replace the Cohere API key with your own in the script.

5. Run the Python script:
```python
   python main.py
   ```

## Project Structure
```css

├── main.py
├── service_account.json
├── README.md
```

## Deliverables

- Python script that automates sentiment analysis and summarization.

- Updated Google Sheet with:

- Sentiment, summary, and action needed columns.

- Pie chart of sentiment distribution.

- Screenshot of the updated Google Sheet.
  

## Contributors

- Ogechukwu Okoli

- Osuala Emmanuella

## Acknowledgment

This project was developed as part of the Data Epic Mentorship Program (2025 Cohort).
