import re
import httpx
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlencode, parse_qsl, urljoin
from typing import Dict, List, Optional
from app.models.anime.mal_model import MalDataType1, MalResponseType1
from app.models.anime.mal_model import AnimeSeasonAndScheduleData, AnimeSeasonAndScheduleResponse
from app.models.anime.mal_model import AnimeSearchResponse, AnimeSearchResult
from app.models.anime.mal_model import PersonDetails, VoiceActingRole, AnimeStaffPosition
import logging

logger = logging.getLogger(__name__)

class AnimeMalScraper:
    mal_top_anime = "https://myanimelist.net/topanime.php"
    mal_top_airing = "https://myanimelist.net/topanime.php?type=airing"
    mal_top_upcoming = "https://myanimelist.net/topanime.php?type=upcoming"
    mal_top_tv_series = "https://myanimelist.net/topanime.php?type=tv"
    mal_top_movies = "https://myanimelist.net/topanime.php?type=movie"
    mal_top_ova = "https://myanimelist.net/topanime.php?type=ova"
    mal_top_ona = "https://myanimelist.net/topanime.php?type=ona"
    mal_top_special = "https://myanimelist.net/topanime.php?type=special"
    mal_most_popular = "https://myanimelist.net/topanime.php?type=bypopularity"
    mal_most_favorited = "https://myanimelist.net/topanime.php?type=favorite"

    async def scrape_top_anime(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping top anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_top_anime}?limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch top anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch top anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_top_airing(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping top airing anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_top_airing}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch top airing anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch top airing anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_top_upcoming(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping top upcoming anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_top_upcoming}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch top upcoming anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch top upcoming anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_top_tv_series(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping top TV series anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_top_tv_series}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch top TV series anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch top tv series anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_top_movies(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping top anime movies list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_top_movies}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch top anime movies list. Status code: {response.status_code}")
            raise Exception("Failed to fetch top tv movies anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_top_ova(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping top OVA anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_top_ova}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch top OVA anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch top OVAs anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_top_ona(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping top ONA anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_top_ona}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch top ONA anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch top ONAs anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_top_special(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping top special anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_top_special}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch top special anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch top special anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_most_popular(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping most popular anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_most_popular}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch most popular anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch most popular anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)
    
    async def scrape_most_favorited(self, page: int = 1, total_pages = 1):
        logger.info(f"Scraping most favorited anime list for page {page}")
        limit = (page - 1) * 50
        url = f"{self.mal_most_favorited}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch most favorited anime list. Status code: {response.status_code}")
            raise Exception("Failed to fetch most favorited anime list")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_data(soup, page, total_pages)

    # Main Data Scraper Type 1
    def _parse_anime_data(self, soup, page, total_pages):
        logger.debug("Parsing anime data from HTML")
        anime_list = []
        rows = soup.select('tr.ranking-list')

        for row in rows:
            rank = row.select_one('td.rank span').text.strip() if row.select_one('td.rank span').text else "N/A"
            title_element = row.select_one('td.title div.detail a.hoverinfo_trigger') if row.select_one('td.title div.detail a.hoverinfo_trigger') else "N/A"
            title = title_element.text.strip() if title_element.text else "N/A"
            url = title_element['href'] if title_element['href'] else "N/A"
            image_small_url = row.select_one('td.title img')['data-src'] if row.select_one('td.title img')['data-src'] else "N/A"
            image_url = self.transform_url(image_small_url) if image_small_url else None
            score = row.select_one('td.score span').text.strip() if row.select_one('td.score span').text else "N/A"

            anime_data = MalDataType1(
                rank=rank,
                title=title,
                url=url,
                image_small_url=image_small_url,
                image_url=image_url,
                score=score
            )
            anime_list.append(anime_data)

        logger.info(f"Successfully parsed {len(anime_list)} anime entries")
        return MalResponseType1(
            page=page,
            total_pages = total_pages,
            total_results_here=len(anime_list),
            results=anime_list
        )
    
    def transform_url(self, url):
        logger.debug(f"Transforming URL: {url}")
        start_index = url.find('r/')
        if start_index != -1:
            end_index = url.find('/', start_index + 2)
            if end_index != -1:
                url = url[:start_index] + url[end_index+1:]
        
        url_parts = url.split('?')
        transformed_url = url_parts[0]

        logger.debug(f"Transformed URL: {transformed_url}")
        return transformed_url
    

