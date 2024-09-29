import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.hero_model import HeroSearchResponse, HeroDetail
from app.dependencies import get_heroes_scraper
from app.models.errorResponse_model import ErrorResponse
from typing import List

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/heroes", response_model=HeroSearchResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_heroes(
    start: str = Query(..., min_length=1, max_length=1),
    scraper = Depends(get_heroes_scraper)
):
    """Fetch superhero data from the hero fandom website starting with a specific letter."""
    valid_starts = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    
    if start not in valid_starts:
        logger.warning(f"Invalid starting character: {start}")
        raise HTTPException(status_code=400, detail="Invalid starting character. Please use # or A-Z.")
    
    logger.info(f"Fetching heroes starting with '{start}'")
    try:
        search_response = await scraper.scrape(start.upper())
        logger.info(f"Successfully fetched heroes starting with '{start}'")
        return search_response
    except Exception as e:
        logger.error(f"Error fetching hero data for start '{start}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/details", response_model=HeroDetail, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_hero_detail(
    heroid: str = Query(..., description="The ID of the hero to fetch details for"),
    scraper = Depends(get_heroes_scraper)
):
    """Fetch detailed information about a specific hero."""
    logger.info(f"Fetching hero details for ID: {heroid}")
    try:
        hero_detail = await scraper.scrape_hero_detail(heroid)
        logger.info(f"Successfully fetched hero details for ID: {heroid}")
        return hero_detail
    except Exception as e:
        logger.error(f"Error fetching hero detail for ID {heroid}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=HeroSearchResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def search_heroes(
    query: str = Query(..., description="The search query"),
    scraper = Depends(get_heroes_scraper)
):
    """Search for heroes based on a query."""
    logger.info(f"Searching heroes with query: '{query}'")
    try:
        search_response = await scraper.search_heroes(query)
        logger.info(f"Successfully searched heroes with query: '{query}'")
        return search_response
    except Exception as e:
        logger.error(f"Error searching heroes with query '{query}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))