import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.anime.mal_model import (MalResponseType1, AnimeSeasonAndScheduleResponse, AnimeSearchResponse, AnimeDetails, CharacterDetails, PersonDetails)
from app.dependencies import get_anime_scraper, get_anime_season_and_schedule_scraper, get_anime_search_scraper, get_anime_details_scraper
from typing import Optional, List

router = APIRouter()
logger = logging.getLogger(__name__)

# MyAnimeList
# top and popular
@router.get("/mal/top", response_model=MalResponseType1)
async def get_top_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=100),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching top anime, page: {page}")
    try:
        result = await scraper.scrape_top_anime(page, total_pages=100)
        logger.info(f"Successfully fetched top anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching top anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/top_airing", response_model=MalResponseType1)
async def get_top_airing_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=5),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching top airing anime, page: {page}")
    try:
        result = await scraper.scrape_top_airing(page, total_pages=5)
        logger.info(f"Successfully fetched top airing anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching top airing anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/top_upcoming", response_model=MalResponseType1)
async def get_top_upcoming_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=6),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching top upcoming anime, page: {page}")
    try:
        result = await scraper.scrape_top_upcoming(page, total_pages=6)
        logger.info(f"Successfully fetched top upcoming anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching top upcoming anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/top_series", response_model=MalResponseType1)
async def get_top_series_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=100),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching top TV series anime, page: {page}")
    try:
        result = await scraper.scrape_top_tv_series(page, total_pages=100)
        logger.info(f"Successfully fetched top TV series anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching top TV series anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/top_movies", response_model=MalResponseType1)
async def get_top_movies_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=40),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching top anime movies, page: {page}")
    try:
        result = await scraper.scrape_top_movies(page, total_pages=40)
        logger.info(f"Successfully fetched top anime movies, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching top anime movies, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/top_ova", response_model=MalResponseType1)
async def get_top_ova_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=30),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching top OVA anime, page: {page}")
    try:
        result = await scraper.scrape_top_ova(page, total_pages=30)
        logger.info(f"Successfully fetched top OVA anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching top OVA anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/top_ona", response_model=MalResponseType1)
async def get_top_ona_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=30),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching top ONA anime, page: {page}")
    try:
        result = await scraper.scrape_top_ona(page, total_pages=30)
        logger.info(f"Successfully fetched top ONA anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching top ONA anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/top_special", response_model=MalResponseType1)
async def get_top_special_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=36),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching top special anime, page: {page}")
    try:
        result = await scraper.scrape_top_special(page, total_pages=36)
        logger.info(f"Successfully fetched top special anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching top special anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/most_popular", response_model=MalResponseType1)
async def get_most_popular_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=100),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching most popular anime, page: {page}")
    try:
        result = await scraper.scrape_most_popular(page, total_pages=100)
        logger.info(f"Successfully fetched most popular anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching most popular anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mal/most_fav", response_model=MalResponseType1)
async def get_most_favorited_anime(
    page: int = Query(1, description="Page number, starting from 1", ge=1, le=100),
    scraper = Depends(get_anime_scraper)
):
    logger.info(f"Fetching most favorited anime, page: {page}")
    try:
        result = await scraper.scrape_most_favorited(page, total_pages=100)
        logger.info(f"Successfully fetched most favorited anime, page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error fetching most favorited anime, page {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Seasons
@router.get("/mal/season", response_model=AnimeSeasonAndScheduleResponse)
async def get_anime_season(
    y: Optional[int] = Query(None, description="Year of the anime season"),
    s: Optional[str] = Query(None, description="Season (winter, spring, summer, fall)"),
    scraper = Depends(get_anime_season_and_schedule_scraper)
):
    logger.info(f"Fetching anime season, year: {y}, season: {s}")
    try:
        result = await scraper.scrape_anime_season(y, s)
        logger.info(f"Successfully fetched anime season, year: {y}, season: {s}")
        return result
    except Exception as e:
        logger.error(f"Error fetching anime season, year: {y}, season: {s}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# schedule
@router.get("/mal/schedule", response_model=AnimeSeasonAndScheduleResponse)
async def get_anime_schedule(
    scraper = Depends(get_anime_season_and_schedule_scraper)
):
    logger.info("Fetching anime schedule")
    try:
        result = await scraper.scrape_anime_schedule()
        logger.info("Successfully fetched anime schedule")
        return result
    except Exception as e:
        logger.error(f"Error fetching anime schedule: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# search
@router.get("/mal/search", response_model=AnimeSearchResponse)
async def search_anime(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, description="Page number, starting from 1", ge=1),
    type: Optional[str] = Query(None, description="Anime type (tv / ova / movie / special / ona / music)"),
    score: Optional[int] = Query(None, description="Minimum score (1-10)", ge=1, le=10),
    status: Optional[str] = Query(None, description="Airing status (finshed / airing / not_aired)"),
    genre: Optional[str] = Query(None, description="Genre names. Available genres: action, adventure, avant garde, award winning, boys love, comedy, drama, fantasy, girls love, gourmet, horror, mystery, romance, sci-fi, slice of life, sports, supernatural, suspense, ecchi, erotica, hentai"),
    adult: Optional[bool] = Query(None, description="Whether to include adult anime's (true / false). (default=false). To use explicit genres like ecchi, erotica and hentai it must be true."),
    demographic: Optional[str] = Query(None, description="demographics (josei / kids / seinen / shoujo / shounen)"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    scraper = Depends(get_anime_search_scraper)
):
    logger.info(f"Searching anime with query: '{q}', page: {page}")
    try:
        genre_list = genre.split(',') if genre else None
        result = await scraper.search_anime(
            q=q, 
            page=page, 
            type=type, 
            score=score, 
            status=status, 
            genre=genre_list,
            demographic=demographic,
            adult=adult, 
            start_date=start_date, 
            end_date=end_date
        )
        logger.info(f"Successfully searched anime with query: '{q}', page: {page}")
        return result
    except Exception as e:
        logger.error(f"Error searching anime with query: '{q}', page: {page}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Anime details
@router.get("/mal/details", response_model=AnimeDetails)
async def get_anime_details(
    id: int = Query(..., description="MyAnimeList ID of the anime"),
    scraper = Depends(get_anime_details_scraper)
):
    logger.info(f"Fetching anime details for ID: {id}")
    try:
        result = await scraper.scrape_anime_details(id)
        logger.info(f"Successfully fetched anime details for ID: {id}")
        return result
    except Exception as e:
        logger.error(f"Error fetching anime details for ID {id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
# Anime character details
@router.get("/mal/character", response_model=CharacterDetails)
async def get_character_details(
    id: int = Query(..., description="MyAnimeList ID of the character"),
    scraper = Depends(get_anime_details_scraper)
):
    logger.info(f"Fetching character details for ID: {id}")
    try:
        result = await scraper.scrape_character_details(id)
        logger.info(f"Successfully fetched character details for ID: {id}")
        return result
    except Exception as e:
        logger.error(f"Error fetching character details for ID {id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
# People details
@router.get("/mal/person", response_model=PersonDetails)
async def get_person_details(
    id: int = Query(..., description="MyAnimeList ID of the person"),
    scraper = Depends(get_anime_details_scraper)
):
    logger.info(f"Fetching person details for ID: {id}")
    try:
        result = await scraper.scrape_person_details(id)
        logger.info(f"Successfully fetched person details for ID: {id}")
        return result
    except Exception as e:
        logger.error(f"Error fetching person details for ID {id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))