class AnimeMalSeasonAndScheduleScraper:
    anime_season = "https://myanimelist.net/anime/season"
    anime_schedule = "https://myanimelist.net/anime/season/schedule"

    async def scrape_anime_season(self, year: int = None, season: str = None):
        logger.info(f"Scraping anime season data for year: {year}, season: {season}")
        url = self.anime_season
        if year and season:
            url = f"{self.anime_season}/{year}/{season}"
        else:
            season, year = self.get_season_and_year()
            url = f"{self.anime_season}/{year}/{season}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch anime season data. Status code: {response.status_code}")
            raise Exception("Failed to fetch anime season data")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_season_data(soup, year, season, scrape_type="season")
    
    async def scrape_anime_schedule(self):
        logger.info("Scraping anime schedule data")
        url = self.anime_schedule
        season, year = self.get_season_and_year()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch anime schedule data. Status code: {response.status_code}")
            raise Exception("Failed to fetch anime season data")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_season_data(soup, year, season,  scrape_type="schedule")

    def _parse_anime_season_data(self, soup, year, season, scrape_type):
        logger.debug(f"Parsing anime {scrape_type} data")
        types = {}
        if (scrape_type=="season"):
            types = {
                'TV (New)': [], 'TV (Continuing)': [], 'ONA': [], 'OVA': [], 'Movie': [], 
                'Special': []
            }
        else:
            types = {
                'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 
                'Saturday': [], 'Sunday': [], 'Other': [], 'Unknown': []
            }

        seasonal_anime_lists = soup.select('div.seasonal-anime-list')

        for anime_list in seasonal_anime_lists:
            category = anime_list.select_one('div.anime-header')
            if category:
                category = category.text.strip()
            else:
                category = 'Unknown'

            anime_items = anime_list.select('div.seasonal-anime')
            for anime in anime_items:
                url = anime.select_one('a.link-title')['href'] if anime.select_one('a.link-title') else "N/A"
                title = anime.select_one('h2.h2_anime_title').text.strip() if anime.select_one('h2.h2_anime_title') else "N/A"
                
                image_element = anime.select_one('img')
                if image_element:
                    image_url = image_element.get('src') or image_element.get('data-src') or "N/A"
                else:
                    image_url = "N/A"

                score = anime.select_one('.score').text.strip() if anime.select_one('.score') else 'N/A'            
                genres = [genre.text for genre in anime.select('.genre a')]

                adult_genres = ["ecchi", "erotica", "hentai"]
                
                adult = any(genre.lower() in adult_genres for genre in genres)
                
                synopsis = anime.select_one('.preline').text.strip() if anime.select_one('.preline') else 'N/A'
                synopsis = self.clean_text(synopsis)

                anime_data = AnimeSeasonAndScheduleData(
                    url=url,
                    title=title,
                    image_url=image_url,
                    score=score,
                    adult=adult,
                    genres=genres,
                    synopsis=synopsis
                )

                if category in types:
                    types[category].append(anime_data)

        total_results = sum(len(animes) for animes in types.values())

        logger.info(f"Successfully parsed {total_results} anime entries for {scrape_type}")
        return AnimeSeasonAndScheduleResponse(
            total_results=total_results,
            year=year,
            season=season,
            results=types
        )
    
    def clean_text(self, text):
        logger.debug("Cleaning text")
        text = text.replace('\r', '').replace('\n', '')
        text = re.sub(r'\s*\[.*?\]$', '', text)
        return text

    def get_season_and_year(self):
        logger.debug("Getting current season and year")
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        
        if month in [1, 2, 3]:
            season = 'winter'
        elif month in [4, 5, 6]:
            season = 'spring'
        elif month in [7, 8, 9]:
            season = 'summer'
        elif month in [10, 11, 12]:
            season = 'fall'

        logger.debug(f"Current season: {season}, year: {year}")
        return season, year
    
