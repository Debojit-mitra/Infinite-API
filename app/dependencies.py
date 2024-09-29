from app.scrapers.wunderground_scraper import WundergroundScraper
from app.scrapers.timeanddate_scraper import TimeAndDateScraper
from app.scrapers.libgen_scraper import LibgenDownloadScraper
from app.scrapers.gsmarena_scraper import GSMArenaScraper, GSMArenaPhoneInfoScraper
from app.scrapers.hero_scraper import HeroScraper
from app.scrapers.anime.mal_scraper import AnimeMalScraper, AnimeMalSeasonAndScheduleScraper, AnimeSearchScraper, AnimeDetailsScraper


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

def get_anime_scraper():
    return AnimeMalScraper()

def get_anime_season_and_schedule_scraper():
    return AnimeMalSeasonAndScheduleScraper()

def get_anime_search_scraper():
    return AnimeSearchScraper()

def get_anime_details_scraper():
    return AnimeDetailsScraper()