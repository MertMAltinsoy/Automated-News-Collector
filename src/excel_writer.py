import logging
import os
import openpyxl
import pandas as pd
from openpyxl.styles import Font, Border, Side, PatternFill, Alignment, Color
from src.config import COLORS, Up_To_Date_NEWS_FILE


def create_workbook():
    """Create a new Excel workbook."""
    try:
        book = openpyxl.Workbook()
        # Remove the default sheet
        del book['Sheet']
        return book
    except Exception as e:
        logging.exception(f"Error creating Excel workbook: {e}")
        raise


def create_sheet(book, source):
    """Create a new sheet with headers."""
    try:
        sheet = book.create_sheet(source)

        # Get the color for the source
        if source.startswith("Daily-Updates"):
            sourceColor = COLORS['Daily-Updates']
            headers = ['Author', 'Title', 'Link']
            headersColor = adjust_color(sourceColor, -20)  # Make the headers color a bit darker
        else:
            sourceColor = COLORS.get(source)
            headers = ['Title', 'Link', 'Date']
            headersColor = adjust_color(sourceColor, -20)  # Make the headers color a bit darker

        # Add the source header
        stripped_source = replace_dash_with_space(source)
        sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=3)
        source_cell = sheet.cell(row=1, column=1, value=stripped_source)
        source_cell.font = Font(bold=True, color="FFFFFF", size=16)
        source_cell.fill = PatternFill(start_color=sourceColor, end_color=sourceColor, fill_type="solid")
        source_cell.alignment = Alignment(horizontal="center", vertical="center")
        # Add the headers
        sheet.append(headers)
        # Make the headers bold, colored, and centered
        for cell in sheet[2:2]:
            cell.font = Font(bold=True, color="FFFFFF", size=14)
            cell.fill = PatternFill(start_color=headersColor, end_color=headersColor, fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
        # Freeze the top two rows
        sheet.freeze_panes = "A3"
        # Add an auto filter
        sheet.auto_filter.ref = f"A2:C{sheet.max_row}"
        return sheet
    except Exception as e:
        logging.exception(f"Error creating sheet for source '{source}': {e}")
        raise


def replace_dash_with_space(source):
    try:
        if source.startswith("Daily-Updates"):
            # Replace only the first two dashes with spaces
            return source.replace("-", " ", 2)
        else:
            # Replace all dashes with spaces
            return source.replace("-", " ")
    except Exception as e:
        logging.exception(f"Error replacing dashes with spaces in source '{source}': {e}")
        raise


def adjust_color(color, amount):
    """Adjust the brightness of a color."""
    try:
        # Convert the color to RGB
        r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
        # Adjust the brightness
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        # Convert back to hex
        adjusted_color = "{:02x}{:02x}{:02x}".format(r, g, b)
        return adjusted_color
    except Exception as e:
        logging.exception(f"Error adjusting color '{color}': {e}")
        raise


def change_font_daily_updates(sheet):
    """Change the font of the titles and authors in the sheet."""
    title_font = Font(name='Arial', size=14, bold=True)
    author_font = Font(name='Times New Roman', size=12, italic=True)
    try:
        for i, row in enumerate(sheet.iter_rows(min_row=3, min_col=1, max_col=3), start=3):
            for j, cell in enumerate(row, start=1):
                if j == 1:  # If this is the 'Author' column
                    cell.font = author_font
                elif j == 2:  # If this is the 'Title' column
                    cell.font = title_font
                if i % 2 == 0:
                    cell.fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
                else:
                    cell.fill = PatternFill(fill_type=None)  # Clear the fill for the white rows
    except Exception as e:
        logging.exception(f"Error while changing font in sheet '{sheet.title}': {e}")
        raise


def change_font_author(sheet):
    """Change the font of the titles in the sheet."""
    title_font = Font(name='Arial', size=14)
    date_font = Font(name='Consolas', size=12)
    try:
        for i, row in enumerate(sheet.iter_rows(min_row=3, min_col=1, max_col=3), start=3):
            for j, cell in enumerate(row, start=1):
                if j == 1:  # If this is the 'Title' column
                    cell.font = title_font
                elif j == 3:  # If this is the 'Date' column
                    cell.font = date_font
                if i % 2 == 0:
                    cell.fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
                else:
                    cell.fill = PatternFill(fill_type=None)  # Clear the fill for the white rows
    except Exception as e:
        logging.exception(f"Error while changing font in sheet '{sheet.title}': {e}")
        raise


def add_borders_daily_updates(sheet):
    """Add borders around the cells in the sheet."""
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    try:
        for row in sheet.iter_rows(min_row=3,
                                   max_row=sheet.max_row):  # Apply border only to the rows that contain the articles
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="center", vertical="center")
    except Exception as e:
        logging.exception(f"Error while applying border to sheet '{sheet.title}': {e}")
        raise