class AnimeSearchScraper:
    search_url = "https://myanimelist.net/anime.php"

    type_mapping = {
        "tv": 1,
        "ova": 2,
        "movie": 3,
        "special": 4,
        "ona": 5,
        "music": 6
    }

    demographic_mapping = {
        "josei": 43,
        "kids": 15,
        "seinen": 42,
        "shoujo": 25,
        "shounen": 27
    }

    genre_mapping = {
        "action": 1,
        "adventure": 2,
        "avant garde": 5,  # Also known as Dementia
        "award winning": 46,
        "boys love": 28,   # Also known as Shounen Ai
        "comedy": 4,
        "drama": 8,
        "fantasy": 10,
        "girls love": 26,  # Also known as Shoujo Ai
        "gourmet": 47,
        "horror": 14,
        "mystery": 7,
        "romance": 22,
        "sci-fi": 24,
        "slice of life": 36,
        "sports": 30,
        "supernatural": 37,
        "suspense": 41,    # Also known as Thriller
        "ecchi": 9,
        "erotica": 49,
        "hentai": 12
    }

    explicit_genres = {"ecchi", "erotica", "hentai"}
    explicit_genre_ids = [9, 49, 12]

    async def search_anime(
        self, 
        q: str, 
        page: int = 1, 
        type: Optional[str] = None, 
        score: Optional[int] = None, 
        status: Optional[str] = None, 
        genre: Optional[List[str]] = None,
        demographic: Optional[List[str]] = None,
        adult: Optional[bool] = None, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None,
    ):    
        logger.info(f"Searching anime with query: '{q}', page: {page}")
        params = {
            'q': q,
            'cat': 'anime',
        }
        
        # Only add parameters if they are provided
        if type:
            type = type.lower()
            if type in self.type_mapping:
                params['type'] = self.type_mapping[type]
            else:
                logger.warning(f"Invalid type: {type}")
                raise ValueError(f"Invalid type: {type}. Valid types are: {', '.join(self.type_mapping.keys())}")
        if score:
            params['score'] = score
        if status:
            params['status'] = status
        if genre:
            genre_ids = []
            for g in genre:
                g_lower = g.lower()
                if g_lower in self.genre_mapping:
                    genre_id = self.genre_mapping[g_lower]
                    # Exclude explicit genres if adult is False
                    if not adult and g_lower in self.explicit_genres:
                        continue
                    genre_ids.append(genre_id)
                else:
                    logger.warning(f"Invalid genre: {g}")
                    raise ValueError(f"Invalid genre: {g}. Valid genres are: {', '.join(self.genre_mapping.keys())}")
            params['genre[]'] = genre_ids
        
        if start_date:
            try:
                date = datetime.datetime.strptime(start_date, '%d-%m-%Y')
                params['sd'] = date.day
                params['sm'] = date.month
                params['sy'] = date.year
            except ValueError:
                logger.warning(f"Invalid start_date format: {start_date}")
                raise ValueError("Invalid start_date format. Use DD-MM-YYYY.")

        if end_date:
            try:
                date = datetime.datetime.strptime(end_date, '%d-%m-%Y')
                params['ed'] = date.day
                params['em'] = date.month
                params['ey'] = date.year
            except ValueError:
                logger.warning(f"Invalid end_date format: {end_date}")
                raise ValueError("Invalid end_date format. Use DD-MM-YYYY.")

        if genre:
            genre_ids = []
            for g in genre:
                g_lower = g.lower()
                if g_lower in self.genre_mapping:
                    genre_id = self.genre_mapping[g_lower]
                    if not adult and g_lower in self.explicit_genres:
                        continue
                    genre_ids.append(genre_id)
                else:
                    logger.warning(f"Invalid genre: {g}")
                    raise ValueError(f"Invalid genre: {g}. Valid genres are: {', '.join(self.genre_mapping.keys())}")
            params['genre[]'] = genre_ids

        # Explicitly exclude explicit genres if adult is False
        if adult is False:
            params['genre_ex[]'] = self.explicit_genre_ids

        if demographic:
            demographic_lower = demographic.lower()
            if demographic_lower in self.demographic_mapping:
                params['genre[]'] = [self.demographic_mapping[demographic_lower]]
            else:
                logger.warning(f"Invalid demographic: {demographic}")
                raise ValueError(f"Invalid demographic: {demographic}. Valid demographics are: {', '.join(self.demographic_mapping.keys())}")

        # Add 'show' parameter last
        params['show'] = (page - 1) * 50
        
        # Construct URL ensuring 'show' is at the end
        url_params = urlencode(params, doseq=True)
        url_parts = parse_qsl(url_params)
        show_param = next(((k, v) for k, v in url_parts if k == 'show'), None)
        if show_param:
            url_parts.remove(show_param)
            url_parts.append(show_param)
        
        url = f"{self.search_url}?{urlencode(url_parts)}"
        
        logger.debug(f"Constructed search URL: {url}")
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch anime search results. Status code: {response.status_code}")
            raise Exception("Failed to fetch anime search results")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_search_results(soup, page)

    def _parse_search_results(self, soup, page):
        logger.debug("Parsing search results")
        anime_list = []
        total_pages = page  # Default to the current page
        # Select the rows within the specified div
        rows = soup.select('div.js-categories-seasonal table tr')

        # Filter the rows to include only those with the specified td elements
        filtered_rows = [row for row in rows if row.select('td.borderClass.bgColor0, td.borderClass.bgColor1')]
        
        for row in filtered_rows:
            image = row.select_one('td:nth-child(1) img')
            image_small = image['data-src'] if image else None
            get_clean_text = AnimeMalScraper()
            image_large = get_clean_text.transform_url(str(image_small) if str(image_small) else "")
            title_div = row.select_one('td:nth-child(2)')
            type_cell = row.select_one('td:nth-child(3)')
            eps_cell = row.select_one('td:nth-child(4)')
            score_cell = row.select_one('td:nth-child(5)')

            if not all([image, title_div, type_cell, eps_cell, score_cell]):
                continue

            title_link = title_div.select_one('a.hoverinfo_trigger')
            synopsis_div = title_div.select_one('div.pt4')

            anime_data = AnimeSearchResult(
                title=title_link.text.strip() if title_link else "Not Available",
                url=title_link['href'] if title_link else "Not Available",
                image_small=image_small,
                image_large=image_large,
                type=type_cell.text.strip() if type_cell else "Not Available",
                episodes=eps_cell.text.strip() if eps_cell else "Not Available",
                score=score_cell.text.strip() if score_cell else "No Rating",
                synopsis=synopsis_div.text.strip() if synopsis_div else "Not Available",
            )
            anime_list.append(anime_data)

            pagination = soup.select_one('.normal_header .fl-r.di-ib')
            if pagination:
                page_links = pagination.select('a')

                if page_links:  # Check if there are any pagination links
                    # Iterate through page links and find the maximum page number
                    for link in page_links:
                        link_text = link.text.strip()
                        if link_text.isdigit():  # Check if the link text is a number
                            total_pages = max(total_pages, int(link_text))  # Update total_pages if a higher number is found

                    # If the last link is not a number, check for a page count using text in square brackets
                    last_link_text = page_links[-1].text.strip()
                    if last_link_text.startswith('[') and last_link_text.endswith(']'):
                        # Extract the number from the last link text if it's in square brackets
                        try:
                            total_pages = max(total_pages, int(last_link_text[1:-1]))  # Remove brackets and convert to int
                        except ValueError:
                            pass  # If conversion fails, keep the previously set total_pages
            else:
                total_pages = page  # No pagination found, assume current page

        logger.info(f"Successfully parsed {len(anime_list)} search results")
        return AnimeSearchResponse(
            page=page,
            total_pages=total_pages,
            results=anime_list
        )
    
