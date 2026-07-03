import gspread

from google.oauth2.service_account import Credentials

from bot.config import GOOGLE_SHEET_ID

from bot.database.database import SessionLocal

from bot.models.expense import Expense


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


_operations_sheet = None


def _get_operations_sheet():
    global _operations_sheet

    if _operations_sheet is None:

        creds = Credentials.from_service_account_file(
            "credentials/google.json",
            scopes=SCOPES,
        )

        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

        _operations_sheet = spreadsheet.worksheet("operations")

    return _operations_sheet


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

    _get_operations_sheet().append_row(
        _expense_to_row(expense)
    )


def append_expenses(expenses):

    if not expenses:
        return

    rows = [
        _expense_to_row(e)
        for e in expenses
    ]

    _get_operations_sheet().append_rows(rows)


def rewrite_sheet():

    db = SessionLocal()

    try:
        expenses = (
            db.query(Expense)
            .order_by(Expense.id.asc())
            .all()
        )
    finally:
        db.close()

    sheet = _get_operations_sheet()

    sheet.clear()

    sheet.append_row([
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
        sheet.append_rows(rows)
