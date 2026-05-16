import gspread

from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(
    "credentials/google.json",
    scopes=SCOPES,
)

client = gspread.authorize(creds)

spreadsheet = client.open_by_key("10bc1iB9g0sc26x8mpNeEcGGy6naXMkfvBaWPTIbyhx0")

operations_sheet = spreadsheet.worksheet("operations")