import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # importing library for the formatting the legend of the pie ch
from dotenv import load_dotenv # importing the library for loading environment variables
import os # os module
import gspread # library for interacting with Gspread
from oauth2client.service_account import ServiceAccountCredentials # library for aunthentication
import cohere # cohere library
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload # library for uploading files bia google api

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
FINE_TUNED_MODEL_ID = os.getenv("FINE_TUNED_MODEL_ID")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
# checking for the existence of the environment variable
if not SPREADSHEET_ID:
    raise ValueError("SPREADSHEET_ID not set in .env file.")

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

# Opening the spreadsheet
spreadsheet = client.open("Redmi Reviews - Team 2")
sheet = spreadsheet.worksheet("Redmi6")

# Initialize Cohere
co = cohere.Client(COHERE_API_KEY)

# Get sentiments and create pie chart for rows 11-21 in the spreadsheet
sentiments = sheet.col_values(4)[11:22]
labels = list(set(sentiments)) # labels
sizes = [sentiments.count(label) for label in labels] # counting the percentages of negative and positives
colors = ['#2ca02c', '#1f77b4'] # picking colors

plt.figure(figsize=(10, 6)) # size of the pie chart
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True,
        textprops={'fontsize': 10, "fontweight": "bold", 'fontname': 'Verdana'}) #plotting the piechart
# Add custom font to legend title using FONTPROPERTIES
legend_font = FontProperties(family='Verdana', weight='bold')
plt.legend(labels, title="Breakdown", title_fontproperties=legend_font, loc="upper right")

plt.title("Sentiment breakdown of rows(12–21)", fontdict={
    'fontsize': 15,
    'fontweight': 'bold',
    'fontname': 'Verdana',
    'color': 'black'
})# styling the title of my pie chart
plt.axis("equal")
plt.savefig("Sentiments_piechart.png")# name of the pie chart
plt.show() # displaying the chart

# Upload image to Google Drive
def upload_image_to_drive():
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': 'Sentiments_piechart.png',
        'mimeType': 'image/png'
    } # datatype of the uploaded file
    media = MediaFileUpload('Sentiments_piechart.png', mimetype='image/png') #uploading the file
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

    #using formula method to insert image by specifying the image size
    formula = f'=IMAGE("{image_url}", 4, 600, 600)'

    body = {
        'values': [[formula]]
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="Redmi6!G11", # position of the image
        valueInputOption="USER_ENTERED", #values are stored as if it was user typed and google sheets evalutes ut to display the image
        body=body
    ).execute()
    print("Image inserted using formula into cell G11") # confirmation message that the image has been inserted into the file

# Main function
def main():
    image_file_id = upload_image_to_drive() # callin the function to upload image
    insert_image_formula_into_sheet(SPREADSHEET_ID, image_file_id) # calling the function that inserts the pie chart into the spreadsheet and it takes two parameters.
# Execute script
main() # calling the main function
