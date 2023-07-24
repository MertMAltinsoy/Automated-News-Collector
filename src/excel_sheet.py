# excel_sheet.py
import logging

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

from article_source import add_headers, add_source_header, adjust_color, get_source_and_headers


def create_workbook():
    """
    Create a new Excel workbook.

    Returns:
        openpyxl.Workbook: Workbook object.
    """
    try:
        book = openpyxl.Workbook()
        del book['Sheet']
        return book
    except Exception as e:
        logging.exception(f"Error creating Excel workbook: {e}")
        raise


def create_sheet(book, source):
    """
    Create a new sheet with headers.

    Args:
        book: Workbook object.
        source: String representing the source of the data.

    Returns:
        Sheet object.
    """
    try:
        sheet = book.create_sheet(source)
        sourceColor, headers = get_source_and_headers(source)
        headersColor = adjust_color(sourceColor, -20)  # Make the headers color a bit darker
        add_source_header(sheet, source, sourceColor)
        add_headers(sheet, headers, headersColor)
        return sheet
    except Exception as e:
        logging.exception(f"Error creating sheet for source '{source}': {e}")
        raise


def create_or_load_sheet(book, source):
    """
    Create or load a sheet based on the source.

    Args:
        book (openpyxl.Workbook): Workbook object.
        source (str): Source string.

    Returns:
        openpyxl.Workbook: Sheet object.
    """
    if source in book.sheetnames:
        sheet = book[source]
    elif source.startswith('Daily-Updates'):
        sheet = create_sheet(book, source)
        book._sheets.sort(key=lambda sheet: sheet.title != source)
        sheet.column_dimensions['A'].width = 15
        sheet.column_dimensions['B'].width = 110
        sheet.column_dimensions['C'].width = 110
    else:
        sheet = create_sheet(book, source)
        sheet.column_dimensions['A'].width = 110
        sheet.column_dimensions['B'].width = 110
        sheet.column_dimensions['C'].width = 15

    return sheet


def insert_rows(df, sheet):
    """
    Insert rows from DataFrame to the sheet.

    Args:
        df (pandas.DataFrame): DataFrame object.
        sheet (openpyxl.Worksheet): Sheet object.

    Returns:
        None
    """
    for (index, row) in list(df.iterrows())[::-1]:
        sheet.insert_rows(3)
        for (i, value) in enumerate(row.tolist(), start=1):
            cell = sheet.cell(row=3, column=i, value=value)
            cell.alignment = Alignment(horizontal='center', vertical='center')
