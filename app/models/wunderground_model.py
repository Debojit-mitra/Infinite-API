from pydantic import BaseModel
from typing import Optional

class Temperature(BaseModel):
    F: float
    C: float

class Condition(BaseModel):
    icon: Optional[str]
    description: str

class AirQuality(BaseModel):
    aqi_value: str
    aqi_type: str
    api_icon: str
    aqi_suggestion: str
    dominant_pollutant: str
    pollutant_desc: str

class AdditionalConditions(BaseModel):
    pressure: dict
    visibility: dict
    clouds: str
    dew_point: dict
    humidity: dict
    rainfall: dict
    snow_depth: dict

class Astronomy(BaseModel):
    sun: dict
    moon: dict

class WundergroundWeatherData(BaseModel):
    location: str
    temperature: Temperature
    feels_like: Temperature
    condition: Condition
    forecast: str
    pollen: str
    air_quality: AirQuality
    additional_conditions: AdditionalConditions
    astronomy: Astronomy