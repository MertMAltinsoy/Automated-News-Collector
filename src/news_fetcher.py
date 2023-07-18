import requests
from bs4 import BeautifulSoup
import logging


def get_soup(url):
    """Send a GET request to a URL and return a BeautifulSoup object of the HTML content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch news: {e}")
        return None

    return BeautifulSoup(response.content, 'html.parser')


def parse_reuters(soup):
    """Parse the HTML of the Reuters finance page."""
    news_items = soup.find_all('li', class_=['story-collection__story__LeZ29', 'story-collection__hero__2gK6-'])
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('h3')
        if title_tag:
            title = title_tag.text
            link = "https://www.reuters.com" + news_item.find('a')['href']
            articles.append((title, link))
    return articles


def parse_nagehan_alci(soup):
    """Parse the HTML of Nagehan Alçı's page."""
    news_items = soup.find_all('li', class_=['w-full border-dotted mb-5 pb-5 border-b dark:border-gray-800'])
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('span', class_='block font-black mb-2.5')
        link_tag = news_item.find('a',
                                  class_='inline-block font-bold py-2.5 px-7 text-center border dark:border-gray-800')
        if title_tag and link_tag:
            title = title_tag.text
            link = "https://www.haberturk.com" + link_tag['href']
            articles.append((title, link))
    return articles


def parse_dilek_gungor(soup):
    """Parse the HTML of Dilek Güngör's page."""
    target_div = soup.find('div', class_='col-sm-12 view20')
    news_items = target_div.find_all('div', class_='col-sm-12')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('strong', class_='postCaption')
        link_tag = news_item.find('a', href=True)
        if title_tag and link_tag:
            title = title_tag.text
            link = "https://www.sabah.com.tr" + link_tag['href']
            articles.append((title, link))
    return articles


def parse_deniz_zeyrek(soup):
    """Parse the HTML of Deniz Zeyrek's page."""
    news_items = soup.find('div', class_='col-lg-8').find_all('a', class_='archive-item')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('span', class_='title')
        date_tag = news_item.find('span', class_='date')
        link_tag = news_item['href']
        if title_tag and date_tag and link_tag:
            title = title_tag.text
            link = link_tag
            articles.append((title, link))
    return articles


def parse_sant_manukyan(soup):
    """Parse the HTML of Sant Manukyan's page."""
    news_items = soup.find('div', class_='col-12 col-lg mw0 author-article_list').find_all('div', class_='left-side')
    articles = []
    for news_item in news_items:
        title_tag = news_item.find('a')
        if title_tag:
            title = title_tag.text
            link = title_tag['href']
            articles.append((title, link))
    return articles


def fetch_news(source):
    """Fetch news from a specific source."""
    if source == "Reuters-Finance":
        url = "https://www.reuters.com/business/finance/"
        soup = get_soup(url)
        articles = parse_reuters(soup)
    elif source == "Nagehan-Alci":
        url = "https://www.haberturk.com/htyazar/nagehan-alci"
        soup = get_soup(url)
        articles = parse_nagehan_alci(soup)
    elif source == "Dilek-Gungor":
        url = "https://www.sabah.com.tr/yazarlar/dilek-gungor/arsiv?getall=true"
        soup = get_soup(url)
        articles = parse_dilek_gungor(soup)
    elif source == "Deniz-Zeyrek":
        url = "https://www.sozcu.com.tr/kategori/yazarlar/deniz-zeyrek/?utm_source=yazardetay&utm_medium=free" \
              "&utm_campaign=yazar_tumyazilar "
        soup = get_soup(url)
        articles = parse_deniz_zeyrek(soup)
    elif source == "Sant-Manukyan":
        url = "https://www.ekonomim.com/yazar/sant-manukyan/163"
        soup = get_soup(url)
        articles = parse_sant_manukyan(soup)
    elif source == "Bloomberg-Markets-Economics":  # Not used
        urls = ["https://www.bloomberg.com/markets", "https://www.bloomberg.com/economics"]
        articles_markets = []
        articles_economics = []
        for url in urls:
            soup = get_soup(url)
            if url.endswith("markets"):
                articles_markets = parse_bloomberg_markets(soup)
            elif url.endswith("economics"):
                articles_economics = parse_bloomberg_economics(soup)
        # Interleave the articles from the two sources
        articles = [article for pair in zip(articles_markets, articles_economics) for article in pair]

        # If one source has more articles than the other, append the remaining articles
        if len(articles_markets) > len(articles_economics):
            articles.extend(articles_markets[len(articles_economics):])
        elif len(articles_economics) > len(articles_markets):
            articles.extend(articles_economics[len(articles_markets):])

        # Remove duplicates while maintaining order
        articles = [article for i, article in enumerate(articles) if article not in articles[:i]]
    elif source == "Bloomberg-AI":  # Not used
        url = "https://www.bloomberg.com/ai"
        soup = get_soup(url)
        articles = parse_bloomberg_ai(soup)

    logging.debug(f"Fetched {len(articles)} articles from {source}.")
    return articles


def parse_bloomberg_markets(soup):  # Not used, Not included in prod. due to CAPTCHA issues
    """Parse the HTML of the Bloomberg Markets page."""
    articles = []
    print(soup)
    # Parse the big news item
    big_news_item = soup.find('div', attrs={'class': 'hover:underline focus:underline', 'data-component': 'headline'})
    if big_news_item:
        big_news_link = big_news_item.find('a')['href']
        big_news_title = big_news_item.text
        articles.append((big_news_title, big_news_link))

    # Parse the small news items
    small_news_items = soup.find_all('div', class_='styles_storyBlock__l5VzV')
    for news_item in small_news_items:
        title_tag = news_item.find('div',
                                   attrs={'class': 'hover:underline focus:underline', 'data-component': 'headline'})
        if title_tag:
            title = title_tag.text
            link = title_tag.find('a')['href']
            articles.append((title, link))

    return articles


def parse_bloomberg_economics(soup):
    """Parse the HTML of the Bloomberg Economics page."""
    articles = []

    # Parse the big news item
    big_news_item = soup.find('h1')
    if big_news_item:
        big_news_link_tag = soup.find('a', {'class': 'lede-text-v2__hed-link'})
        if big_news_link_tag:  # Check if the link tag is found
            big_news_link = big_news_link_tag['href']
            big_news_title = big_news_item.text
            articles.append((big_news_title, big_news_link))

    # Parse the small news items
    small_news_items = soup.find_all('div', class_='story-package-module__story__headline-link')
    for news_item in small_news_items:
        title_tag = news_item.find('a')
        if title_tag:
            title = title_tag.text
            link = title_tag['href']
            articles.append((title, link))

    return articles


def parse_bloomberg_ai(soup):
    """Parse the HTML of the Bloomberg AI page."""
    articles = []

    # Parse the big news item
    big_news_item = soup.find('section', class_='styles_SingleStoryCitylabVertical___9BKl')
    if big_news_item:
        big_news_link = big_news_item.find('a')['href']
        big_news_title = big_news_item.find('div', class_='hover:underline focus:underline').text
        articles.append((big_news_title, big_news_link))

    # Parse the small news items
    small_news_items = soup.find_all('div', class_='styles_storyBlock__l5VzV')
    for news_item in small_news_items:
        title_tag = news_item.find('div', class_='hover:underline focus:underline')
        if title_tag:
            title = title_tag.text
            link = title_tag.find('a')['href']
            articles.append((title, link))

    return articles