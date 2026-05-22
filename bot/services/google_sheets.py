import gspread

from google.oauth2.service_account import Credentials

from bot.database.database import SessionLocal

from bot.models.expense import Expense


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


creds = Credentials.from_service_account_file(
    "credentials/google.json",
    scopes=SCOPES,
)


client = gspread.authorize(creds)


spreadsheet = client.open_by_key(
    "10bc1iB9g0sc26x8mpNeEcGGy6naXMkfvBaWPTIbyhx0"
)


operations_sheet = spreadsheet.worksheet("operations")


def _expense_to_row(expense):
    created_at_str = ""
    if expense.created_at:
        created_at_str = expense.created_at.strftime("%d.%m.%Y %H:%M")

    return [
        expense.id,
        created_at_str,
        expense.creator,
        expense.owner,
        expense.category,
        expense.amount,
        expense.comment,
    ]


def append_expense(expense):

    operations_sheet.append_row(
        _expense_to_row(expense)
    )


def append_expenses(expenses):

    if not expenses:
        return

    rows = [
        _expense_to_row(e)
        for e in expenses
    ]

    operations_sheet.append_rows(rows)


def rewrite_sheet():

    db = SessionLocal()

    expenses = (
        db.query(Expense)
        .order_by(Expense.id.asc())
        .all()
    )

    operations_sheet.clear()

    operations_sheet.append_row([
        "id",
        "created_at",
        "creator",
        "owner",
        "category",
        "amount",
        "comment",
    ])

    rows = [
        _expense_to_row(expense)
        for expense in expenses
    ]

    if rows:
        operations_sheet.append_rows(rows)

    db.close()