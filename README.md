<h1 align="center">Automated News Collector</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg">
  <img src="https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg">
</p>

<p align="center">
The Automated-News-Collector is a Python-based project designed to scrape news articles from various sources and compile them into an Excel file. The project is highly customizable, allowing you to add or remove news sources, change the color coding for each source, and specify the save location for the Excel file.
</p>

![Automated-News-Collector](./docs/Daily-Updates-Image.png)
![Automated-News-Collector](./docs/Author-News-Image.png)
![Automated-News-Collector](./docs/Sheets-Ordering-Image.png)

## Table of Contents
1. [Workflow Overview](#workflow-overview)
2. [Configuration](#configuration)
   - [Excel File Save Location](#excel-file-save-location)
   - [News Sources](#news-sources)
3. [Adding New Sources](#adding-new-sources)
4. [Error Handling](#error-handling)
5. [Running the Project](#running-the-project)
6. [Contributing](#contributing)
7. [License](#license)
8. [Disclaimer](#disclaimer)

## Workflow Overview

The Automated-News-Collector project is a comprehensive and robust system designed to automate the process of collecting news articles from various sources. It uses a combination of web scraping techniques, data management, and scheduling to provide a seamless and efficient way to stay updated with the latest news. Here's an overview of the workflow:

### 1. Web Scraping and Fetching News

The project utilizes Python libraries like `requests` and `BeautifulSoup` to scrape and parse the HTML content of various news websites. Specific parser functions are defined for each news source, extracting relevant information such as article titles, links, and publication dates. These parser functions are customized to handle the unique structure of each news source's webpage, ensuring accurate and efficient data extraction.

### 2. Excel Data Management

Excel files are used for data storage and tracking. The main Excel file, `Up_To_Date_NEWS_FILE`, stores historical news articles from various sources. Each source is tracked separately in the Excel file, with each article's title, link, and publication date recorded for future reference. Past articles are also saved in a dictionary for quick access and to prevent duplication.

### 3. Daily Updates

The script is designed to run hourly, checking for new articles from each news source. At the start of each new day, a separate sheet labeled 'Daily-Updates-[DATE]' is created in the Excel file. This sheet is used to store new articles published on that day, providing a daily snapshot of the news landscape.

### 4. Fetching and Processing Articles

For each news source, the script fetches the current articles and processes them to identify new articles not previously recorded. New articles are saved to the Excel file and marked as processed to avoid duplicates. This ensures that the Excel file is always up-to-date with the latest articles, and that each day's news is accurately captured.

## Configuration

The configuration for the Automated-News-Collector is primarily done in the `config.py` file. This file contains several important variables and structures that control the behavior of the project.

### Excel File Save Location

The `config.py` file allows you to choose where the Excel file will be saved. You can choose to save the file on your desktop or in the 'data' directory of the project. To change the save location, modify the `SAVE_ON_DESKTOP` variable in the `config.py` file. Set it to `True` to save on the desktop, or `False` to save in the 'data' directory.

### News Sources

The `config.py` file also contains the configurations for the news sources. There are three main structures:

1. `SOURCES`: A list of strings representing the names of the news sources. Each source name must be unique.

2. `COLORS`: A dictionary mapping each source name to a color code. The color code must be a string representing a valid hex color.

3. `SOURCE_MAP`: A dictionary mapping each source name to a URL and a parser function. The URL is a string representing the URL of the news source's author page. The parser function is a string representing the name of the parser function to be used for this news source.

## Adding New Sources

When adding a new source, make sure to:

- Add the source name to the `SOURCES` list.
- Add a color code for the source to the `COLORS` dictionary. The color code must be a valid hexadecimal color code.
- Add a URL and a parser function for the source to the `SOURCE_MAP` dictionary.

The parser function must be defined in the `news_fetcher.py` file and its name must be included in the `parsers` dictionary in the same file.

## Error Handling

The `config.py` file contains error handling for missing URLs or parsers. If a source is missing a URL or parser, the script will raise a `ValueError`.

## Running the Project

To run the project, simply navigate to the project directory in your terminal and run the `main.py` file with Python.

## Contributing

As the sole creator of the Automated-News-Collector, I welcome any contributions to improve this project. If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for the full license text.

## Disclaimer

This project is intended for educational and research purposes only. It is not intended for commercial use. The project scrapes publicly available data from various news websites, and the data remains the intellectual property of the original authors. If you choose to use this project, please respect the rights of the original authors. 

This project is not endorsed by, directly affiliated with, maintained, or sponsored by any of the news websites from which it scrapes data. All product and company names are the registered trademarks of their original owners. The use of any trade name or trademark is for identification and reference purposes only and does not imply any association with the trademark holder or their product brand.

Please use this project responsibly and ethically. If you plan to use it for purposes other than education or research, please seek permission from the original authors or the websites hosting the content.
