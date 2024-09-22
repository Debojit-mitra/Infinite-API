from app.scrapers.wunderground_scraper import WundergroundScraper
from app.scrapers.timeanddate_scraper import TimeAndDateScraper
from app.scrapers.libgen_scraper import LibgenDownloadScraper
from app.scrapers.gsmarena_scraper import GSMArenaScraper, GSMArenaPhoneInfoScraper
from app.scrapers.hero_scraper import HeroScraper

def get_wunderground_scraper():
    return WundergroundScraper()

def get_timeanddate_scraper():
    return TimeAndDateScraper()

def get_libgen_download_scraper():
    return LibgenDownloadScraper()

def get_gsmarena_scraper():
    return GSMArenaScraper()

def get_gsmarena_phone_info_scraper():
    return GSMArenaPhoneInfoScraper()

def get_heroes_scraper():
    return HeroScraper()