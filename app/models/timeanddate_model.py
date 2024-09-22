from pydantic import BaseModel
from typing import Optional, List, Dict

class SunMoonData(BaseModel):
    moon_percent: str
    moon_title: str
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    daylight_hours: str

class AstronomyData(BaseModel):
    sun_moon: SunMoonData

class Temperature(BaseModel):
    C: Optional[float] = None
    F: Optional[float] = None

class Condition(BaseModel):
    description: str
    icon: Optional[str] = None

class AdditionalConditions(BaseModel):
    pressure: Dict[str, str]
    visibility: Dict[str, str]
    humidity: Dict[str, str]
    dew_point: Dict[str, str]
    wind: str

class FiveHourForecast(BaseModel):
    time: str
    temperature: str
    description: str
    icon: Optional[str] = None

class TimeAndDateWeatherData(BaseModel):
    location: str
    temperature: Temperature
    feels_like: Temperature
    condition: Condition
    forecast: str
    additional_conditions: AdditionalConditions
    fiveHourForecast: List[FiveHourForecast]

    class Config:
        extra = 'allow'