def add_borders_author(sheet):
    """Add borders around the cells in the sheet."""
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    try:
        for row in sheet.iter_rows(min_row=3,
                                   max_row=sheet.max_row):  # Apply border only to the rows that contain the articles
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="center", vertical="center")
    except Exception as e:
        logging.exception(f"Error while applying border to sheet '{sheet.title}': {e}")
        raise


def append_to_excel(df, source):
    """Insert the DataFrame to the Excel file."""
    if os.path.exists(Up_To_Date_NEWS_FILE):
        book = openpyxl.load_workbook(Up_To_Date_NEWS_FILE)
    else:
        book = create_workbook()

    if source in book.sheetnames:
        # If the source sheet exists, insert data to it
        sheet = book[source]
    else:
        # If the source is 'Daily-Updates', create the sheet with headers and move it to the first position
        if source.startswith("Daily-Updates"):
            sheet = create_sheet(book, source)
            book._sheets.sort(key=lambda sheet: sheet.title != source)
            # Standardize column widths
            sheet.column_dimensions['A'].width = 15
            sheet.column_dimensions['B'].width = 110
            sheet.column_dimensions['C'].width = 110
        # If the author source sheet doesn't exist, create a new sheet
        else:
            sheet = create_sheet(book, source)
            # Standardize column widths
            sheet.column_dimensions['A'].width = 110
            sheet.column_dimensions['B'].width = 110
            sheet.column_dimensions['C'].width = 15

    # Insert the rows at the top of the sheet
    for index, row in list(df.iterrows())[::-1]:
        sheet.insert_rows(3)
        for i, value in enumerate(row.tolist(), start=1):
            cell = sheet.cell(row=3, column=i, value=value)
            cell.alignment = Alignment(horizontal="center", vertical="center")  # Center align the links

    # Make the links clickable
    for row in sheet.iter_rows(min_row=3, max_row=sheet.max_row):
        for i, cell in enumerate(row, start=1):
            if (source.startswith("Daily-Updates") and i == 3) or (
                    not source.startswith("Daily-Updates") and i == 2):  # If this is the 'Link' column
                cell.hyperlink = cell.value
                cell.style = "Hyperlink"

    # If the number of articles exceeds 50, remove the oldest articles
    if not source.startswith("Daily-Updates"):  # Don't limit the number of articles for 'Daily-Updates'
        while sheet.max_row - 2 > 50:  # Subtract 2 because the first two rows are headers
            sheet.delete_rows(sheet.max_row)  # Delete the last row, which is the oldest article

    if source.startswith("Daily-Updates"):
        add_borders_daily_updates(sheet)
        change_font_daily_updates(sheet)
    else:
        add_borders_author(sheet)
        change_font_author(sheet)

    # Enable text wrapping for columns A and B and center align the text
    for row in sheet.iter_rows(min_row=3, min_col=1, max_col=3):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')

    return book


def save_articles(articles, source):
    """Save articles to an Excel file."""
    if source.startswith("Daily-Updates"):
        df = pd.DataFrame(articles, columns=['Source', 'Title', 'Link'])
    else:
        df = pd.DataFrame(articles, columns=['Title', 'Link', 'Date'])

    # Append to the Excel file (or create a new one if it doesn't exist)
    book = append_to_excel(df, source)

    # Save the Excel file after appending the articles
    book.save(Up_To_Date_NEWS_FILE)
