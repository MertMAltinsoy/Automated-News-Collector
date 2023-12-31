import datetime
import logging
import os
import openpyxl
from news_fetcher import fetch_news
from config import SOURCES, Up_To_Date_NEWS_FILE
from excel_writer import save_articles
from excel_sheet import create_index_sheet
from utils import load_past_articles, save_past_articles

# Configure the logging system
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def is_new_day(current_date, last_reset_date):
    """
    Check if the current date is a new day compared to the last reset date.

    Args:
    current_date (str): The current date in the format "dd-mm-yy".
    last_reset_date (str): The date of the last reset in the format "dd-mm-yy".

    Returns:
    bool: True if the current date is a new day, False otherwise.
    """
    return current_date != last_reset_date


def reset_daily_updates_sheet(workbook, sheet_name):
    """
    Reset the 'Daily-Updates' sheet because a new day has started.

    Args:
    workbook (openpyxl.workbook.workbook.Workbook): The workbook where the sheet is located.
    sheet_name (str): The name of the sheet to be reset.
    """
    logging.info(f"Resetting the 'Daily-Updates' sheet because a new day has started.")
    del workbook[sheet_name]
    workbook.save(Up_To_Date_NEWS_FILE)


def process_articles(source, past_articles):
    """
    Fetch and process new articles for a given source.

    Args:
    source (str): The name of the news source.
    past_articles (dict): A dictionary containing past articles for each source.

    Returns:
    list: A list of tuples containing the source, title, and link of new articles.
    """
    current_articles = fetch_news(source)
    new_articles = [article for article in current_articles if
                    (article[1], article[2]) not in past_articles.get(source, set())]

    if new_articles:
        logging.info(f"Found {len(new_articles)} new articles from {source}.")
        save_articles(new_articles, source)
        # Update the past articles with the current articles
        past_articles[source] = set((article[1], article[2]) for article in current_articles)
        # Add the new articles published today to the daily updates articles
        current_date = datetime.datetime.now().strftime("%d-%m-%y")
        daily_updates_articles = [(source, article[0], article[1]) for article in new_articles if
                                  article[2] == current_date]
        return daily_updates_articles
    else:
        logging.info(f"No new articles found from {source}.")
        return []


def main():
    """
    Main function that fetches news from each source, saves new articles, and updates the Excel file.
    """
    # Get the current date
    current_date = datetime.datetime.now().strftime("%d-%m-%y")

    # Check if the Excel file exists
    if os.path.exists(Up_To_Date_NEWS_FILE):
        # If the file exists, load it
        workbook = openpyxl.load_workbook(Up_To_Date_NEWS_FILE)
        # Get the name of the first sheet and extract the date from it
        first_sheet_name = workbook.sheetnames[0]
        last_reset_date = first_sheet_name.split("Daily-Updates-")[-1]
        if is_new_day(current_date, last_reset_date):
            reset_daily_updates_sheet(workbook, first_sheet_name)

    # Fetch news from each source and save new articles
    past_articles = load_past_articles()
    daily_updates_articles = []

    for source in SOURCES:
        daily_updates_articles.extend(process_articles(source, past_articles))

    save_past_articles(past_articles)
    # Save the daily updates articles to the daily updates sheet
    daily_updates_articles = [(author.replace('-', ' '), title, link) for author, title, link in daily_updates_articles]
    logging.debug(f"Successfully fetched {len(daily_updates_articles)} articles dated {current_date}.")
    save_articles(daily_updates_articles, f"Daily-Updates-{current_date}")
    create_index_sheet()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
