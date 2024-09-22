import logging
from fastapi import APIRouter, HTTPException, Depends, Path
from app.models.wunderground_model import WundergroundWeatherData
from app.models.timeanddate_model import TimeAndDateWeatherData
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
    try:
        weather_data = await scraper.scrape(country, location)
        return weather_data
    except Exception as e:
        logger.error(f"Error fetching Wunderground weather data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timeanddate/{country}/{location}", response_model=TimeAndDateWeatherData, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_timeanddate_weather(
    country: str = Path(..., min_length=2, max_length=50),
    location: str = Path(..., min_length=2, max_length=50),
    scraper = Depends(get_timeanddate_scraper)
):
    """Fetch weather data from TimeAndDate for a specific location."""
    try:
        weather_data = await scraper.scrape(country, location)
        return weather_data
    except Exception as e:
        logger.error(f"Error fetching TimeAndDate weather data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{source}/{country}/{location}", responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_weather(
    source: str = Path(..., pattern="^(wunderground|timeanddate)$"),
    country: str = Path(..., min_length=2, max_length=50),
    location: str = Path(..., min_length=2, max_length=50)
):
    """Fetch weather data from a specified source for a specific location."""
    try:
        if source == "wunderground":
            return await get_wunderground_weather(country, location)
        elif source == "timeanddate":
            return await get_timeanddate_weather(country, location)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))