import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException
from app.models.gsmarena_model import GSMArenaPhoneData, GSMArenaSearchResponse, PhoneDetailsResponse


class GSMArenaScraper:
    def __init__(self):
        self.proxy_base_url = "https://webproxy.lumiproxy.com/request?area=US&u="

    async def fetch(self, url):
        proxied_url = f"{self.proxy_base_url}{url}"
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(proxied_url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching data")
            return response

    async def fetch_Normal(self, url):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching data")
            return response

    async def scrape(self, search_query: str):
        url = f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={search_query}"
        response = await self.fetch_Normal(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_data(soup)
    
    async def scrapeTopSeventy(self):
        url = f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName="
        response = await self.fetch(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_data(soup)

    def _parse_data(self, soup):
        try:
            results_list = soup.find('div', class_='makers').find('ul')
            if not results_list:
                raise ValueError("Results list not found")

            phone_data_list = []
            items = results_list.find_all('li')

            for item in items:
                link = item.find('a')
                img = link.find('img')
                name = link.find('strong').find('span')

                phone_data = GSMArenaPhoneData(
                    name=name.get_text(separator=" ", strip=True),
                    image_url=img['src'],
                    phone_url=f"https://www.gsmarena.com/{link['href']}"
                )
                phone_data_list.append(phone_data)

            total_results = len(phone_data_list)
            return GSMArenaSearchResponse(total_results=total_results, phones=phone_data_list)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing phone data: {str(e)}")


class GSMArenaPhoneInfoScraper:
    def __init__(self):
        self.proxy_base_url = "https://webproxy.lumiproxy.com/request?area=US&u="

    async def fetch(self, id):
        proxied_url = f"{self.proxy_base_url}https://www.gsmarena.com/{id}"
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(proxied_url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching data")
            return response

    async def scrape_phone_details(self, id: str):
        response = await self.fetch(id)
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_phone_details(soup, id)

    def _parse_phone_details(self, soup, id):
        try:
            specifications = {}

            # Extract the photo URL
            photo_div = soup.find('div', class_='specs-photo-main')
            if photo_div:
                img_tag = photo_div.find('img')
                photo_url = img_tag['src'] if img_tag else None
            else:
                photo_url = None

            spec_div = soup.find('div', id='specs-list')
            spec_tables = spec_div.find_all('table')

            for table in spec_tables:
                rows = table.find_all('tr')
                if rows:
                    # The first row usually contains the category
                    category_name = rows[0].find('th').get_text(strip=True)
                    specs = {}
                    for row in rows[1:]:
                        spec_name = row.find('td', class_='ttl')
                        spec_value = row.find('td', class_='nfo')

                        if spec_name and spec_value:
                            specs[spec_name.get_text(strip=True)] = spec_value.get_text(strip=True)

                    specifications[category_name] = specs

            return PhoneDetailsResponse(id=id, photo_url=photo_url, specifications=specifications)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing phone details: {str(e)}")