class AnimeDetailsScraper:
    base_url = "https://myanimelist.net"

    async def scrape_anime_details(self, anime_id: int):
        logger.info(f"Scraping anime details for ID: {anime_id}")
        url = f"{self.base_url}/anime/{anime_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch anime details for ID {anime_id}. Status code: {response.status_code}")
            raise Exception(f"Failed to fetch anime details for ID {anime_id}")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_anime_details(soup, anime_id)

    def _parse_anime_details(self, soup, anime_id):
        logger.debug(f"Parsing anime details for ID: {anime_id}")
        details = {}

        # Title
        title_elem = soup.select_one('h1.title-name strong')
        details['title'] = title_elem.text.strip() if title_elem else ''

        # English Title
        english_title = soup.select_one('p.title-english')
        details['english_title'] = english_title.text.strip() if english_title else ""

        # Information section
        info_block = soup.select_one('div[id="content"] table')
        if not info_block:
            logger.error("Could not find information block")
            raise Exception("Could not find information block")

        def get_info(selector, default='Unknown'):
            elem = info_block.select_one(selector)
            if elem:
                next_elem = elem.find_next()
                if next_elem and next_elem.name == 'a':
                    return next_elem.text.strip()
                return elem.next_sibling.strip() if elem.next_sibling else default
            return default

        details['type'] = get_info('span:-soup-contains("Type:")')
        details['episodes'] = get_info('span:-soup-contains("Episodes:")')
        details['status'] = get_info('span:-soup-contains("Status:")')
        details['aired'] = get_info('span:-soup-contains("Aired:")')
        details['premiered'] = get_info('span:-soup-contains("Premiered:")')
        details['broadcast'] = get_info('span:-soup-contains("Broadcast:")')
        details['source'] = get_info('span:-soup-contains("Source:")')
        details['duration'] = get_info('span:-soup-contains("Duration:")')
        details['rating'] = get_info('span:-soup-contains("Rating:")')

        def get_list_info(selector):
            return [item.text.strip() for item in info_block.select(f'{selector} ~ a')]

        # Extract producers
        producer_div = soup.select_one('div.spaceit_pad:has(> span.dark_text:-soup-contains("Producers:"))')
        if producer_div:
            details['producers'] = {}
            for producer_link in producer_div.select('a'):
                name = producer_link.text.strip()
                url = urljoin(self.base_url, producer_link['href'])
                details['producers'][name] = url

        # Extract studios
        studio_div = soup.select_one('div.spaceit_pad:has(> span.dark_text:-soup-contains("Studios:"))')
        if studio_div:
            details['studios'] = {}
            for studio_link in studio_div.select('a'):
                name = studio_link.text.strip()
                url = urljoin(self.base_url, studio_link['href'])
                details['studios'][name] = url

        details['licensors'] = get_list_info('span:-soup-contains("Licensors:")')
        details['genres'] = get_list_info('span:-soup-contains("Genres:")')
        details['themes'] = get_list_info('span:-soup-contains("Theme:")')
        details['demographics'] = get_list_info('span:-soup-contains("Demographic:")')

        # Score and stats
        score_elem = soup.select_one('div.score-label')
        details['score'] = score_elem.text.strip() if score_elem else ''

        ranked_elem = soup.select_one('span.ranked strong')
        details['ranked'] = ranked_elem.text.strip() if ranked_elem else ''

        popularity_elem = soup.select_one('span.popularity strong')
        details['popularity'] = popularity_elem.text.strip() if popularity_elem else ''

        # Synopsis
        synopsis_elem = soup.select_one('p[itemprop="description"]')
        details['synopsis'] = synopsis_elem.text.strip() if synopsis_elem else 'No synopsis available'

        # Related Entries
        details['related_entries'] = {}
        related_div = soup.select_one('div.related-entries')
        if related_div:
            # Process entries in the tile format
            for entry in related_div.select('div.entry'):
                relation_elem = entry.select_one('div.relation')
                title_elem = entry.select_one('div.title a')
                img_elem = entry.select_one('div.image a img')
                
                if relation_elem and title_elem:
                    relation = relation_elem.text.strip()
                    title = title_elem.text.strip()
                    url = urljoin(self.base_url, title_elem['href'])
                    entry_type = relation.split('(')[-1].rstrip(')') if '(' in relation else 'Unknown'
                    relation = relation.split('(')[0].strip()
                    
                    image_url = None
                    if img_elem:
                        image_url = img_elem.get('data-src') or img_elem.get('src')
                    
                    if relation not in details['related_entries']:
                        details['related_entries'][relation] = []
                    details['related_entries'][relation].append({
                        'title': title,
                        'url': url,
                        'type': entry_type,
                        'image_url': image_url
                    })

            # Process entries in the table format
            for table in related_div.select('table.entries-table'):
                for row in table.select('tr'):
                    relation_elem = row.select_one('td.ar.fw-n')
                    if relation_elem:
                        relation = relation_elem.text.strip().rstrip(':')
                        for li in row.select('ul.entries li'):
                            a_tag = li.select_one('a')
                            if a_tag:
                                title = a_tag.text.strip()
                                url = urljoin(self.base_url, a_tag['href'])
                                type_match = re.search(r'\((.*?)\)$', li.text)
                                entry_type = type_match.group(1) if type_match else 'Unknown'
                                
                                if relation not in details['related_entries']:
                                    details['related_entries'][relation] = []
                                details['related_entries'][relation].append({
                                    'title': title,
                                    'url': url,
                                    'type': entry_type,
                                    'image_url': "https://cdn.myanimelist.net/images/qm_50.gif"  # Default image URL for table entries
                                })

        # Characters & Voice Actors
        details['characters'] = []
        char_blocks = soup.select('div.detail-characters-list .left-column, div.detail-characters-list .left-right')
        for column in char_blocks:
            tables = column.select('table')
            for i in range(0, len(tables), 2):  # Process tables in pairs
                char_table = tables[i]
                va_table = tables[i+1] if i+1 < len(tables) else None

                char_img = char_table.select_one('td:first-child img')
                char_info = char_table.select_one('td:nth-child(2)')
                
                # Check if this is a character entry (has an h3 tag) and not a staff entry
                if char_info and char_img and char_info.select_one('h3'):
                    char = {
                        'name': char_info.select_one('h3 a').text.strip() if char_info.select_one('h3 a') else 'Unknown',
                        'url': urljoin(self.base_url, char_info.select_one('h3 a')['href']) if char_info.select_one('h3 a') else None,
                        'image_url': char_img['data-src'] if char_img.has_attr('data-src') else char_img['src'],
                        'role': char_info.select_one('div.spaceit_pad small').text.strip() if char_info.select_one('div.spaceit_pad small') else 'N/A',
                        'voice_actors': []
                    }
                    
                    if va_table:
                        va_info = va_table.select_one('tr')
                        if va_info:
                            va_name = va_info.select_one('td.va-t a')
                            va_img = va_info.select_one('td:last-child img')
                            va_lang = va_info.select_one('td.va-t small')
                            
                            if va_name and va_img:
                                va = {
                                    'name': va_name.text.strip(),
                                    'url': urljoin(self.base_url, va_name['href']),
                                    'image_url': va_img['data-src'] if va_img.has_attr('data-src') else va_img['src'],
                                    'language': va_lang.text.strip() if va_lang else 'N/A'
                                }
                                char['voice_actors'].append(va)
                    
                    details['characters'].append(char)

        # Opening and Ending Themes
        details['themes'] = {'opening': [], 'ending': []}
        theme_blocks = soup.select('div.theme-songs')
        for block in theme_blocks:
            theme_type = 'opening' if 'opnening' in block.get('class', []) else 'ending'
            for row in block.select('table tr'):
                # Skip rows that don't have the expected structure
                if not row.select_one('td:nth-of-type(2)'):
                    continue

                theme = {
                    'number': 'Unknown',
                    'title': 'Unknown',
                    'artist': 'Unknown',
                    'episodes': None,
                    'platforms': {}
                }
                
                # Extract all text from the main cell
                cell_text = row.select_one('td:nth-of-type(2)').text.strip()
                
                # Skip entries that don't look like theme songs
                if not ('"' in cell_text or 'by' in cell_text):
                    continue

                # Extract number
                index_elem = row.select_one('span.theme-song-index')
                if index_elem:
                    theme['number'] = index_elem.text.strip().rstrip(':')
                elif cell_text.startswith('S'):
                    theme['number'] = cell_text.split(':')[0].strip()
                
                # Try to extract title and artist
                title_artist_match = re.search(r'"(.+)"\s*(?:by\s+(.+?)(?:\s*\(|$))', cell_text)
                if title_artist_match:
                    theme['title'] = title_artist_match.group(1)
                    if title_artist_match.group(2):
                        theme['artist'] = title_artist_match.group(2).strip()
                else:
                    # If the standard format isn't found, try a different pattern
                    alt_match = re.search(r'(?::\s*)?(?:")?(.+?)(?:")?\s+by\s+(.+?)(?:\s*\(|$)', cell_text)
                    if alt_match:
                        theme['title'] = alt_match.group(1).strip('"')
                        theme['artist'] = alt_match.group(2).strip()
                    else:
                        # If still no match, use the whole text as title
                        theme['title'] = cell_text
                
                # Extract episodes
                episode_match = re.search(r'\((eps[^)]+)\)', cell_text)
                if episode_match:
                    theme['episodes'] = episode_match.group(1).lstrip('eps').strip()
                else:
                    # Try to match special episode format
                    special_match = re.search(r'\((.+?:\s*[\d-]+)\)', cell_text)
                    if special_match:
                        theme['episodes'] = special_match.group(1)
                
                # Extract platforms
                for platform in ['spotify', 'apple', 'amazon', 'youtube']:
                    input_elem = row.select_one(f'input[id^="{platform}_url_"]')
                    if input_elem and input_elem.get('value'):
                        theme['platforms'][platform] = input_elem['value']
                
                details['themes'][theme_type].append(theme)

        # Recommendations
        details['recommendations'] = []
        rec_blocks = soup.select('div #anime_recommendation div.anime-slide-outer ul.anime-slide li.btn-anime')
        if rec_blocks:
            for block in rec_blocks:
                try:
                    title = block.select_one('span.title')
                    title_text = title.text.strip() if title else 'N/A'

                    url = block.select_one('a')
                    url_href = url['href'] if url and 'href' in url.attrs else ''
                    full_url = urljoin(self.base_url, url_href)

                    img = block.select_one('img')
                    image_url = img['data-src'] if img and 'data-src' in img.attrs else ''
                    if not image_url and img and 'src' in img.attrs:
                        image_url = img['src']
                    image_url = image_url or 'https://via.placeholder.com/90x140'

                    users = block.select_one('span.users')
                    recommenders = users.text.strip().split()[0] if users else '0'

                    rec = {
                        'title': title_text,
                        'url': full_url,
                        'image_url': image_url,
                        'recommenders': recommenders
                    }
                    details['recommendations'].append(rec)
                except Exception as e:
                    logger.error(f"Error processing recommendation: {str(e)}", exc_info=True)
                    continue

        if not details['recommendations']:
            logger.warning("No recommendations found or error occurred while parsing")

        logger.info(f"Successfully parsed details for anime ID: {anime_id}")
        return details
    
