import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("favorites")


def get_active_sheet(id, rows, cols=6):
    list = sheet.add_worksheet(id, rows + 5, cols)
    list.update_cell(1, 1, 'trID')
    list.update_cell(1, 2, 'key')
    list.update_cell(1, 3, 'assignee')
    list.update_cell(1, 4, 'creator')
    list.update_cell(1, 5, 'resolution')

    return list
