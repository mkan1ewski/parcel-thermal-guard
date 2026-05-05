import httpx


class WeatherClient:
    """
    Client for fetching weather forecast and geocoding data from Open-Meteo API.
    """

    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.geocode_url = "https://geocoding-api.open-meteo.com/v1/search"

    async def get_city_coordinates(self, city_name: str) -> tuple[float, float] | None:
        """
        Converts a city name to latitude and longitude coordinates.
        Returns None if the city is not found.
        """
        params = {
            "name": city_name,
            "count": 1,
            "language": "pl",
            "format": "json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.geocode_url, params=params)
            response.raise_for_status()
            data = response.json()

            results = data.get("results")
            if not results:
                return None

            latitude = results[0]["latitude"]
            longitude = results[0]["longitude"]

            return latitude, longitude

    async def get_temperature_extremes(
        self, latitude: float, longitude: float, forecast_days: int
    ) -> tuple[float, float]:
        """
        Fetches the lowest and highest temperatures expected within the given timeframe.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": ["temperature_2m_max", "temperature_2m_min"],
            "forecast_days": forecast_days,
            "timezone": "auto",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            daily_max_temps = data["daily"]["temperature_2m_max"]
            daily_min_temps = data["daily"]["temperature_2m_min"]

            highest_expected_temp = max(daily_max_temps)
            lowest_expected_temp = min(daily_min_temps)

            return lowest_expected_temp, highest_expected_temp
