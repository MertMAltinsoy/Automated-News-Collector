from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from config import SOURCE_MAP


def convert_turkish_date_to_datetime(date_string):
    """
    Convert a Turkish date string to a datetime object.

    Parameters:
    date_string (str): The Turkish date string to convert.

    Returns:
    str: The converted date string in the format 'dd-mm-yy'.
    """
    # Map of Turkish month names to English
    turkish_to_numeric_months = {
        'Ocak': '01',
        'Şubat': '02',
        'Mart': '03',
        'Nisan': '04',
        'Mayıs': '05',
        'Haziran': '06',
        'Temmuz': '07',
        'Ağustos': '08',
        'Eylül': '09',
        'Ekim': '10',
        'Kasım': '11',
        'Aralık': '12'
    }
    # Split the date string into day, month, and year
    day, month, year = date_string.split()
    # Convert the Turkish month name to Numeric
    month = turkish_to_numeric_months[month]
    # Combine the day, month, and year into a new date string
    return f"{day}-{month}-{year[2:]}"


def get_soup(url):
    """
    Send a GET request to a URL and return a BeautifulSoup object of the HTML content.

    Parameters:
    url (str): The URL to send the GET request to.

    Returns:
    BeautifulSoup: A BeautifulSoup object of the HTML content of the response.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch news: {e}")
        return None

    return BeautifulSoup(response.content, 'html.parser')


# Parser functions for each news site
def parse_hurriyet(soup):
    """
    Parse the HTML of Hürriyet's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find_all('div', class_='highlighted-box mb20')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('a', class_='title title-news-detail')
        date_tag = news_item.find('div', class_='date')
        link_tag = news_item['data-article-link']
        if title_tag and date_tag and link_tag:
            title = title_tag.text
            link = "https://www.hurriyet.com.tr" + link_tag
            date_string = date_tag.text
            # Split the date string by space and remove the time part
            date_parts = date_string.split()
            date_without_time = " ".join(date_parts[:-1])
            # Convert the Turkish date to a datetime object
            date = convert_turkish_date_to_datetime(date_without_time)
            articles.append((title, link, date))
    return articles


def parse_sabah(soup):
    """
    Parse the HTML of Sabah's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find('div', class_='col-sm-12 view20').find_all('div', class_='col-sm-12')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('strong', class_='postCaption')
        link_tag = news_item.find('a', href=True)
        date_tag = news_item.find('span', class_='postTime')
        if title_tag and link_tag and date_tag:
            title = title_tag.text
            link = "https://www.sabah.com.tr" + link_tag['href']
            date_string = date_tag.text.split()[:-1]  # Exclude the day of the week
            date = convert_turkish_date_to_datetime(" ".join(date_string))
            articles.append((title, link, date))
    return articles


def parse_sozcu(soup):
    """
    Parse the HTML of Sözcü's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find('div', class_='col-lg-8').find_all('a', class_='archive-item')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('span', class_='title')
        date_tag = news_item.find('span', class_='date')
        link_tag = news_item['href']
        if title_tag and date_tag and link_tag:
            title = title_tag.text
            link = link_tag
            date = convert_turkish_date_to_datetime(date_tag.text)
            articles.append((title, link, date))
    return articles


def parse_ekonomim(soup):
    """
    Parse the HTML of Ekonomim's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find('div', class_='col-12 col-lg mw0 author-article_list').find_all('div', class_='left-side')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('a')
        date_tag = news_item.find('span', class_='date')
        if title_tag and date_tag:
            title = title_tag.text
            link = title_tag['href']
            date = convert_turkish_date_to_datetime(date_tag.text)
            articles.append((title, link, date))
    return articles


def parse_10haber(soup):
    """
    Parse the HTML of 10Haber's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find_all('p', class_='card-text')
    articles = []
    for news_item in news_items:
        # Split the text into date and title
        date_and_title = news_item.text.split(' - ', 1)
        if len(date_and_title) == 2:
            date_string, title = date_and_title
            # Convert the Turkish date string to a datetime object
            date = convert_turkish_date_to_datetime(date_string)
            # Get the link
            link = news_item.find('a')['href']
            articles.append((title, link, date))
    return articles


def parse_gazeteoksijen(soup):
    """
    Parse the HTML of GazeteOksijen's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find_all('div', class_='col-12 col-md-6')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('h5', class_='card-title fs-3')
        link_tag = title_tag.find('a', href=True)
        date_tag = news_item.find('span', class_='fs-7')
        if title_tag and link_tag and date_tag:
            title = title_tag.text.strip()
            link = link_tag['href']
            date_string = date_tag.text
            date = convert_turkish_date_to_datetime(date_string)
            articles.append((title, link, date))

    return articles


def parse_mahfiegilmez(soup):
    """
    Parse the HTML of MahfiEğilmez's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    articles = []
    # Parse the top news
    top_news_item = soup.find('article', class_='post')
    if top_news_item:
        title_tag = top_news_item.find('h3', class_='post-title')
        date_tag = top_news_item.find('span', class_='byline post-timestamp')
        link_tag = top_news_item.find('a', class_='timestamp-link')
        if title_tag and date_tag and link_tag:
            title = title_tag.text.strip()
            date = date_tag.text.strip("")
            link = link_tag['href']
            # Adjust the date format and convert it to 'dd-mm-yyyy' format
            date_parts = date.replace(",", "").split()
            date = f"{date_parts[1]} {date_parts[0]} {date_parts[2]}"
            date = convert_turkish_date_to_datetime(date)
            articles.append((title, link, date))

    # Parse the rest of the news
    news_items = soup.find_all('article', class_='post-outer-container')
    for news_item in news_items:
        title_tag = news_item.find('h3', class_='post-title')
        date_tag = news_item.find('span', class_='byline post-timestamp')
        link_tag = news_item.find('a', class_='timestamp-link')
        if title_tag and date_tag and link_tag:
            title = title_tag.text.strip()
            date = date_tag.text.strip()
            link = link_tag['href']
            # Adjust the date format and convert it to 'dd-mm-yyyy' format
            date_parts = date.replace(",", "").split()
            date = f"{date_parts[1]} {date_parts[0]} {date_parts[2]}"
            date = convert_turkish_date_to_datetime(date)
            articles.append((title, link, date))
    return articles


