import time
import logging
import os
from news_fetcher import fetch_news
from excel_writer import save_articles
from utils import load_past_articles, save_past_articles, get_last_reset_time, update_last_reset_time, \
    Up_To_Date_NEWS_FILE, PAST_ARTICLES_FILE, SOURCES


def main():
    """Main function."""
    # Check for reset condition and perform reset if necessary
    last_reset_time = get_last_reset_time()
    if time.time() - last_reset_time > 36 * 60 * 60:
        logging.info(f"Resetting the Excel file because the last reset time is more than 36 hours ago.")
        # Reset the Excel File
        if os.path.exists(Up_To_Date_NEWS_FILE):
            os.remove(Up_To_Date_NEWS_FILE)
        # Reset the Past Articles File
        if os.path.exists(PAST_ARTICLES_FILE):
            os.remove(PAST_ARTICLES_FILE)
        update_last_reset_time()

    # Fetch news from each source and save new articles
    past_articles = load_past_articles()
    for source in SOURCES:  # Add more sources as needed
        current_articles = fetch_news(source)
        new_articles = [article for article in current_articles if
                        article[1] not in past_articles.get(source, set())]

        if new_articles:
            logging.info(f"Found {len(new_articles)} new articles from {source}.")
            save_articles(new_articles, source)
            # Update the past articles with the current articles
            past_articles[source] = set(article[1] for article in current_articles)
        else:
            logging.info(f"No new articles found from {source}.")
    save_past_articles(past_articles)


if __name__ == "__main__":
    main()
