
import gspread
import cohere
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
load_dotenv()

# === Setup Google Sheets and Drive API credentials ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

# Google Drive API
drive_creds = Credentials.from_service_account_file('service_account.json', scopes=["https://www.googleapis.com/auth/drive"])
drive_service = build('drive', 'v3', credentials=drive_creds)

# To open the Google Sheet and get data
spreadsheet = client.open("Redmi Reviews - Team 2")
sheet = spreadsheet.worksheet("Redmi6")

co = cohere.Client(os.getenv("COHERE_API_KEY"))  # Your Cohere API key

sentiments = sheet.col_values(4)[1:]  # Exclude header
if not sentiments:
    raise ValueError("Sentiments does not exist in sheet Redmi6")

# Count sentiment occurrences
sentiments_count = {} # empty dictionary to store sentiment counts
for sentiment in sentiments:
    if sentiment in sentiments_count:
        sentiments_count[sentiment] += 1
    else:
        sentiments_count[sentiment] = 1

# Plot and save the pie chart
plt.figure(figsize=(12, 10))  # Adjust the figure size
plt.pie(sentiments_count.values(), labels=sentiments_count.keys(), startangle=90, textprops={"rotation": 45})
plt.title("Sentiments distribution")
plt.savefig("sentiments_distribution.png", bbox_inches='tight')
plt.close()

# Upload image to Google Drive
file_metadata = {'name': 'sentiments_distribution.png'}
media = MediaFileUpload('sentiments_distribution.png', mimetype='image/png')
file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
file_id = file['id']

# Make the file publicly accessible
drive_service.permissions().create(
    fileId=file_id,
    body={"type": "anyone", "role": "reader"},
).execute()

# Construct the public image URL
image_url = f"https://drive.google.com/uc?id={file_id}"
cell_list = sheet.range(f"G1:G10")
for cell in cell_list:
    cell.value = f'=IMAGE("{image_url}", 4, 500, 300)'
sheet.update_cells(cell_list)
print("Pie chart created and uploaded successfully.")
