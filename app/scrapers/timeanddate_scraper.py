import re
import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException
import logging
from datetime import datetime
from app.models.timeanddate_model import TimeAndDateWeatherData, Temperature, Condition, AdditionalConditions, AstronomyData, SunMoonData
from app.models.timeanddate_model import FourteenDayForecast, DailyForecast, TwentyFourHourForecast, HourlyForecast

class TimeAndDateScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

    async def scrape(self, country: str, location: str):
        self.logger.info(f"Scraping weather data for {location}, {country}")
        url = f"https://www.timeanddate.com/weather/{country}/{location}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch weather data for {location}, {country}. Status code: {response.status_code}")
            raise HTTPException(status_code=404, detail="Weather data not found")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_data = self._parse_data(soup)

        self.logger.info(f"Scraping astronomy data for {location}, {country}")
        astronomy_data = await self.scrape_astronomy(country, location)

        weather_data.astronomy = astronomy_data
        self.logger.info(f"Successfully scraped weather and astronomy data for {location}, {country}")
        return weather_data

    def _parse_data(self, soup):
        try:
            self.logger.debug("Parsing weather data from HTML")
            current_weather = soup.find('section', class_='bk-focus')
            if not current_weather:
                self.logger.error("Current weather section not found in HTML")
                raise ValueError("Current weather section not found")

            location = self._extract_location(soup)
            current_temp = self._safe_extract_float(current_weather, 'div.h2')

            condition_elem = current_weather.find('p')
            condition = condition_elem.text.strip() if condition_elem else 'N/A'
            condition_icon = self._extract_icon(current_weather)

            feels_like = self._extract_temperature(self._safe_extract(current_weather, 'p', contains='Feels Like:'))
            
            forecast_span = current_weather.find('span', title=lambda x: x and 'High and low forecasted temperature today' in x)
            if forecast_span:
                forecast_high, forecast_low = self._parse_forecast(forecast_span.text)
            else:
                forecast_high, forecast_low = None, None
            
            wind = self._extract_wind(current_weather)
            
            additional_info = current_weather.find('div', class_='bk-focus__info')
            if additional_info:
                visibility = self._safe_extract(additional_info, 'tr', contains='Visibility:')
                pressure = self._safe_extract(additional_info, 'tr', contains='Pressure:')
                humidity = self._safe_extract(additional_info, 'tr', contains='Humidity:')
                dew_point = self._safe_extract(additional_info, 'tr', contains='Dew Point:')
            else:
                self.logger.warning("Additional weather information not found")
                visibility = pressure = humidity = dew_point = 'N/A'

            forecast_table = soup.find('table', id='wt-5hr')
            forecast_data = self._parse_5hour_forecast(forecast_table) if forecast_table else []

            self.logger.debug("Successfully parsed weather data")
            return TimeAndDateWeatherData(
                location=location or 'Unknown',
                temperature=Temperature(
                    C=current_temp,
                    F=self._celsius_to_fahrenheit(current_temp)
                ),
                feels_like=Temperature(
                    C=feels_like,
                    F=self._celsius_to_fahrenheit(feels_like)
                ),
                condition=Condition(description=condition, icon=condition_icon),
                forecast=f"High: {forecast_high}°C, Low: {forecast_low}°C" if forecast_high and forecast_low else 'N/A',
                additional_conditions=AdditionalConditions(
                    pressure=self._parse_value_unit(pressure),
                    visibility=self._parse_value_unit(visibility),
                    humidity=self._parse_value_unit(humidity),
                    dew_point=self._parse_value_unit(dew_point),
                    wind=wind
                ),
                fiveHourForecast=forecast_data
            )
        except Exception as e:
            self.logger.error(f"Error parsing weather data: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error parsing weather data: {str(e)}")

    async def scrape_astronomy(self, country: str, location: str):
        self.logger.info(f"Scraping astronomy data for {location}, {country}")
        url = f"https://www.timeanddate.com/astronomy/{country}/{location}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch astronomy data for {location}, {country}. Status code: {response.status_code}")
            raise HTTPException(status_code=404, detail="Astronomy data not found")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_astronomy_data(soup)

    def _parse_astronomy_data(self, soup):
        self.logger.debug("Parsing astronomy data from HTML")
        try:
            moon_percent = soup.find('span', id='cur-moon-percent').text.strip()
            moon_title = soup.find('div', class_='bk-focus__qlook').find('a').text.strip()
            sunrise = self._safe_extract(soup, 'tr', contains='Sunrise Today:').split(': ')[1]
            sunset = self._safe_extract(soup, 'tr', contains='Sunset Today:').split(': ')[1]
            moonrise = self._safe_extract(soup, 'tr', contains='Moonrise Today:').split(': ')[1]
            moonset = self._safe_extract(soup, 'tr', contains='Moonset Today:').split(': ')[1]
            daylight_hours = self._safe_extract(soup, 'tr', contains='Daylight Hours:').split(': ')[1]

            self.logger.debug("Successfully parsed astronomy data")
            return AstronomyData(
                sun_moon=SunMoonData(
                    moon_percent=moon_percent,
                    moon_title=moon_title,
                    sunrise=sunrise,
                    sunset=sunset,
                    moonrise=moonrise,
                    moonset=moonset,
                    daylight_hours=daylight_hours
                )
            )
        except Exception as e:
            self.logger.error(f"Error parsing astronomy data: {str(e)}", exc_info=True)
            raise ValueError(f"Error parsing astronomy data: {str(e)}")

    def _extract_location(self, soup):
        header_section = soup.find('div', class_='headline-banner__content')
        if header_section:
            title = header_section.find('h1', class_='headline-banner__title')
            if title:
                location_text = title.text.strip()
                return location_text.replace("Weather in ", "").strip()
        self.logger.warning("Could not extract location from HTML")
        return "Unknown Location"

    def _extract_icon(self, soup):
        img = soup.find('img', id='cur-weather')
        return img['src'] if img else None

    def _extract_wind(self, soup):
        wind_text = self._safe_extract(soup, 'p', contains='Wind:')
        if wind_text:
            wind_parts = wind_text.split('Wind:')
            if len(wind_parts) > 1:
                return wind_parts[1].strip()
        return 'N/A'

    def _parse_value_unit(self, text):
        if text and text != 'N/A':
            parts = text.split(':')
            if len(parts) > 1:
                value_unit = parts[1].strip().split()
                value = value_unit[0].strip()

                if "°C" in value_unit:
                    celsius_value = int(value.replace('°C', '').strip())
                    return {
                        "C": f"{celsius_value}",
                        "F": f"{self._celsius_to_fahrenheit(celsius_value)}"
                    }

                return {
                    "value": ' '.join(value_unit)
                }

        return {"value": "N/A"}

    def _safe_extract(self, soup, selector, contains=None, split_char=None):
        element = soup.select_one(selector)
        if contains:
            element = soup.find(lambda tag: tag.name == selector.split()[0] and contains in tag.text) if soup else None
        if element:
            text = element.text.strip()
            return text.split(split_char)[1].strip() if split_char else text
        return None

    def _safe_extract_float(self, element, selector):
        selected = element.select_one(selector)
        if not selected:
            return None

        match = re.search(r'(\d+)\s*°C', selected.text)
        if match:
            return float(match.group(1))
        return None

    def _parse_forecast(self, forecast_text):
        if forecast_text:
            try:
                high_low = re.findall(r'(\d+)', forecast_text)
                if len(high_low) == 2:
                    high, low = map(float, high_low)
                    return high, low
            except ValueError:
                self.logger.warning(f"Could not parse forecast text: {forecast_text}")
        return None, None

    def _parse_5hour_forecast(self, forecast_table):
        forecast_data = []
        if forecast_table:
            headers = forecast_table.find_all('tr')[0].find_all('td')
            temps = forecast_table.find_all('tr')[2].find_all('td')
            descriptions = forecast_table.find_all('tr')[1].find_all('td')
            
            for header, temp, desc in zip(headers, temps, descriptions):
                time = header.text.strip()
                temperature_value = temp.text.strip().replace('\xa0', '').replace('°C', '')
                celsius_value = float(temperature_value)
                
                forecast_data.append({
                    "time": time,
                    "temperature": f"{celsius_value} °C / {self._celsius_to_fahrenheit(celsius_value)} °F",
                    "description": desc.find('img')['title'] if desc.find('img')['title'] else 'N/A',
                    "icon": desc.find('img')['src'] if desc.find('img') else None
                })
        return forecast_data

    def _celsius_to_fahrenheit(self, celsius):
        return round((celsius * 9/5) + 32, 1) if celsius is not None else None

    def _extract_temperature(self, text):
        if text:
            match = re.search(r'(\d+)\s*°C', text)
            if match:
                return float(match.group(1))
        return None

    async def scrape_14_day_forecast(self, country: str, location: str):
        self.logger.info(f"Scraping 14-day forecast for {location}, {country}")
        url = f"https://www.timeanddate.com/weather/{country}/{location}/ext"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch 14-day forecast for {location}, {country}. Status code: {response.status_code}")
            raise HTTPException(status_code=404, detail="14-day forecast data not found")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_14_day_forecast(soup, location)

    def _parse_14_day_forecast(self, soup, location):
        self.logger.debug(f"Parsing 14-day forecast for {location}")
        forecast_table = soup.find('table', id='wt-ext')
        if not forecast_table:
            self.logger.error("14-day forecast table not found in HTML")
            raise ValueError("14-day forecast table not found")

        rows = forecast_table.find_all('tr')
        forecast_data = []

        for row in rows[2:]:  # Skip header rows
            cells = row.find_all(['th', 'td'])
            if len(cells) < 13:
                continue

            try:
                date_cell = cells[0].text.strip()
            
                day_date_match = re.match(r'([A-Za-z]+)(\d{1,2}\s+[A-Za-z]+)', date_cell)
                
                if day_date_match:
                    day = day_date_match.group(1)
                    date = day_date_match.group(2)
                else:
                    day = "N/A"
                    date = "N/A"

                try:
                    parsed_date = datetime.strptime(date, "%d %b")
                    date = parsed_date.strftime("%d %b")
                except ValueError:
                    self.logger.warning(f"Could not parse date: {date}")

                temp = cells[2].text.strip().split('/')
                temp_high = int(temp[0].strip().replace('°C', '')) if len(temp) > 0 else None
                temp_low = int(temp[1].strip().replace('°C', '')) if len(temp) > 1 else None

                condition_icon = cells[1].find('img')['src'] if cells[1].find('img') else None
                condition = cells[3].text.strip() if len(cells) > 3 else "N/A"
                feels_like = self._safe_extract_int(cells[4].text.strip(), '°C') if len(cells) > 4 else None
                wind_speed = cells[5].text.strip() if len(cells) > 5 else "N/A"
                wind_direction = cells[6].find('span')['title'] if len(cells) > 6 and cells[6].find('span') else "N/A"
                humidity = cells[7].text.strip() if len(cells) > 7 else "N/A"
                precip_chance = cells[8].text.strip() if len(cells) > 8 else "N/A"
                precip_amount = cells[9].text.strip() if len(cells) > 9 else "N/A"
                uv_index = cells[10].text.strip() if len(cells) > 10 else "N/A"
                sunrise = cells[11].text.strip() if len(cells) > 11 else "N/A"
                sunset = cells[12].text.strip() if len(cells) > 12 else "N/A"

                forecast_data.append(DailyForecast(
                    date=date,
                    day=day,
                    temperature_high=temp_high,
                    temperature_low=temp_low,
                    condition=condition,
                    condition_icon=condition_icon,
                    feels_like=feels_like,
                    wind_speed=wind_speed,
                    wind_direction=wind_direction,
                    humidity=humidity,
                    precipitation_chance=precip_chance,
                    precipitation_amount=precip_amount,
                    uv_index=uv_index,
                    sunrise=sunrise,
                    sunset=sunset
                ))
            except Exception as e:
                self.logger.warning(f"Error parsing row in 14-day forecast: {str(e)}", exc_info=True)
                continue

        if not forecast_data:
            self.logger.error("No forecast data could be parsed from 14-day forecast")
            raise ValueError("No forecast data could be parsed")

        self.logger.info(f"Successfully parsed 14-day forecast for {location}")
        return FourteenDayForecast(location=location, forecast=forecast_data)

    def _safe_extract_int(self, text, remove_char=''):
        try:
            return int(text.replace(remove_char, '').strip())
        except ValueError:
            self.logger.warning(f"Could not parse integer from text: {text}")
            return None

    async def scrape_24hour_forecast(self, country: str, location: str):
        self.logger.info(f"Scraping 24-hour forecast for {location}, {country}")
        url = f"https://www.timeanddate.com/weather/{country}/{location}/hourly"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch 24-hour forecast for {location}, {country}. Status code: {response.status_code}")
            raise HTTPException(status_code=404, detail="24-hour forecast data not found")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_24hour_forecast(soup, location)

    def _parse_24hour_forecast(self, soup, location):
        self.logger.debug(f"Parsing 24-hour forecast for {location}")
        forecast_table = soup.find('table', id='wt-hbh')
        if not forecast_table:
            self.logger.error("24-hour forecast table not found in HTML")
            raise ValueError("24-hour forecast table not found")

        rows = forecast_table.find('tbody').find_all('tr')
        forecast_data = []
        current_date = ""

        for row in rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) < 10:
                continue

            try:
                time_cell = cells[0]
                time = time_cell.contents[0].strip()
                
                date_span = time_cell.find('span', class_='smaller soft')
                if date_span:
                    current_date = date_span.text.strip()
                
                temperature = self._safe_extract_int(cells[2].text, '°C')
                condition = cells[3].text.strip()
                condition_icon = cells[1].find('img')['src'] if cells[1].find('img') else None
                feels_like = self._safe_extract_int(cells[4].text, '°C')
                wind_speed = cells[5].text.strip()
                wind_direction = cells[6].find('span')['title'] if cells[6].find('span') else "N/A"
                humidity = cells[7].text.strip()
                precip_chance = cells[8].text.strip()
                precip_amount = cells[9].text.strip()

                forecast_data.append(HourlyForecast(
                    time=time,
                    date=current_date,
                    temperature=temperature,
                    condition=condition,
                    condition_icon=condition_icon,
                    feels_like=feels_like,
                    wind_speed=wind_speed,
                    wind_direction=wind_direction,
                    humidity=humidity,
                    precipitation_chance=precip_chance,
                    precipitation_amount=precip_amount
                ))
            except Exception as e:
                self.logger.warning(f"Error parsing row in 24-hour forecast: {str(e)}", exc_info=True)
                continue

        if not forecast_data:
            self.logger.error("No forecast data could be parsed from 24-hour forecast")
            raise ValueError("No forecast data could be parsed")

        self.logger.info(f"Successfully parsed 24-hour forecast for {location}")
        return TwentyFourHourForecast(location=location, forecast=forecast_data)