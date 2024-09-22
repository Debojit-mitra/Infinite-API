import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException
from app.models.libgen_model import LibgenBookData, LibgenSearchResponse

class LibgenScraper:
    async def scrape(self, bookname: str):
        url = f"https://libgen.is/search.php?req={bookname}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Book data not found")

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_data(soup)

    def _parse_data(self, soup):
        try:
            results_table = soup.find('table', class_='c')
            if not results_table:
                raise ValueError("Results table not found")

            book_data_list = []
            rows = results_table.find_all('tr')[1:]  # Start from the second row (index 1)

            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 11:  # Ensure there are enough columns (including two mirror links)
                    continue

                book_data = LibgenBookData(
                    id=cols[0].text.strip(),
                    author=cols[1].text.strip(),
                    title=cols[2].find('a').text.strip() if cols[2].find('a') else cols[2].text.strip(),
                    publisher=cols[3].text.strip(),
                    year=cols[4].text.strip(),
                    pages=cols[5].text.strip(),
                    language=cols[6].text.strip(),
                    size=cols[7].text.strip(),
                    extension=cols[8].text.strip(),
                    download_id=cols[9].find('a')['href'].split('/')[-1] if cols[9].find('a') else None
                )
                book_data_list.append(book_data)

            # Get total results count
            total_results = len(book_data_list)

            # Try to find the pagination info for a more accurate total count
            pagination = soup.find('div', style='float:left')
            if pagination:
                pagination_text = pagination.text.strip()
                if 'of' in pagination_text:
                    total_results = int(pagination_text.split('of')[-1].strip())

            return LibgenSearchResponse(total_results=total_results, books=book_data_list)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing book data: {str(e)}")



class LibgenDownloadScraper:
    async def get_library_lol_link(self, download_id: str):
        url = f"http://library.lol/main/{download_id}"
        return await self._scrape_library_lol(url)

    async def get_libgen_li_link(self, download_id: str):
        url = f"http://libgen.li/ads.php?md5={download_id}"
        return await self._scrape_libgen_li(url)

    async def _scrape_library_lol(self, url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Download page not found")

        soup = BeautifulSoup(response.text, 'html.parser')
        download_button = soup.find('div', id='download').find('h2').find('a')

        if download_button and 'href' in download_button.attrs:
            return download_button['href']
        else:
            raise HTTPException(status_code=500, detail="Download link not found on library.lol")

    async def _scrape_libgen_li(self, url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Download page not found")

        soup = BeautifulSoup(response.text, 'html.parser')
        download_button = soup.find('td', bgcolor="#A9F5BC").find('a')

        if download_button and 'href' in download_button.attrs:
            return f"http://libgen.li/{download_button['href']}"
        else:
            raise HTTPException(status_code=500, detail="Download link not found on libgen.li")
