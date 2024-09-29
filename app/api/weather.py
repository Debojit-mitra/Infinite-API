import logging
from fastapi import APIRouter, HTTPException, Depends, Path
from app.models.wunderground_model import WundergroundWeatherData
from app.models.timeanddate_model import TimeAndDateWeatherData, FourteenDayForecast, TwentyFourHourForecast
from app.models.errorResponse_model import ErrorResponse
from app.dependencies import get_wunderground_scraper, get_timeanddate_scraper

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/wunderground/{country}/{location}", response_model=WundergroundWeatherData, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_wunderground_weather(
    country: str = Path(..., min_length=2, max_length=50),
    location: str = Path(..., min_length=2, max_length=50),
    scraper = Depends(get_wunderground_scraper)
):
    """Fetch weather data from Wunderground for a specific location."""
    logger.info(f"Fetching Wunderground weather data for {country}/{location}")
    try:
        weather_data = await scraper.scrape(country, location)
        logger.info(f"Successfully fetched Wunderground weather data for {country}/{location}")
        return weather_data
    except Exception as e:
        logger.error(f"Error fetching Wunderground weather data for {country}/{location}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timeanddate/{country}/{location}", response_model=TimeAndDateWeatherData, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_timeanddate_weather(
    country: str = Path(..., min_length=2, max_length=50),
    location: str = Path(..., min_length=2, max_length=50),
    scraper = Depends(get_timeanddate_scraper)
):
    """Fetch weather data from TimeAndDate for a specific location."""
    logger.info(f"Fetching TimeAndDate weather data for {country}/{location}")
    try:
        weather_data = await scraper.scrape(country, location)
        logger.info(f"Successfully fetched TimeAndDate weather data for {country}/{location}")
        return weather_data
    except Exception as e:
        logger.error(f"Error fetching TimeAndDate weather data for {country}/{location}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{source}/{country}/{location}", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_weather(
    source: str = Path(..., pattern="^(wunderground|timeanddate)$"),
    country: str = Path(..., min_length=2, max_length=50),
    location: str = Path(..., min_length=2, max_length=50)
):
    """Fetch weather data from a specified source for a specific location."""
    logger.info(f"Fetching weather data from {source} for {country}/{location}")
    try:
        if source == "wunderground":
            return await get_wunderground_weather(country, location)
        elif source == "timeanddate":
            return await get_timeanddate_weather(country, location)
    except HTTPException as e:
        logger.error(f"HTTP exception occurred while fetching weather data from {source} for {country}/{location}: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error fetching weather data from {source} for {country}/{location}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timeanddate/{country}/{location}/14day", response_model=FourteenDayForecast, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_timeanddate_14day_forecast(
    country: str = Path(..., min_length=2, max_length=50),
    location: str = Path(..., min_length=2, max_length=50),
    scraper = Depends(get_timeanddate_scraper)
):
    """Fetch 14-day weather forecast from TimeAndDate for a specific location."""
    logger.info(f"Fetching TimeAndDate 14-day forecast for {country}/{location}")
    try:
        forecast_data = await scraper.scrape_14_day_forecast(country, location)
        logger.info(f"Successfully fetched TimeAndDate 14-day forecast for {country}/{location}")
        return forecast_data
    except Exception as e:
        logger.error(f"Error fetching TimeAndDate 14-day forecast for {country}/{location}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timeanddate/{country}/{location}/24hour", response_model=TwentyFourHourForecast, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_timeanddate_24hour_forecast(
    country: str = Path(..., min_length=2, max_length=50),
    location: str = Path(..., min_length=2, max_length=50),
    scraper = Depends(get_timeanddate_scraper)
):
    """Fetch 24-hour weather forecast from TimeAndDate for a specific location."""
    logger.info(f"Fetching TimeAndDate 24-hour forecast for {country}/{location}")
    try:
        forecast_data = await scraper.scrape_24hour_forecast(country, location)
        logger.info(f"Successfully fetched TimeAndDate 24-hour forecast for {country}/{location}")
        return forecast_data
    except Exception as e:
        logger.error(f"Error fetching TimeAndDate 24-hour forecast for {country}/{location}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))