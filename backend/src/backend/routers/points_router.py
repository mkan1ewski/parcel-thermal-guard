from fastapi import APIRouter, HTTPException, Query
from backend.services.location_client import LocationClient
from backend.services.weather_client import WeatherClient
from backend.services.inpost_client import InpostClient
from backend.services.thermal_evaluator import ThermalEvaluator

points_router = APIRouter()
location_client = LocationClient()
weather_client = WeatherClient()
inpost_client = InpostClient()
thermal_evaluator = ThermalEvaluator()

@points_router.get("/api/safe-points")
async def get_safe_points(
    address: str = Query(..., description="Full address, e.g., Złote Tarasy, Warszawa"),
    radius_meters: int = Query(1500, description="Search radius in meters"),
    forecast_days: int = Query(3, ge=1, le=7, description="Number of days the package might wait"),
    min_temp_tolerance: float = Query(5.0, description="User's lowest safe temperature (Celsius)"),
    max_temp_tolerance: float = Query(25.0, description="User's highest safe temperature (Celsius)")
):
    coords = await location_client.get_coordinates_from_address(address)
    if not coords:
        raise HTTPException(
            status_code=404,
            detail="Address not found. Please try being more specific (e.g., 'Polna 5, Warszawa')."
        )
    latitude, longitude = coords

    lowest_temp, highest_temp = await weather_client.get_temperature_extremes(
        latitude, longitude, forecast_days
    )

    is_hazardous = thermal_evaluator.is_weather_hazardous(
        forecasted_min_temp=lowest_temp,
        forecasted_max_temp=highest_temp,
        user_min_tolerance=min_temp_tolerance,
        user_max_tolerance=max_temp_tolerance
    )

    raw_points = await inpost_client.get_points_by_radius(latitude, longitude, radius_meters)

    safe_points = []
    for point in raw_points:
        category = thermal_evaluator.categorize_point(point, is_hazardous)

        if category in ["GOLD", "SILVER"]:
            safe_points.append({
                "id": point.get("name"),
                "address": point.get("address_details", {}),
                "latitude": point.get("location", {}).get("latitude"),
                "longitude": point.get("location", {}).get("longitude"),
                "safety_category": category,
                "location_type": point.get("location_type")
            })

    return {
        "metadata": {
            "address_searched": address,
            "coordinates": {"lat": latitude, "lon": longitude},
            "radius_meters": radius_meters,
            "forecast_days": forecast_days,
            "forecasted_min_temperature": lowest_temp,
            "forecasted_max_temperature": highest_temp,
            "hazard_detected": is_hazardous,
            "total_machines_in_radius": len(raw_points),
            "safe_machines_returned": len(safe_points)
        },
        "points": safe_points
    }