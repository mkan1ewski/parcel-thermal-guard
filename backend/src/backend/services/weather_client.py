import httpx


class WeatherClient:
    """
    Client for fetching weather forecast data from Open-Meteo API.
    """

    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

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
