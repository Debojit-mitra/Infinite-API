import re
import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException
from app.models.timeanddate_model import TimeAndDateWeatherData, Temperature, Condition, AdditionalConditions, FiveHourForecast, AstronomyData, SunMoonData

class TimeAndDateScraper:
    async def scrape(self, country: str, location: str):
        url = f"https://www.timeanddate.com/weather/{country}/{location}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Weather data not found")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_data = self._parse_data(soup)

        # Scrape astronomy data
        astronomy_data = await self.scrape_astronomy(country, location)

        # Combine weather and astronomy data
        weather_data.astronomy = astronomy_data
        return weather_data

    def _parse_data(self, soup):
        try:
            current_weather = soup.find('section', class_='bk-focus')
            if not current_weather:
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
                visibility = pressure = humidity = dew_point = 'N/A'

            forecast_table = soup.find('table', id='wt-5hr')
            forecast_data = self._parse_5hour_forecast(forecast_table) if forecast_table else []

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
            raise HTTPException(status_code=500, detail=f"Error parsing weather data: {str(e)}")
        
    async def scrape_astronomy(self, country: str, location: str):
        url = f"https://www.timeanddate.com/astronomy/{country}/{location}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Astronomy data not found")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_astronomy_data(soup)

    def _parse_astronomy_data(self, soup):
        moon_percent = soup.find('span', id='cur-moon-percent').text.strip()
        moon_title = soup.find('div', class_='bk-focus__qlook').find('a').text.strip()
        sunrise = self._safe_extract(soup, 'tr', contains='Sunrise Today:').split(': ')[1]
        sunset = self._safe_extract(soup, 'tr', contains='Sunset Today:').split(': ')[1]
        moonrise = self._safe_extract(soup, 'tr', contains='Moonrise Today:').split(': ')[1]
        moonset = self._safe_extract(soup, 'tr', contains='Moonset Today:').split(': ')[1]
        daylight_hours = self._safe_extract(soup, 'tr', contains='Daylight Hours:').split(': ')[1]

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

    def _extract_location(self, soup):
        header_section = soup.find('div', class_='headline-banner__content')
        if header_section:
            title = header_section.find('h1', class_='headline-banner__title')
            if title:
                location_text = title.text.strip()
                # Remove "Weather in " from the title
                return location_text.replace("Weather in ", "").strip()
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

                # Check if it's a temperature value with °C
                if "°C" in value_unit:
                    celsius_value = int(value.replace('°C', '').strip())
                    return {
                        "C": f"{celsius_value}",
                        "F": f"{self._celsius_to_fahrenheit(celsius_value)}"
                    }

                # For pressure and visibility, return value with unit
                return {
                    "value": ' '.join(value_unit)  # Combine value and unit
                }

        return {"value": "N/A"}  # Adjusted for consistency

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

        # Extract numeric value and ignore extra characters
        match = re.search(r'(\d+)\s*°C', selected.text)
        if match:
            return float(match.group(1))
        return None

    def _parse_forecast(self, forecast_text):
        if forecast_text:
            try:
                # Extract the numbers from the forecast text
                high_low = re.findall(r'(\d+)', forecast_text)
                if len(high_low) == 2:
                    high, low = map(float, high_low)
                    return high, low
            except ValueError:
                pass
        return None, None

    def _parse_5hour_forecast(self, forecast_table):
        forecast_data = []
        if forecast_table:
            headers = forecast_table.find_all('tr')[0].find_all('td')
            temps = forecast_table.find_all('tr')[2].find_all('td')
            descriptions = forecast_table.find_all('tr')[1].find_all('td')
            
            for header, temp, desc in zip(headers, temps, descriptions):
                time = header.text.strip()
                # Clean the temperature string
                temperature_value = temp.text.strip().replace('\xa0', '').replace('°C', '')
                celsius_value = float(temperature_value)  # Convert cleaned string to float
                
                forecast_data.append({
                    "time": time,
                    "temperature": f"{celsius_value} °C / {self._celsius_to_fahrenheit(celsius_value)} °F",  # Format as string
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
