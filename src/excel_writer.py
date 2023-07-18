import os
import openpyxl
import time
import pandas as pd
from openpyxl.styles import Font, Border, Side, PatternFill, Alignment
from utils import Up_To_Date_NEWS_FILE, COLORS, get_last_reset_time


def create_workbook():
    """Create a new Excel workbook."""
    book = openpyxl.Workbook()
    # Remove the default sheet
    del book['Sheet']
    return book


def create_sheet(book, source):
    """Create a new sheet with headers."""
    sheet = book.create_sheet(source)
    # Add the source header
    sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=2)
    source_cell = sheet.cell(row=1, column=1, value=source)
    source_cell.font = Font(bold=True, color="FFFFFF", size=16)
    source_cell.fill = PatternFill(start_color=COLORS.get(source, "000000"), end_color=COLORS.get(source, "000000"), fill_type="solid")
    source_cell.alignment = Alignment(horizontal="center", vertical="center")
    # Add the headers
    headers = ['Title', 'Link']
    sheet.append(headers)
    # Make the headers bold, colored, and centered
    color = COLORS.get(source, "000000")  # Get the color for the source
    for cell in sheet[2:2]:
        cell.font = Font(bold=True, color="FFFFFF", size=14)
        cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")
    # Freeze the top two rows
    sheet.freeze_panes = "A3"
    # Add an auto filter
    sheet.auto_filter.ref = f"A2:B{sheet.max_row}"
    return sheet


def add_borders(sheet):
    """Add borders around the cells in the sheet."""
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    for row in sheet.iter_rows(min_row=3, max_row=sheet.max_row - 1):  # Apply border only to the rows that contain the articles
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center")


def change_font(sheet):
    """Change the font of the titles in the sheet."""
    arial_font = Font(name='Arial', size=12)
    for i, row in enumerate(sheet.iter_rows(min_row=3, max_row=sheet.max_row - 1, min_col=1, max_col=1), start=3):  # Apply striping only to the title column
        for cell in row:
            cell.font = arial_font
            if i % 2 == 0:
                cell.fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
            else:
                cell.fill = PatternFill(fill_type=None)  # Clear the fill for the white rows


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
        # If the source sheet doesn't exist, create a new sheet
        sheet = create_sheet(book, source)

    # Insert the rows at the top of the sheet and make the links clickable
    for index, row in list(df.iterrows())[::-1]:
        sheet.insert_rows(3)
        for i, value in enumerate(row.tolist(), start=1):
            cell = sheet.cell(row=3, column=i, value=value)
            if i == 2:  # If this is the 'Link' column
                cell.hyperlink = value
                cell.style = "Hyperlink"
                cell.alignment = Alignment(horizontal="center", vertical="center")  # Center align the links

    # Add/update timestamps
    last_reset_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(get_last_reset_time()))
    last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    if 'Last file reset time' in sheet['A' + str(sheet.max_row)].value and 'Last news update time' in sheet['B' + str(sheet.max_row)].value:
        # If the timestamps already exist, update them
        reset_time_cell = sheet['A' + str(sheet.max_row)]
        update_time_cell = sheet['B' + str(sheet.max_row)]
    else:
        # If the timestamps don't exist, add them
        reset_time_cell = sheet.cell(row=sheet.max_row + 1, column=1)
        update_time_cell = sheet.cell(row=sheet.max_row, column=2)
    reset_time_cell.value = f"Last file reset time: {last_reset_time}"
    update_time_cell.value = f"Last news update time: {last_update_time}"

    add_borders(sheet)
    change_font(sheet)

    # Standardize column widths
    sheet.column_dimensions['A'].width = 110
    sheet.column_dimensions['B'].width = 110

    # Enable text wrapping for columns A and B and center align the text
    for row in sheet.iter_rows(min_row=3, min_col=1, max_col=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')

    return book


def save_articles(articles, source):
    """Save articles to an Excel file."""
    df = pd.DataFrame(articles, columns=['Title', 'Link'])

    # Append to the Excel file (or create a new one if it doesn't exist)
    book = append_to_excel(df, source)

    # Save the Excel file after appending the articles
    book.save(Up_To_Date_NEWS_FILE)
