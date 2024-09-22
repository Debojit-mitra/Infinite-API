import logging
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from app.models.gsmarena_model import GSMArenaSearchResponse, PhoneDetailsResponse
from app.models.errorResponse_model import ErrorResponse
from app.dependencies import get_gsmarena_scraper, get_gsmarena_phone_info_scraper

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/gsmarena", response_model=PhoneDetailsResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_phone_details(
    id: str = Query(..., description="URL of the phone details page on GSMArena"),
    scraper = Depends(get_gsmarena_phone_info_scraper)
):
    """Fetch detailed phone specifications from GSMArena for a specific phone URL."""
    try:
        phone_details = await scraper.scrape_phone_details(id)
        return phone_details
    except Exception as e:
        logger.error(f"Error fetching phone details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gsmarena/top", response_model=GSMArenaSearchResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_top_phones(
    scraper = Depends(get_gsmarena_scraper)
):
    """Fetch top seventy phones from GSMArena."""
    try:
        phone_details = await scraper.scrapeTopSeventy()
        return phone_details
    except Exception as e:
        logger.error(f"Error fetching top phones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gsmarena/{search_query}", response_model=GSMArenaSearchResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_gsmarena_phones(
    search_query: str = Path(..., min_length=1, max_length=200),
    scraper = Depends(get_gsmarena_scraper)
):
    """Fetch phone data from GSMArena for a specific search query."""
    try:
        phone_data = await scraper.scrape(search_query)
        return phone_data
    except Exception as e:
        logger.error(f"Error fetching GSMArena phones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))