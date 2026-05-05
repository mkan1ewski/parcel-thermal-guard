class ThermalEvaluator:
    """
    Evaluates InPost points based on user's temperature constraints
    and parcel locker characterictics.
    """

    def is_weather_hazardous(
        self,
        forecasted_min_temp: float,
        forecasted_max_temp: float,
        user_min_tolerance: float,
        user_max_tolerance: float,
    ) -> bool:
        """
        Determines if the forecasted temperatures pose a risk to sensitive packages
        based on user-defined tolerance levels.
        """
        if forecasted_max_temp > user_max_tolerance:
            return True

        if forecasted_min_temp < user_min_tolerance:
            return True

        return False

    def categorize_point(self, point_data: dict, is_hazardous: bool) -> str:
        """
        Assigns a safety category to a single parcel point.

        Categories:
        - "GOLD": 100% safe (POP inside a shop or temperature-controlled locker).
        - "SILVER": Generally safe (Standard locker, but located indoors).
        - "DANGER": Unsafe during extreme weather (Standard outdoor locker).
        """
        point_types = point_data.get("type", [])
        location_type = point_data.get("location_type", "")
        supported_temperatures = point_data.get("supported_locker_temperatures")

        is_pop = "pop" in point_types
        is_fridge = supported_temperatures is not None

        if is_pop or is_fridge:
            return "GOLD"

        if location_type == "Indoor":
            return "SILVER"

        if location_type == "Outdoor":
            return "DANGER" if is_hazardous else "SILVER"

        return "UNKNOWN"