def parse_haberturk(soup):
    """
    Parse the HTML of HaberTürk's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find_all('li', {'class': 'mb-16 pb-8 border-b dark:border-gray-800'})

    articles = []
    for item in news_items:
        title_element = item.find('h3', {'class': 'text-2xl max-w-lg mb-3 font-black'})
        link_element = item.select_one('a.block')
        date_element = item.find('time')

        if title_element and link_element and date_element:
            title = title_element.text.strip()
            link = 'https://www.haberturk.com' + link_element['href']
            date_str = date_element.text.strip().replace('Güncelleme: ', '')

            # Remove leading and trailing spaces
            date_str = date_str.strip()

            # Parse the date string and reformat it
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            formatted_date = date.strftime('%d-%m-%y')

            articles.append((title, link, formatted_date))

    return articles


def parse_yetkinreport(soup):
    """
    Parse the HTML of YetkinReport's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    articles = []
    # Parse the top news
    top_news_items = soup.find_all('div', class_='kl-blog-item-container')
    for item in top_news_items:
        title_and_link_tag = item.find('h3', class_='itemTitle kl-blog-item-title').find('a', href=True)
        if title_and_link_tag:
            title = title_and_link_tag.text.strip()  # Extract the title from the text of the a tag
            link = title_and_link_tag['href']  # Extract the link from the href attribute of the a tag
            # Parse the URL and extract the date
            url_parts = urlparse(link)
            path_parts = url_parts.path.strip("/").split("/")
            if len(path_parts) >= 3:
                year, month, day = path_parts[:3]
                date = f"{day}-{month}-{year[2:]}"
                articles.append((title, link, date))
    return articles


def parse_perspektif(soup):
    """
    Parse the HTML of Perspektif's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find_all('div', class_=['box', 'three', 'small', 'box'])
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('meta', itemprop='name')
        link_tag = news_item.find('meta', itemprop='url')
        date_tag = news_item.find('meta', itemprop='datePublished')

        if title_tag and link_tag and date_tag:
            title = title_tag['content']
            link = link_tag['content']
            date_str = date_tag['content']

            # Parse the date string and reformat it
            formatted_date = convert_turkish_date_to_datetime(date_str)

            articles.append((title, link, formatted_date))

    return articles


def parse_paraanaliz(soup):
    """
    Parse the HTML of Paraanaliz's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find_all('li')
    articles = []
    for news_item in news_items:
        h2_tag = news_item.find('h2')
        if h2_tag is not None:
            title_tag = h2_tag.find('a')
            date_tag = news_item.find('span', class_='yzr_dgr_trh')
            if title_tag and date_tag:
                title = title_tag.text
                link = title_tag['href']
                date = convert_turkish_date_to_datetime(date_tag.text)
                articles.append((title, link, date))
    return articles


def parse_ugurses(soup):
    """
    Parse the HTML of UgurGürses's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find('article')
    articles = []
    title_tag = news_items.find('h2', class_='entry-title').find('a')
    link_tag = title_tag
    date_tag = news_items.find('span', class_='posted-on').find('time', class_='entry-date published')
    if title_tag and link_tag and date_tag:
        title = title_tag.text
        link = link_tag['href']
        date = datetime.strptime(date_tag['datetime'].split('T')[0], '%Y-%m-%d')
        date = date.strftime('%d-%m-%y')  # format the date as 'dd-mm-yy'
        articles.append((title, link, date))
    return articles


#  For a new Parser function addition, add the name of the function with its string value to the below
#  parsers list. Do NOT forget to implement the actual corresponding parser function as well.
parsers = {

    'parse_hurriyet': parse_hurriyet,
    'parse_sabah': parse_sabah,
    'parse_sozcu': parse_sozcu,
    'parse_ekonomim': parse_ekonomim,
    'parse_10haber': parse_10haber,
    'parse_gazeteoksijen': parse_gazeteoksijen,
    'parse_mahfiegilmez': parse_mahfiegilmez,
    'parse_haberturk': parse_haberturk,
    'parse_yetkinreport': parse_yetkinreport,
    'parse_perspektif': parse_perspektif,
    'parse_paraanaliz': parse_paraanaliz,
    'parse_ugurses': parse_ugurses
}


def fetch_news(source):
    """
    Fetch news from a specific source.

    Parameters:
    source (str): The name of the news source to fetch news from.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    if source in SOURCE_MAP:
        url = SOURCE_MAP[source]["url"]
        parser = parsers[SOURCE_MAP[source]["parser"]]
        soup = get_soup(url)
        if soup is None:
            logging.error("Failed to fetch articles: No internet connection, invalid URL, or other network issue.")
            return []
        articles = parser(soup)
        logging.debug(f"Fetched {len(articles)} articles from {source}.")
        return articles
    else:
        logging.error(f"Unknown source: {source}")
        return []