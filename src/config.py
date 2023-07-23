# config.py
import os
from utils import DATA_DIR

"""
Configuration for the Excel file save location:

This script provides two options for saving the Excel file: on your desktop or in the 'data' directory of the project.

- DESKTOP_DIR: This is the path to your desktop. It's determined automatically based on your operating system.

- SAVE_ON_DESKTOP: This is a boolean variable. If it's set to True, the Excel file will be saved on your desktop. If 
it's set to False, the file will be saved in the 'data' directory of the project. 

- Up_To_Date_NEWS_FILE: This is the path where the Excel file will be saved. It's determined based on the value of 
SAVE_ON_DESKTOP. 

To change the save location, simply change the value of SAVE_ON_DESKTOP and run the script again.
"""

# Path to your desktop
DESKTOP_DIR = os.path.join(os.path.expanduser("~"), "Desktop")

# Boolean variable to choose the save location: True for desktop, False for data directory
SAVE_ON_DESKTOP = True

# Path to the Excel file
Up_To_Date_NEWS_FILE = os.path.join(DESKTOP_DIR, 'Up_To_Date_NEWS.xlsx') if SAVE_ON_DESKTOP else os.path.join(DATA_DIR, 'Up_To_Date_NEWS.xlsx')


"""
Configuration for Automated-News-Collector Sources:

This file contains three main structures that are used throughout the Automated-News-Collector project: SOURCES, 
COLORS, and SOURCE_MAP. 

1. SOURCES: A list of strings representing the names of the news sources. Each source name must be unique.

2. COLORS: A dictionary mapping each source name to a color code. The color code must be a string representing a 
valid hex color. 

3. SOURCE_MAP: A dictionary mapping each source name to a URL and a parser function. The URL is a string representing 
the URL of the news source's author page. The parser function is a string representing the name of the parser 
function to be used for this news source. 

When adding a new source, make sure to: [!!!!!!!!!! ATTENTION !!!!!!!!!!!]

- Add the source name to the SOURCES list.
- Add a color code for the source to the COLORS dictionary. [hexadecimal] (Default = Black, If not defined)
- Add a URL and a parser function for the source to the SOURCE_MAP dictionary.

The parser function must be defined in the 'news_fetcher.py' file and its name must be included in the 'parsers' 
dictionary in the same file. 

Please ensure that all entries are correctly formatted and that all source names are consistent across the three 
structures.
"""

# List of sources to scrape
SOURCES = [
    "Abdulkadir-Selvi", "Seref-Oguz", "Alaattin-Aktas", "Barıs-Soydan",
    "Deniz-Zeyrek", "Dilek-Gungor", "Fatih-Ozatay", "Haluk-Burumcekci",
    "Hande-Fırat", "Kerem-Alkin", "Mahfi-Egilmez", "Muharrem-Sarıkaya",
    "Murat-Yetkin", "Nagehan-Alci", "Okan-Muderrisoglu", "Ugur-Gürses",
    "Kerim-Rota", "Sant-Manukyan", "Atilla-Yesilada", "Zeynep-Gurcanli",
    "Sedat-Ergin"
]

# Color assignments for each source
COLORS = {
    "Daily-Updates": "FFD700",  # Special visually appealing color (Gold)
    "Abdulkadir-Selvi": "D2B48C",  # Tan (Cream/Beige)
    "Seref-Oguz": "F0E68C",  # Khaki
    "Alaattin-Aktas": "CD853F",  # Peru
    "Barıs-Soydan": "BC8F8F",  # Rosy Brown
    "Deniz-Zeyrek": "FFA07A",  # Light Salmon
    "Dilek-Gungor": "90EE90",  # Light Green
    "Fatih-Ozatay": "00CED1",  # Dark Turquoise
    "Haluk-Burumcekci": "FF8C00",  # Dark Orange
    "Hande-Fırat": "1E90FF",  # Dodger Blue
    "Kerem-Alkin": "9370DB",  # Medium Purple
    "Mahfi-Egilmez": "BA55D3",  # Medium Orchid
    "Muharrem-Sarıkaya": "FF69B4",  # Hot Pink
    "Murat-Yetkin": "FF4500",  # Orange Red
    "Nagehan-Alci": "FFDAB9",  # Peach Puff
    "Okan-Muderrisoglu": "EEE8AA",  # Pale Goldenrod
    "Ugur-Gürses": "BDB76B",  # Dark Khaki
    "Kerim-Rota": "6B8E23",  # Olive Drab
    "Sant-Manukyan": "8FBC8F",  # Dark Sea Green
    "Atilla-Yesilada": "20B2AA",  # Light Sea Green
    "Zeynep-Gurcanli": "87CEFA",  # Light Sky Blue
    "Sedat-Ergin": "8470FF",  # Light Slate Blue
}

