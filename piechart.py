import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cohere
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
FINE_TUNED_MODEL_ID = os.getenv("FINE_TUNED_MODEL_ID")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

if not SPREADSHEET_ID:
    raise ValueError("SPREADSHEET_ID not set in .env file.")

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

# Open the specific sheet
spreadsheet = client.open("Redmi Reviews - Team 2")
sheet = spreadsheet.worksheet("Redmi6")

# Initialize Cohere (optional – not used in this chart generation)
co = cohere.Client(COHERE_API_KEY)

# Get sentiments and create pie chart
sentiments = sheet.col_values(4)[11:22]
labels = list(set(sentiments))
sizes = [sentiments.count(label) for label in labels]
colors = ['#2ca02c', '#1f77b4']

plt.figure(figsize=(10, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True,
        textprops={'fontsize': 10, "fontweight": "bold", 'fontname': 'Verdana'})

# Add custom font to legend title
legend_font = FontProperties(family='Verdana', weight='bold')
plt.legend(labels, title="Breakdown", title_fontproperties=legend_font, loc="upper right")

plt.title("Sentiment breakdown of rows(12–21)", fontdict={
    'fontsize': 15,
    'fontweight': 'bold',
    'fontname': 'Verdana',
    'color': 'black'
})
plt.axis("equal")
plt.savefig("Sentiments_piechart.png")
plt.show()

# Upload image to Google Drive
def upload_image_to_drive():
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': 'Sentiments_piechart.png',
        'mimeType': 'image/png'
    }
    media = MediaFileUpload('Sentiments_piechart.png', mimetype='image/png')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Make the file public
    file_id = file.get('id')
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file_id, body=permission).execute()
    return file_id

# Insert image via IMAGE formula into Google Sheets
def insert_image_formula_into_sheet(spreadsheet_id, image_file_id):
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    service = build('sheets', 'v4', credentials=creds)

    image_url = f'https://drive.google.com/uc?id={image_file_id}'

    # Option 4 lets you control the size (300x200 px here, adjust as needed)
    formula = f'=IMAGE("{image_url}", 4, 600, 600)'

    body = {
        'values': [[formula]]
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="Redmi6!G11",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

    print("Image inserted using formula into cell G11")

# Main function
def main():
    image_file_id = upload_image_to_drive()
    insert_image_formula_into_sheet(SPREADSHEET_ID, image_file_id)

# Execute script
main()
