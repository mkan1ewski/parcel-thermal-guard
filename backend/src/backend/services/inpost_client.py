import httpx
from typing import Any
from geopy.distance import geodesic


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
        Retrieves InPost points and filters them by physical distance.
        """
        valid_points = []
        current_page = 1
        total_pages = 1

        async with httpx.AsyncClient() as client:
            while current_page <= total_pages:
                params = {
                    "relative_point": f"{latitude},{longitude}",
                    "per_page": 100,
                    "page": current_page,
                }

                response = await client.get(self.base_url, params=params)
                if response.status_code != 200:
                    break

                data = response.json()
                items = data.get("items", [])

                for point in items:
                    p_lat = point.get("location", {}).get("latitude")
                    p_lon = point.get("location", {}).get("longitude")

                    if p_lat and p_lon:
                        distance = geodesic(
                            (latitude, longitude), (p_lat, p_lon)
                        ).meters

                        if distance <= radius_meters:
                            point["distance_meters"] = round(distance)
                            valid_points.append(point)
                        else:
                            return valid_points

                if current_page == 1:
                    total_pages = data.get("total_pages", 1)

                current_page += 1

        return valid_points
