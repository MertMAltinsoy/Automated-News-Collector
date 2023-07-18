import logging
import os
import time

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))  # Get the directory where the script is located

LOG_DIR = os.path.join(SCRIPT_DIR, '../logs')
DATA_DIR = os.path.join(SCRIPT_DIR, '../data')

LOG_FILE = os.path.join(LOG_DIR, 'logfile.log')
PAST_ARTICLES_FILE = os.path.join(DATA_DIR, 'past_articles.txt')
Up_To_Date_NEWS_FILE = os.path.join(DATA_DIR, 'Up_To_Date_NEWS.xlsx')
LAST_RESET_FILE = os.path.join(DATA_DIR, 'last_reset.txt')

SOURCES = ["Reuters-Finance", "Nagehan-Alci", "Dilek-Gungor", "Deniz-Zeyrek", "Sant-Manukyan"]

COLORS = {
    "Reuters-Finance": "800000",  # Dark Red
    "Dilek-Gungor": "804000",  # Brown
    "Nagehan-Alci": "808000",  # Olive
    "Deniz-Zeyrek": "408000",  # Dark Green
    "Sant-Manukyan": "008000",  # Green
    "Source-6": "008080",  # Teal
    "Source-7": "000080",  # Navy
    "Source-8": "400080",  # Dark Purple
    "Source-9": "800080",  # Purple
    "Source-10": "800040",  # Dark Magenta
}

# Create the logs and data directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_past_articles():
    """Load past articles from a file."""
    past_articles = {}
    try:
        with open(PAST_ARTICLES_FILE, 'r') as f:
            for line in f:
                source, article = line.strip().split('|', 1)
                past_articles.setdefault(source, set()).add(article)
    except FileNotFoundError:
        pass
    return past_articles


def save_past_articles(past_articles):
    """Save past articles to a file."""
    with open(PAST_ARTICLES_FILE, 'w') as f:
        for source, articles in past_articles.items():
            for article in articles:
                f.write(f"{source}|{article}\n")


def get_last_reset_time():
    """Get the last reset time from the file. If the file doesn't exist, return 0."""
    if os.path.exists(LAST_RESET_FILE):
        with open(LAST_RESET_FILE, 'r') as f:
            return float(f.read())
    else:
        return 0


def update_last_reset_time():
    """Update the last reset time in the file to the current time."""
    with open(LAST_RESET_FILE, 'w') as f:
        f.write(str(time.time()))
