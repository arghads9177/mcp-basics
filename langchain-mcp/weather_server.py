# A weather MCP server containing weather tools. Call weather APIs here.

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Any
import datetime

# Load environment variables from .env file
load_dotenv()
# Get the OpenWeatherMap API key from environment variables
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

# Initialize the FastMCP server
app = FastMCP("Weather MCP")

# Base URL for OpenWeatherMap API
OWM_API_BASE = "https://api.openweathermap.org/data/2.5"
USER_AGENT = "weather-mcp/1.0"

async def make_owm_request(url: str, params: dict[str, Any]) -> dict[str, Any] | None:
    """Make a request to the OpenWeatherMap API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@app.tool()
async def get_current_weather(city: str, country: str) -> str:
    """Get current weather for a city.

    Args:
        city: City name (e.g. London)
        country: Country code (e.g. GB)
    """
    url = f"{OWM_API_BASE}/weather"
    params = {
        "q": f"{city},{country}",
        "appid": OPEN_WEATHER_API_KEY,
        "units": "metric"
    }
    data = await make_owm_request(url, params)

    if not data or "weather" not in data:
        return "Unable to fetch weather data."

    weather_desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    return (f"Current weather in {city}, {country}:\n"
            f"Description: {weather_desc}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s")

if __name__ == "__main__":
    app.run(transport="streamable-http")