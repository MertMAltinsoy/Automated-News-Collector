import logging
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))  # Get the directory where the script is located

LOG_DIR = os.path.join(SCRIPT_DIR, '../logs')
DATA_DIR = os.path.join(SCRIPT_DIR, '../data')

LOG_FILE = os.path.join(LOG_DIR, 'logfile.log')
PAST_ARTICLES_FILE = os.path.join(DATA_DIR, 'past_articles.txt')

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
                source, link, date = line.strip().split('|', 2)
                past_articles.setdefault(source, set()).add((link, date))
    except FileNotFoundError:
        pass
    return past_articles


def save_past_articles(past_articles):
    """Save past articles to a file."""
    with open(PAST_ARTICLES_FILE, 'w') as f:
        for source, articles in past_articles.items():
            for link, date in articles:
                f.write(f"{source}|{link}|{date}\n")