# character details
    async def scrape_character_details(self, character_id: int) -> Dict:
        url = f"{self.base_url}/character/{character_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch character details for ID {character_id}. Status code: {response.status_code}")
            raise Exception(f"Failed to fetch character details for ID {character_id}")

        return self._parse_character_details(response.text)


    def _parse_character_details(self, html_content: str) -> Dict:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract character name
        name_elem = soup.select_one('h2', class_='normal_header')
        name = name_elem.text.strip() if name_elem else "Unknown"

        # Extract image URL
        image_elem = soup.select_one('img.portrait-225x350')
        image_url = image_elem['data-src'] if image_elem and 'data-src' in image_elem.attrs else None

        # Extract character details
        details = ""
        details_elem = soup.find('td', valign='top', style='padding-left: 5px;')

        if details_elem:
            # Find the h2 tag
            h2_tag = details_elem.find('h2', class_='normal_header')
            
            # Find the spoiler div
            spoiler_div = details_elem.find('div', class_='spoiler')
            
            # Find the voice actors section
            voice_actors_section = details_elem.find(text=re.compile(r'Voice Actors', re.IGNORECASE))

            if h2_tag:
                # Traverse all the next siblings until the spoiler div or voice actors section (whichever comes first)
                current = h2_tag
                while current and current != spoiler_div and current != voice_actors_section:
                    current = current.next_sibling
                    
                    # Check for strings and tag elements
                    if isinstance(current, str):
                        details += current.strip() + ' '
                    elif current and current.name:
                        details += current.get_text(separator=" ", strip=True) + ' '  # Extract text from tag elements

        # Clean up details
        details = re.sub(r'\s+', ' ', details).strip()
        details = re.sub(r' \n ', '\n', details)
        details = re.sub(r'\n+', '\n', details).strip()

        # Remove lines that contain source citations or unwanted patterns like (Source: ...)
        details = re.sub(r'\(Source:.*?\)', '', details)  # Remove anything inside parentheses with "Source:"
        details = re.sub(r'\s+', ' ', details).strip()  # Clean up extra spaces

        # Remove any voice actor information (e.g., lines starting with "Voice Actors" and followed by names)
        details = re.sub(r'Voice Actors.*', '', details, flags=re.DOTALL)

        # Remove any remaining navigation text or irrelevant lines
        details = re.sub(r'^(Details|Clubs|Pictures|Top|Characters).*?\n', '', details, flags=re.MULTILINE).strip()

        # Extract spoiler
        spoiler_elem = soup.select_one('div.spoiler span.spoiler_content')
        spoiler = spoiler_elem.text.strip() if spoiler_elem else ""

        # Extract voice actors
        voice_actors = []
        voice_actor_tables = soup.select('div.normal_header:-soup-contains("Voice Actors") ~ table')
        #print(voice_actor_tables)

        for table in voice_actor_tables:
            name_elem = table.select_one('td.borderClass:nth-of-type(2) a')
            lang_elem = table.select_one('td.borderClass:nth-of-type(2) small')
            img_elem = table.select_one('td.borderClass img')

            if name_elem and lang_elem:
                voice_actor = {
                    "name": name_elem.text,
                    "language": lang_elem.text.strip(),
                    "url": urljoin(self.base_url, name_elem['href']) if name_elem.has_attr('href') else "",
                    "image_url": img_elem['data-src'] if img_elem and img_elem.has_attr('data-src') else ""
                }
                voice_actors.append(voice_actor)

        return {
            "name": name,
            "image_url": image_url,
            "details": details,
            "spoiler": spoiler,
            "voice_actors": voice_actors
        }
    
