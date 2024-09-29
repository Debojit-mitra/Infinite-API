import logging
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from app.models.libgen_model import DownloadLinkResponse, LibgenSearchResponse
from app.models.errorResponse_model import ErrorResponse
from app.dependencies import get_libgen_download_scraper
from app.scrapers.libgen_scraper import LibgenScraper

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/libgen/download/{source}/{download_id}", response_model=DownloadLinkResponse, responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_download_link(
    source: str = Path(..., pattern="^(library_lol|libgen_li)$"),
    download_id: str = Path(..., min_length=32, max_length=32),
    scraper = Depends(get_libgen_download_scraper)
):
    """Fetch download link for a specific book from Libgen."""
    logger.info(f"Fetching download link for source: {source}, ID: {download_id}")
    try:
        if source == "library_lol":
            download_link = await scraper.get_library_lol_link(download_id)
        else:  # source == "libgen_li"
            download_link = await scraper.get_libgen_li_link(download_id)

        if not download_link:
            logger.warning(f"Download link not found for source: {source}, ID: {download_id}")
            raise HTTPException(status_code=404, detail="Download link not found")

        logger.info(f"Successfully fetched download link for source: {source}, ID: {download_id}")
        return DownloadLinkResponse(download_link=download_link)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching download link for source: {source}, ID: {download_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/libgen/{bookname}", response_model=LibgenSearchResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_libgen_books(
    bookname: str = Path(..., min_length=1, max_length=200)
):
    """Fetch book data from Libgen for a specific book name."""
    libgen_scraper = LibgenScraper()
    logger.info(f"Searching Libgen for book: '{bookname}'")
    try:
        search_response = await libgen_scraper.scrape(bookname)
        logger.info(f"Successfully fetched Libgen books for: '{bookname}'")
        return search_response
    except Exception as e:
        logger.error(f"Error fetching Libgen books for '{bookname}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))