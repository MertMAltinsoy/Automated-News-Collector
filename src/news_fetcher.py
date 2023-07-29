from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from config import SOURCE_MAP
import random


def convert_turkish_date_to_datetime(date_string):
    """
    Convert a Turkish date string to a datetime object.

    Parameters:
    date_string (str): The Turkish date string to convert.

    Returns:
    str: The converted date string in the format 'dd-mm-yy'.
    """
    # Map of Turkish month names and abbreviations to English
    turkish_to_numeric_months = {
        'Ocak': '01', 'Oca': '01',
        'Şubat': '02', 'Şub': '02',
        'Mart': '03', 'Mar': '03',
        'Nisan': '04', 'Nis': '04',
        'Mayıs': '05', 'May': '05',
        'Haziran': '06', 'Haz': '06',
        'Temmuz': '07', 'Tem': '07',
        'Ağustos': '08', 'Ağu': '08',
        'Eylül': '09', 'Eyl': '09',
        'Ekim': '10', 'Eki': '10',
        'Kasım': '11', 'Kas': '11',
        'Aralık': '12', 'Ara': '12'
    }
    # Split the date string into day, month, and year
    day, month, year = date_string.split()
    # Convert the Turkish month name or abbreviation to Numeric
    month = turkish_to_numeric_months[month]
    # Combine the day, month, and year into a new date string
    return f"{day}-{month}-{year[2:]}"


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
]

session = requests.Session()
session.headers.update({
    'User-Agent': random.choice(user_agents),
    'Accept-Language': 'tr-TR,tr;q=0.9'
})


def get_soup(url):
    """
    Send a GET request to a URL and return a BeautifulSoup object of the HTML content.

    Parameters:
    url (str): The URL to send the GET request to.

    Returns:
    BeautifulSoup: A BeautifulSoup object of the HTML content of the response.
    """
    try:
        response = session.get(url)
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
            # Split the date string by space and remove the time part if it exists
            date_parts = date_string.split()
            if len(date_parts) > 3:  # If the date string contains a time part
                date_without_time = " ".join(date_parts[:-1])
            else:
                date_without_time = date_string
            try:
                # Convert the Turkish date to a datetime object
                date = convert_turkish_date_to_datetime(date_without_time)
                articles.append((title, link, date))
            except ValueError:
                logging.error(f"Failed to parse date: '{date_without_time}'")
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
    Parse the HTML of UğurGürses's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_item = soup.find('article')
    articles = []
    title_tag = news_item.find('h2', class_='entry-title').find('a')
    link_tag = title_tag
    date_tag = news_item.find('span', class_='posted-on').find('time', class_='entry-date published')
    if title_tag and link_tag and date_tag:
        title = title_tag.text
        link = link_tag['href']
        date = datetime.strptime(date_tag['datetime'].split('T')[0], '%Y-%m-%d')
        date = date.strftime('%d-%m-%y')  # format the date as 'dd-mm-yy'
        articles.append((title, link, date))
    return articles


def parse_yenisafak(soup):
    """
    Parse the HTML of Yenişafak's page.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing the HTML content of the author's page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    articles = []
    # First, find the parent element
    left_content = soup.find('div', class_='left-content')

    # Check if the parent element was found
    if left_content is not None:
        # Then, find the news items within the 'cards-list' element
        news_items = left_content.find_all('div', class_='ys-link')
    else:
        # If the parent element was not found, log an error and set news_items to an empty list
        logging.error('Failed to find left-content element')
        news_items = []
    for item in news_items:
        h2 = item.find('h2')
        # Check if the h2 element was found
        if h2 is not None:
            title = h2.text.strip()
            link = "https://www.yenisafak.com" + item.find('a')['href']
            date = item.find('p', class_='date').text.strip()
            # Split the date string into its components
            components = date.split()
            # Remove the comma from the year
            components[2] = components[2].replace(',', '')
            # Reorder the components and join them back into a string
            date = ' '.join([components[1], components[0], components[2]])
            try:
                date = convert_turkish_date_to_datetime(date)  # format the date as 'dd-mm-yy'
            except KeyError as e:
                logging.error(f"Failed to convert date: {date}. Error: {e}")
                continue
            articles.append((title, link, date))
        else:
            # If the h2 element was not found, log a debug message
            logging.debug('Found a ys-link element without an h2 element')

    return articles


def parse_birgun(soup):
    """
    Parse the HTML of Birgün's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    news_items = soup.find_all('div', class_='col-12')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('h5', class_='card-title')
        if title_tag:
            title_tag = title_tag.find('a')
        date_tag = news_item.find('li', class_='nav-item no-line')
        if title_tag and date_tag:
            title = title_tag.text
            link = "https://www.birgun.net" + title_tag['href']
            date = datetime.strptime(date_tag.text, '%d.%m.%Y %H:%M')
            date = date.strftime('%d-%m-%y')  # format the date as 'dd-mm-yy'
            articles.append((title, link, date))
    return articles


def parse_gazeteduvar(soup):
    """
    Parse the HTML of GazeteDuvar's page.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object of the HTML content of the page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    articles = []
    news_items = soup.find_all('div', class_='col-12 col-md-6')
    for item in news_items:
        date_tag = item.find('span', class_='time')
        link_tag = item.find('a')
        if date_tag and link_tag:
            date = date_tag.text.replace(',', '').strip()  # remove commas and leading/trailing whitespaces
            date = date.split(' ')[1:]  # remove the day of the week
            date = ' '.join(date)  # join the remaining parts
            date = convert_turkish_date_to_datetime(date)  # convert the date to 'dd-mm-yy' format
            title = link_tag['title']
            link = link_tag['href']
            articles.append((title, link, date))
    return articles


def parse_t24(soup):
    """
    Parse articles from T24.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing the HTML content of the author's page.

    Returns:
    list: A list of tuples, where each tuple contains the title, link, and date of an article.
    """
    articles = []
    # First, find the parent element
    parent_element = soup.find('div', class_='col-md-8 col-sm-12 col-xs-12')
    # Check if the parent element was found
    if parent_element is not None:
        # Then, find the news items within the '1fE_V' element
        news_items = parent_element.find('div', class_='_2Mepd').find_all('div', class_='_1fE_V')
    else:
        # If the parent element was not found, log an error and set news_items to an empty list
        logging.error('Failed to find parent element')
        news_items = []
    for item in news_items:
        date_tag = item.find('div', class_='_2J9OF col-sm-3 col-xs-12').find_all('p')[-1]
        link_tag = item.find('div', class_='_31Tbh col-sm-9 col-xs-12').find('h3').find('a')
        if date_tag and link_tag:
            date = date_tag.text.strip()
            date = convert_turkish_date_to_datetime(date)
            title = link_tag.text.strip()
            link = "https://t24.com.tr" + link_tag['href']
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
    'parse_ugurses': parse_ugurses,
    'parse_yenisafak': parse_yenisafak,
    'parse_birgun': parse_birgun,
    'parse_gazeteduvar': parse_gazeteduvar,
    'parse_t24': parse_t24
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
