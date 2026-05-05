import httpx


class LocationClient:
    """
    Client for geocoding precise street addresses using OpenStreetMap's Nominatim API.
    """

    def __init__(self):
        self.geocode_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {"User-Agent": "ThermalShieldApp/1.0"}

    async def get_coordinates_from_address(
        self, address: str
    ) -> tuple[float, float] | None:
        """
        Converts a full street address (e.g., 'Polna 5, Warszawa') to exact coordinates.
        """
        params = {"q": address, "format": "json", "limit": 1}

        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(self.geocode_url, params=params)

            if response.status_code != 200:
                print(f" Warning: Nominatim API returned status {response.status_code}")
                return None

            results = response.json()
            if not results:
                return None

            lat = float(results[0]["lat"])
            lon = float(results[0]["lon"])
            return lat, lon
