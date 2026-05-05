import httpx
from typing import Any


class InpostClient:
    """
    Client for fetching parcel locker data from the InPost API.
    """

    def __init__(self):
        self.base_url = "https://api-global-points.easypack24.net/v1/points"

    async def get_points_by_radius(
        self, latitude: float, longitude: float, radius_meters: int = 1500
    ) -> list[dict[str, Any]]:
        """
        Retrieves InPost points within a strict physical radius from a specific GPS coordinate.
        """
        all_points = []
        current_page = 1
        total_pages = 1

        async with httpx.AsyncClient() as client:
            while current_page <= total_pages:
                params = {
                    "relative_point": f"{latitude},{longitude}",
                    "relative_distance": radius_meters,
                    "per_page": 100,
                    "page": current_page,
                }

                response = await client.get(self.base_url, params=params)
                if response.status_code != 200:
                    break
                data = response.json()
                all_points.extend(data.get("items", []))

                if current_page == 1:
                    total_pages = data.get("total_pages", 1)
                current_page += 1

        return all_points
