import axios from 'axios';

export interface AddressDetails {
    city: string;
    street: string;
    building_number: string;
}

export interface SafePoint {
    id: string;
    address: AddressDetails;
    latitude: number;
    longitude: number;
    safety_category: "GOLD" | "SILVER" | "DANGER" | "UNKNOWN";
    location_type: string;
}

export interface Metadata {
    address_searched: string;
    coordinates: { lat: number; lon: number };
    radius_meters: number;
    forecast_days: number;
    forecasted_min_temperature: number;
    forecasted_max_temperature: number;
    hazard_detected: boolean;
    total_machines_in_radius: number;
    safe_machines_returned: number;
}

export interface ThermalApiResponse {
    metadata: Metadata;
    points: SafePoint[];
}

const API_BASE_URL = 'http://127.0.0.1:8000';

export const fetchSafePoints = async (
    address: string,
    radiusMeters: number = 1500,
    forecastDays: number = 3,
    minTemp: number = 5.0,
    maxTemp: number = 25.0
): Promise<ThermalApiResponse> => {
    const response = await axios.get<ThermalApiResponse>(`${API_BASE_URL}/api/safe-points`, {
        params: {
            address: address,
            radius_meters: radiusMeters,
            forecast_days: forecastDays,
            min_temp_tolerance: minTemp,
            max_temp_tolerance: maxTemp
        }
    });
    return response.data;
};