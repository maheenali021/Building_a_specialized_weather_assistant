from agents import function_tool
import os
import requests
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
from typing import Optional 

@dataclass
class WeatherInfo():
        temperature : float
        feels_like : float
        humidity : int
        description: str
        wind_speed:float
        pressure:int
        location_name: str
        visibility: Optional[int] = None
        
# kelvin to celcius convert 
def kelvin_to_celcius(kelvin:float )-> float:
    """Convert temperature in kelvin to celcius and round in two decimal numbers """
    return  round(kelvin - 273.15, 2)

@function_tool
def get_weather_info(location :str) -> str:
        """Get the current weather of the specific location from the weather api.
        Args:
        location : location of the city
        
        """ 
        weather_api = os.getenv("OPENWEATHERMAP_API_KEY")
        if not weather_api:
            return "Error: OPENWEATHERMAP_API_KEY environment variable not set."

        url = f"https://api.openweathermap.org/data/2.5/weather?&appid={weather_api}&q={location}&units=matric"
        
        try:
            
            response = requests.get(url)
            response.raise_for_status()
            data= response.json()
            temperature_kelvin=data["main"]["temp"]
            feels_like_kelvin=data["main"]["feels_like"]
            
            #extract weather info
            weather_info = WeatherInfo(
           temperature= kelvin_to_celcius(temperature_kelvin),
           feels_like=kelvin_to_celcius(feels_like_kelvin),
           humidity=data["main"]["humidity"],
           description=data["weather"][0]["description"],
           wind_speed=data["wind"]["speed"],
           pressure=data["main"]["pressure"],
           location_name=data["name"],)
            #creat the weather report into string formate
            weather_report = f"""
                Weather in { weather_info.location_name}: 
                Temperature: 🌡️ {weather_info.temperature}C
                feels like:💦 {weather_info.feels_like})
                Conditions:☁️ {weather_info.description}
                Humidity: 🌫️{weather_info.humidity}%
                Wind speed: 🌬️ {weather_info.wind_speed}m/s
                Pressure:🌡️ {weather_info.pressure} hpa
                """
            return weather_report
        
        
        except requests.exceptions.RequestException as e:
            
            return f"error fetching weather data {str(e)}"