# Dictionary mapping sources to their URLs and parser functions
SOURCE_MAP = {
    "Abdulkadir-Selvi": {
        "url": "https://www.hurriyet.com.tr/yazarlar/abdulkadir-selvi/",
        "parser": "parse_hurriyet",
    },
    "Seref-Oguz": {
        "url": "https://www.ekonomim.com/yazar/seref-oguz/1093",
        "parser": "parse_ekonomim",
    },
    "Alaattin-Aktas": {
        "url": "https://www.ekonomim.com/yazar/alaattin-aktas/30",
        "parser": "parse_ekonomim",
    },
    "Barıs-Soydan": {
        "url": "https://10haber.net/yazarlar/baris-soydan/",
        "parser": "parse_10haber",
    },
    "Deniz-Zeyrek": {
        "url": "https://www.sozcu.com.tr/kategori/yazarlar/deniz-zeyrek/?utm_source=yazardetay&utm_medium=free"
               "&utm_campaign=yazar_tumyazilar",
        "parser": "parse_sozcu",
    },
    "Dilek-Gungor": {
        "url": "https://www.sabah.com.tr/yazarlar/dilek-gungor/arsiv?getall=true",
        "parser": "parse_sabah",
    },
    "Fatih-Ozatay": {
        "url": "https://www.ekonomim.com/yazar/fatih-ozatay/85",
        "parser": "parse_ekonomim",
    },
    "Haluk-Burumcekci": {
        "url": "https://gazeteoksijen.com/yazarlar/haluk-burumcekci",
        "parser": "parse_gazeteoksijen",
    },
    "Hande-Fırat": {
        "url": "https://www.hurriyet.com.tr/yazarlar/hande-firat/",
        "parser": "parse_hurriyet",
    },
    "Kerem-Alkin": {
        "url": "https://www.sabah.com.tr/yazarlar/kerem-alkin/arsiv?getall=true",
        "parser": "parse_sabah",
    },
    "Mahfi-Egilmez": {
        "url": "https://www.mahfiegilmez.com/",
        "parser": "parse_mahfiegilmez",
    },
    "Muharrem-Sarıkaya": {
        "url": "https://www.haberturk.com/ozel-icerikler/muharrem-sarikaya",
        "parser": "parse_haberturk",
    },
    "Murat-Yetkin": {
        "url": "https://yetkinreport.com/author/muratmyetkin/",
        "parser": "parse_yetkinreport",
    },
    "Nagehan-Alci": {
        "url": "https://www.haberturk.com/ozel-icerikler/nagehan-alci",
        "parser": "parse_haberturk",
    },
    "Okan-Muderrisoglu": {
        "url": "https://www.sabah.com.tr/yazarlar/muderrisoglu/arsiv?getall=true",
        "parser": "parse_sabah",
    },
    "Ugur-Gürses": {
        "url": "https://ugurses.net/",
        "parser": "parse_ugurses",
    },
    "Kerim-Rota": {
        "url": "https://www.perspektif.online/author/kerim-rota/",
        "parser": "parse_perspektif",
    },
    "Sant-Manukyan": {
        "url": "https://www.ekonomim.com/yazar/sant-manukyan/163",
        "parser": "parse_ekonomim",
    },
    "Atilla-Yesilada": {
        "url": "https://www.paraanaliz.com/yazarlar/atilla-yesilada/",
        "parser": "parse_paraanaliz",
    },
    "Zeynep-Gurcanli": {
        "url": "https://www.ekonomim.com/yazar/zeynep-gurcanli/1125",
        "parser": "parse_ekonomim",
    },
    "Sedat-Ergin": {
        "url": "https://www.hurriyet.com.tr/yazarlar/sedat-ergin/",
        "parser": "parse_hurriyet",
    },
}

# Error handling for missing URLs or parsers
for source in SOURCES:
    if source not in SOURCE_MAP:
        raise ValueError(f"Missing URL or parser for source: {source}")
    if "url" not in SOURCE_MAP[source] or "parser" not in SOURCE_MAP[source]:
        raise ValueError(f"Missing URL or parser for source: {source}")