# People details
    async def scrape_person_details(self, person_id: int):
        logger.info(f"Scraping person details for ID: {person_id}")
        url = f"{self.base_url}/people/{person_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch person details for ID {person_id}. Status code: {response.status_code}")
            raise Exception(f"Failed to fetch person details for ID {person_id}")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_person_details(soup, person_id)

    def _parse_person_details(self, soup, person_id):
        details = {}

        # Name
        name_elem = soup.select_one('h1.title-name strong')
        details['name'] = name_elem.text.strip() if name_elem else ''

        # Image URL
        image_elem = soup.select_one('div[style*="text-align: center;"] img')
        details['image_url'] = image_elem['data-src'] if image_elem and 'data-src' in image_elem.attrs else None

        # Helper function to extract information
        def extract_info(label):
            elem = soup.select_one(f'.spaceit_pad:-soup-contains("{label}:")')
            if elem:
                return elem.contents[-1].strip()
            return None

        # Extract various details
        details['given_name'] = extract_info("Given name")

        family_name_elem = soup.select_one('span.dark_text:-soup-contains("Family name:")')
        details['family_name'] = family_name_elem.next_sibling.strip() if family_name_elem else None

        details['alternate_names'] = extract_info("Alternate names")
        if details['alternate_names']:
            details['alternate_names'] = [name.strip() for name in details['alternate_names'].split(',')]
        else:
            details['alternate_names'] = []
        details['birthday'] = extract_info("Birthday")

        # About information
        about_elem = soup.select_one('.people-informantion-more')
        if about_elem:
            details['about'] = self._parse_about_info(about_elem.text)
        else:
            details['about'] = {}

        # Voice Acting Roles
        details['voice_acting_roles'] = self._parse_voice_acting_roles(soup)

        # Anime Staff Positions
        details['anime_staff_positions'] = self._parse_anime_staff_positions(soup)

        return PersonDetails(**details)

    def _parse_voice_acting_roles(self, soup):
        roles = []
        role_table = soup.select_one('table.js-table-people-character')
        if role_table:
            for row in role_table.select('tr'):
                anime_elem = row.select_one('td:nth-child(2) a.js-people-title')
                anime_image = row.select_one('td:nth-child(1) img')
                character_elem = row.select_one('td:nth-child(3) a')
                character_image = row.select_one('td:nth-child(4) img')
                role_elem = row.select_one('td:nth-child(3) div:nth-child(2)')
                
                if anime_elem and character_elem:
                    role = VoiceActingRole(
                        anime_name=anime_elem.text.strip(),
                        anime_url=self.base_url + anime_elem['href'] if anime_elem.has_attr('href') else None,
                        anime_image=anime_image['data-src'] if anime_image and anime_image.has_attr('data-src') else None,
                        character_name=character_elem.text.strip(),
                        character_url=self.base_url + character_elem['href'] if character_elem.has_attr('href') else None,
                        character_image=character_image['data-src'] if character_image and character_image.has_attr('data-src') else None,
                        role=role_elem.text.strip() if role_elem else 'Unknown'
                    )
                    roles.append(role)
        return roles

    def _parse_anime_staff_positions(self, soup):
        positions = []
        staff_table = soup.select_one('table.js-table-people-staff')
        if staff_table:
            for row in staff_table.select('tr'):
                anime_elem = row.select_one('td:nth-child(2) a.js-people-title')
                position_elem = row.select_one('td:nth-child(2) small')
                anime_image = row.select_one('td:nth-child(1) img')
                
                if anime_elem and position_elem:
                    position = AnimeStaffPosition(
                        anime=anime_elem.text.strip(),
                        anime_url=self.base_url + anime_elem['href'] if anime_elem.has_attr('href') else None,
                        anime_image=anime_image['data-src'] if anime_image and anime_image.has_attr('data-src') else None,
                        position=position_elem.text.strip()
                    )
                    positions.append(position)
        return positions
    
    def _parse_about_info(self, text):
        about_info = {
            'personal_info': {},
            'background': [],
            'awards': [],
            'profile': [],
            'social_media': {}
        }
        
        lines = text.strip().split('\n')
        current_section = 'personal_info'
        
        for line in lines:
            line = line.strip()
            if not line or '(Source:' in line:
                continue
            
            if line.startswith('Awards:'):
                current_section = 'awards'
            elif line.startswith('Profile:'):
                current_section = 'profile'
            elif line.startswith('Twitter:'):
                current_section = 'social_media'
            elif ':' in line and current_section == 'personal_info':
                key, value = line.split(':', 1)
                about_info['personal_info'][key.strip()] = value.strip()
            elif line.startswith('- ') and current_section == 'awards':
                about_info['awards'].append(line[2:])
            elif current_section == 'profile':
                about_info['profile'].extend(line.split(', '))
            elif current_section == 'social_media':
                if line.startswith('@'):
                    key, value = line.split(' ', 1)
                    about_info['social_media'][key] = value.strip('()')
                elif ':' in line:
                    key, value = line.split(':', 1)
                    about_info['social_media'][key.strip()] = value.strip()
            else:
                about_info['background'].append(line)
        
        return about_info


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')