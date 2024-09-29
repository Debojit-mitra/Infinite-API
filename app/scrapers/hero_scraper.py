import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException
from pydantic import BaseModel
from app.models.hero_model import HeroData, HeroSearchResponse, HeroDetail, HeroSearchResult
from typing import List
import logging

class HeroScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def scrape(self, start: str):
        self.logger.info(f"Scraping heroes starting with '{start}'")
        url = f"https://hero.fandom.com/wiki/Category:Superheroes?from={start}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            self.logger.error(f"Failed to fetch hero data. Status code: {response.status_code}")
            raise HTTPException(status_code=404, detail="Hero data not found")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_data(soup)

    def _parse_data(self, soup):
        try:
            self.logger.debug("Parsing hero data from HTML")
            hero_data_list = []
            members_div = soup.find("div", class_="category-page__members")
            if members_div:
                hero_items = members_div.find_all("li", class_="category-page__member")
                for hero_item in hero_items:
                    name_tag = hero_item.find("a", class_="category-page__member-link")
                    image_tag = hero_item.find("img", class_="category-page__member-thumbnail")
                    
                    if name_tag:
                        hero_data = HeroData(
                            hero_id=name_tag.get('href').split("/")[-1],
                            name=name_tag.get('title', ''),
                            image_url=image_tag.get('src', '') if image_tag else ''
                        )
                        hero_data_list.append(hero_data)

            self.logger.info(f"Successfully parsed {len(hero_data_list)} hero entries")
            return HeroSearchResponse(
                total_results=len(hero_data_list),
                results=[HeroSearchResult(
                    name=hero.name,
                    hero_id=hero.hero_id,
                    thumbnail=hero.image_url,
                    description=''
                ) for hero in hero_data_list]
            )
        except Exception as e:
            self.logger.error(f"Error parsing hero data: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error parsing hero data: {str(e)}")
        
    async def scrape_hero_detail(self, hero_id: str):
        self.logger.info(f"Scraping details for hero with ID: {hero_id}")
        url = f"https://hero.fandom.com/wiki/{hero_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            self.logger.error(f"Failed to fetch hero details for ID {hero_id}. Status code: {response.status_code}")
            raise HTTPException(status_code=404, detail="Hero details not found")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_hero_detail(soup, hero_id)

    def _parse_hero_detail(self, soup, hero_id):
        try:
            self.logger.debug(f"Parsing hero details for ID: {hero_id}")
            name = soup.find('h1', class_='page-header__title').text.strip()
            
            image_tag = soup.find('figure', class_='pi-item pi-image')
            image_url = image_tag.find('img')['src'] if image_tag else ''
            
            details = {}
            aside = soup.find('div', class_='mw-parser-output')
            if aside:
                for item in aside.find_all('div', class_='pi-item pi-data pi-item-spacing pi-border-color'):
                    label = item.find('h3', class_='pi-data-label')
                    value = item.find('div', class_='pi-data-value')
                    if label and value:
                        key = label.text.strip()
                        for tag in value.find_all(True):
                            if tag.name == 'br':
                                tag.replace_with(', ')
                            else:
                                tag.unwrap()
                        val = value.decode_contents()
                        details[key] = val

            biography = ""
            bio_section = aside.find('div', id='toc')
            if bio_section:
                bio_content = bio_section.find_next_siblings()
                content_dict = {}
                current_header = None

                for tag in bio_content:
                    if tag.name in ['h2', 'h3', 'h4']:
                        current_header = tag.text.strip()
                        content_dict[current_header] = []
                    elif tag.name == 'p' and current_header:
                        content_dict[current_header].append(tag.text.strip())
                    elif tag.name == 'ul' and current_header:
                        list_items = tag.find_all('li')
                        for item in list_items:
                            content_dict[current_header].append(item.text.strip())
                    elif tag.name == 'table' and current_header:
                        table_text = []
                        for tr in tag.find_all('tr'):
                            row_text = ' '.join(td.get_text(strip=True) for td in tr.find_all('td'))
                            table_text.append(row_text)
                        content_dict[current_header].append('\n'.join(table_text))

                formatted_biography = []
                for header, content in content_dict.items():
                    formatted_biography.append(header + ":")
                    for paragraph in content:
                        formatted_biography.append(f"  - {paragraph}")
                    formatted_biography.append("\n")

                biography = '\n'.join(formatted_biography).strip()

            gallery = []
            gallery_div = soup.find('div', class_='wikia-gallery')
            if gallery_div:
                for item in gallery_div.find_all('div', class_='wikia-gallery-item')[:5]:
                    img = item.find('img')
                    if img:
                        gallery.append({
                            'url': img['src'],
                            'caption': img.get('alt', '')
                        })

            self.logger.info(f"Successfully parsed details for hero: {name}")
            return HeroDetail(
                hero_id=hero_id,
                name=name,
                image_url=image_url,
                details=details,
                biography=biography,
                gallery=gallery
            )
        except Exception as e:
            self.logger.error(f"Error parsing hero detail for ID {hero_id}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error parsing hero detail: {str(e)}")
        
    async def search_heroes(self, query: str) -> HeroSearchResponse:
        self.logger.info(f"Searching heroes with query: '{query}'")
        url = f"https://hero.fandom.com/wiki/Special:Search?query={query}&scope=internal&navigationSearch=true"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            self.logger.error(f"Hero search failed for query '{query}'. Status code: {response.status_code}")
            raise HTTPException(status_code=404, detail="Hero search failed")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_search_results(soup)

    def _parse_search_results(self, soup: BeautifulSoup) -> HeroSearchResponse:
        self.logger.debug("Parsing hero search results")
        results = []
        for item in soup.select('.unified-search__result'):
            name = item.select_one('.unified-search__result__title').text.strip()
            hero_id = item.select_one('.unified-search__result__title')['href']
            hero_id = hero_id.split("/")[-1]
            thumbnail = item.select_one('.unified-search__result__title')['data-thumbnail']
            description = item.select_one('.unified-search__result__content').text.strip()
            
            results.append(HeroSearchResult(
                name=name,
                hero_id=hero_id,
                thumbnail=thumbnail,
                description=description
            ))
        
        total_results = len(results)
        self.logger.info(f"Found {total_results} heroes in search results")
        
        return HeroSearchResponse(total_results=total_results, results=results)