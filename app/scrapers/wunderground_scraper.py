import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException
from app.models.wunderground_model import WundergroundWeatherData, Temperature, Condition, AirQuality, AdditionalConditions, Astronomy
import logging

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5.0 / 9.0

class WundergroundScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def scrape(self, country_code: str, location: str):
        self.logger.info(f"Scraping weather data for {location}, {country_code}")
        url = f"https://www.wunderground.com/weather/{country_code}/{location}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch weather data for {location}, {country_code}. Status code: {response.status_code}")
            raise HTTPException(status_code=404, detail="Weather data not found")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return await self._parse_data(soup)

    async def _parse_data(self, soup):
        city_conditions = soup.find('div', class_='region-content-main')
        if not city_conditions:
            self.logger.error("Error finding weather data container")
            raise HTTPException(status_code=500, detail="Error finding weather data container")

        try:
            self.logger.debug("Parsing basic weather information")
            basic_info = self._parse_basic_info(soup, city_conditions)
            
            self.logger.debug("Parsing air quality information")
            air_quality = await self._parse_air_quality(soup)
            
            self.logger.debug("Parsing additional conditions")
            additional_conditions = self._parse_additional_conditions(soup)
            
            self.logger.debug("Parsing astronomy information")
            astronomy = self._parse_astronomy(soup)

            self.logger.info("Successfully parsed all weather data")
            return WundergroundWeatherData(
                location=basic_info['location'],
                temperature=basic_info['temperature'],
                feels_like=basic_info['feels_like'],
                condition=basic_info['condition'],
                forecast=basic_info['forecast'],
                pollen=air_quality['pollen'],
                air_quality=air_quality['air_quality'],
                additional_conditions=additional_conditions,
                astronomy=astronomy
            )
        except (AttributeError, ValueError) as e:
            self.logger.error(f"Error parsing weather data: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error parsing weather data: {str(e)}")

    def _parse_basic_info(self, soup, city_conditions):
        self.logger.debug("Parsing basic weather information")
        city_header_div = soup.find('div', class_='city-header')
        weather_conditions = city_header_div.find('h1').find('span').text
        location = ' '.join(weather_conditions.split()[:-2])

        temperature_f = int(city_conditions.find('span', class_='wu-value wu-value-to').text)
        feels_like_text = city_conditions.find('div', class_='feels-like').find('span', class_='temp').text
        feels_like_f = int(feels_like_text[:-1])

        condition_icon_div = city_conditions.find('div', class_='condition-icon')
        condition_icon = condition_icon_div.find('img')['src'] if condition_icon_div else None
        condition_description = condition_icon_div.find('p').text if condition_icon_div else "Unknown"

        forecast_text = city_conditions.find('p', class_='weather-quickie').text if city_conditions.find('p', class_='weather-quickie') else "No forecast available"

        self.logger.debug(f"Parsed basic info for location: {location}")
        return {
            'location': location,
            'temperature': Temperature(F=temperature_f, C=round(fahrenheit_to_celsius(temperature_f), 2)),
            'feels_like': Temperature(F=feels_like_f, C=round(fahrenheit_to_celsius(feels_like_f), 2)),
            'condition': Condition(icon=condition_icon, description=condition_description),
            'forecast': forecast_text
        }

    async def _parse_air_quality(self, soup):
        self.logger.debug("Parsing air quality information")
        forecast_sections = soup.find_all('div', class_='city-forecast')
        if len(forecast_sections) < 2:
            self.logger.warning("Forecast section not found")
            raise HTTPException(status_code=500, detail="Forecast section not found")

        forecast_section = forecast_sections[1]
        health_url = forecast_section.find('lib-air-quality-tile').find('a')['href']
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://www.wunderground.com{health_url}")

        if response.status_code != 200:
            self.logger.warning("Failed to fetch air quality data")
            return {"pollen": "No data", "air_quality": AirQuality(aqi_value="No data", aqi_type="No data", api_icon="No data", aqi_suggestion="No data", dominant_pollutant="No data", pollutant_desc="No data")}

        aq_soup = BeautifulSoup(response.text, 'html.parser')
        
        aqi_value = aq_soup.find('div', class_='aqi-value').text.strip() if aq_soup.find('div', class_='aqi-value') else "No data"
        aqi_type = aq_soup.find('div', class_='aqi-type').text.strip() if aq_soup.find('div', class_='aqi-type') else "No data"
        
        aqi_current_div = aq_soup.find("div", class_="aqi-current")
        img_tag = aqi_current_div.find('img', alt='icon') if aqi_current_div else None
        icon = img_tag['src'] if img_tag else "No data"
        
        data_div = aqi_current_div.find("div", class_="data") if aqi_current_div else None
        aqi_suggestion = data_div.find('p').text.strip() if data_div and data_div.find('p') else "No data"
        
        aqi_values = data_div.find_all('div', class_='aqi-value') if data_div else []
        dominant_pollutant = aqi_values[1].text.strip() if len(aqi_values) >= 2 else "No data"
        
        pollutant_desc = data_div.find('p', class_='pollutant-desc').text.strip() if data_div and data_div.find('p', class_='pollutant-desc') else "No data"
        
        pollen_data = aq_soup.find('div', class_='region-pollen')
        pollen = pollen_data.find('div', class_='status').text.strip() if pollen_data and pollen_data.find('div', class_='status') else "No data"

        self.logger.debug("Successfully parsed air quality information")
        return {
            "pollen": pollen,
            "air_quality": AirQuality(
                aqi_value=aqi_value,
                aqi_type=aqi_type,
                api_icon=icon,
                aqi_suggestion=aqi_suggestion,
                dominant_pollutant=dominant_pollutant,
                pollutant_desc=pollutant_desc
            )
        }

    def _parse_additional_conditions(self, soup):
        self.logger.debug("Parsing additional conditions")
        additional_conditions_div = soup.find('div', class_='data-module additional-conditions')
        if not additional_conditions_div:
            self.logger.warning("Additional conditions div not found")
            return AdditionalConditions(
                pressure={"value": "N/A", "unit": "N/A"},
                visibility={"value": "N/A", "unit": "N/A"},
                clouds="N/A",
                dew_point={"value": "N/A", "unit": "N/A"},
                humidity={"value": "N/A", "unit": "N/A"},
                rainfall={"value": "N/A", "unit": "N/A"},
                snow_depth={"value": "N/A", "unit": "N/A"}
            )

        rows = additional_conditions_div.find_all('div', class_='row')
        
        pressure = self._extract_value_unit(rows[0])
        visibility = self._extract_value_unit(rows[1])
        clouds = rows[2].find_all('div')[1].find('span', class_='wx-value').text
        dew_point = self._extract_value_unit(rows[3])
        humidity = self._extract_value_unit(rows[4])
        rainfall = self._extract_value_unit(rows[5])
        snow_depth = self._extract_value_unit(rows[6])

        self.logger.debug("Successfully parsed additional conditions")
        return AdditionalConditions(
            pressure=pressure,
            visibility=visibility,
            clouds=clouds,
            dew_point=dew_point,
            humidity=humidity,
            rainfall=rainfall,
            snow_depth=snow_depth
        )

    def _extract_value_unit(self, row):
        value = row.find_all('div')[1].find('span', class_='wu-value wu-value-to').text
        unit = row.find_all('div')[1].find('span', class_='wu-label').text.replace('°', '').strip()
        return {"value": value, "unit": unit}

    def _parse_astronomy(self, soup):
        self.logger.debug("Parsing astronomy information")
        astronomy_div = soup.find('div', class_='data-module city-astronomy')
        if not astronomy_div:
            self.logger.warning("Astronomy div not found")
            return Astronomy(
                sun={"sunrise": "N/A", "sunset": "N/A", "length_of_day": "N/A"},
                moon={"moonrise": "N/A", "moonset": "N/A", "moon_phase": "N/A", "moon_illumination": "N/A"}
            )

        sun_actual_time_row = astronomy_div.find_all('div', class_='row collapse')[1]
        sunrise_time = sun_actual_time_row.find_all('div', class_='columns small-3')[0].text.strip()
        sunset_time = sun_actual_time_row.find_all('div', class_='columns small-3')[1].text.strip()

        length_actual_time_row = astronomy_div.find_all('div', class_='row collapse ng-star-inserted')[0]
        length_of_day = length_actual_time_row.find_all('div', class_='columns small-6')[1].text.strip()

        moon_row = astronomy_div.find_all('div', class_='row collapse moon-rise-set')[0]
        moonrise_time = moon_row.find_all('div', class_='columns small-3')[0].find('span', class_='data-point').text.strip()
        moonset_time = moon_row.find_all('div', class_='columns small-3')[1].find('span', class_='data-point').text.strip()

        moon_phase_row = astronomy_div.find('div', class_='row collapse phase-today ng-star-inserted')
        moon_phase = moon_phase_row.find('div', class_='phase-name').text.strip()
        moon_illumination = moon_phase_row.find('span', class_='data-point').text.strip()

        self.logger.debug("Successfully parsed astronomy information")
        return Astronomy(
            sun={"sunrise": sunrise_time, "sunset": sunset_time, "length_of_day": length_of_day},
            moon={"moonrise": moonrise_time, "moonset": moonset_time, "moon_phase": moon_phase, "moon_illumination": moon_illumination}
        )