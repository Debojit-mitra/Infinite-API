import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware import ErrorHandlingMiddleware
from app.api import weather, books, phones, hero

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title="Infinite API", description="Collection of multiple APIs.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandlingMiddleware)

app.include_router(weather.router, prefix="/weather", tags=["weather"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(phones.router, prefix="/phones", tags=["phones"])
app.include_router(hero.router, prefix="/hero", tags=["heroes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Infinite API! Made with ❤ by Debojit."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)