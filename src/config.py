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
Up_To_Date_NEWS_FILE = os.path.join(DESKTOP_DIR, 'Up_To_Date_NEWS.xlsx') if SAVE_ON_DESKTOP else os.path.join(DATA_DIR,
                                                                                                              'Up_To_Date_NEWS.xlsx')

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
    "Deniz-Zeyrek", "Dilek-Gungor", "Ugur-Gürses", "Fatih-Ozatay",
    "Haluk-Burumcekci", "Hande-Fırat", "Kerem-Alkin", "Mahfi-Egilmez",
    "Muharrem-Sarıkaya", "Murat-Yetkin", "Nagehan-Alci", "Okan-Muderrisoglu",
    "Kerim-Rota", "Sant-Manukyan", "Atilla-Yesilada", "Zeynep-Gurcanli",
    "Sedat-Ergin", "Levent-Yılmaz", "Erdal-Tanas-Karagol", "Merdan-Yanardag",
    "Ali-Rıza-Güngen", "Mehmet-Yılmaz"
]

# Color assignments for each source
COLORS = {
    "Daily-Updates": "FFD700",  # Gold
    "Abdulkadir-Selvi": "483D8B",  # Dark Slate Blue
    "Seref-Oguz": "6A5ACD",  # Slate Blue
    "Alaattin-Aktas": "7B68EE",  # Medium Slate Blue
    "Barıs-Soydan": "9370DB",  # Medium Purple
    "Deniz-Zeyrek": "BA55D3",  # Medium Orchid
    "Dilek-Gungor": "DA70D6",  # Orchid
    "Fatih-Ozatay": "EE82EE",  # Violet
    "Haluk-Burumcekci": "FF00FF",  # Magenta
    "Hande-Fırat": "FF1493",  # Deep Pink
    "Kerem-Alkin": "FF69B4",  # Hot Pink
    "Mahfi-Egilmez": "FFB6C1",  # Light Pink
    "Muharrem-Sarıkaya": "FFA07A",  # Light Salmon
    "Murat-Yetkin": "FA8072",  # Salmon
    "Nagehan-Alci": "E9967A",  # Dark Salmon
    "Okan-Muderrisoglu": "F08080",  # Light Coral
    "Ugur-Gürses": "CD5C5C",  # Indian Red
    "Kerim-Rota": "B22222",  # Firebrick
    "Sant-Manukyan": "A52A2A",  # Brown
    "Atilla-Yesilada": "8B4513",  # Saddle Brown
    "Zeynep-Gurcanli": "D2691E",  # Chocolate
    "Sedat-Ergin": "CD853F",  # Peru
    "Levent-Yılmaz": "DEB887",  # Burlywood
    "Erdal-Tanas-Karagol": "F4A460",  # Sandy Brown
    "Merdan-Yanardag": "D2B48C",  # Tan
    "Ali-Rıza-Güngen": "BC8F8F",  # Rosy Brown
    "Mehmet-Yılmaz": "A0522D",  # Sienna
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
    "Levent-Yılmaz": {
        "url": "https://www.yenisafak.com/yazarlar/levent-yilmaz",
        "parser": "parse_yenisafak",
    },
    "Erdal-Tanas-Karagol": {
        "url": "https://www.yenisafak.com/yazarlar/erdal-tanas-karagol",
        "parser": "parse_yenisafak",
    },
    "Merdan-Yanardag": {
        "url": "https://www.birgun.net/profil/merdan-yanardag-360",
        "parser": "parse_birgun",
    },
    "Ali-Rıza-Güngen": {
        "url": "https://www.gazeteduvar.com.tr/yazar/ali-riza-gungen",
        "parser": "parse_gazeteduvar",
    },
    "Mehmet-Yılmaz": {
        "url": "https://t24.com.tr/yazarlar/mehmet-y-yilmaz",
        "parser": "parse_t24",
    }
}

# Error handling for missing URLs or parsers
for source in SOURCES:
    if source not in SOURCE_MAP:
        raise ValueError(f"Missing URL or parser for source: {source}")
    if "url" not in SOURCE_MAP[source] or "parser" not in SOURCE_MAP[source]:
        raise ValueError(f"Missing URL or parser for source: {source}")