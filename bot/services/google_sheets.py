import logging

import gspread

from google.oauth2.service_account import Credentials

from bot.config import GOOGLE_SHEET_ID

from bot.database.database import SessionLocal

from bot.models.expense import Expense


logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


_spreadsheet = None

_operations_sheet = None


def _get_spreadsheet():
    global _spreadsheet

    if _spreadsheet is None:

        creds = Credentials.from_service_account_file(
            "credentials/google.json",
            scopes=SCOPES,
        )

        logger.info(
            "Google Sheets: аутентификация как %s, открываю таблицу GOOGLE_SHEET_ID=%r",
            creds.service_account_email,
            GOOGLE_SHEET_ID,
        )

        client = gspread.authorize(creds)

        _spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

    return _spreadsheet


def _get_operations_sheet():
    global _operations_sheet

    if _operations_sheet is None:
        _operations_sheet = _get_spreadsheet().worksheet("operations")

    return _operations_sheet


def get_worksheet_values(sheet_name):
    return _get_spreadsheet().worksheet(sheet_name).get_all_values()


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
        expense.type,
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
        "type",
    ])

    rows = [
        _expense_to_row(expense)
        for expense in expenses
    ]

    if rows:
        sheet.append_rows(rows)
