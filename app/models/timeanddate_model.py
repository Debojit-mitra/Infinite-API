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

# 14 day forecast
class DailyForecast(BaseModel):
    date: str
    day: str
    temperature_high: int
    temperature_low: int
    condition: str
    condition_icon: str
    feels_like: int
    wind_speed: str
    wind_direction: str
    humidity: str
    precipitation_chance: str
    precipitation_amount: str
    uv_index: str
    sunrise: str
    sunset: str

class FourteenDayForecast(BaseModel):
    location: str
    forecast: List[DailyForecast]

# 24 hour forecast
class HourlyForecast(BaseModel):
    time: str
    date: str
    temperature: int
    condition: str
    condition_icon: str
    feels_like: int
    wind_speed: str
    wind_direction: str
    humidity: str
    precipitation_chance: str
    precipitation_amount: str

class TwentyFourHourForecast(BaseModel):
    location: str
    forecast: List[HourlyForecast]