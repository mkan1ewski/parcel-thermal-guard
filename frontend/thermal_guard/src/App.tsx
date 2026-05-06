import { useState } from "react";
import { fetchSafePoints, type ThermalApiResponse } from "./api";
import Map from "./Map";
import {
  MapPin,
  Search,
  Thermometer,
  ShieldCheck,
  Calendar,
  LocateFixed,
} from "lucide-react";
import "./App.css";

export default function App() {
  const [searchAddress, setSearchAddress] = useState("Warszawa, Złote Tarasy");
  const [radius, setRadius] = useState(1000);
  const [forecastDays, setForecastDays] = useState(3);
  const [minTemp, setMinTemp] = useState(5.0);
  const [maxTemp, setMaxTemp] = useState(25.0);

  const [isLoading, setIsLoading] = useState(false);
  const [apiData, setApiData] = useState<ThermalApiResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleGeolocation = () => {
    if (!navigator.geolocation) {
      setErrorMsg("Geolocation is not supported by your browser.");
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        try {
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&addressdetails=1`,
          );
          const data = await response.json();

          if (data && data.address) {
            const street = data.address.road || "";
            const houseNumber = data.address.house_number || "";
            const city =
              data.address.city ||
              data.address.town ||
              data.address.village ||
              "";

            const cleanPart1 = [street, houseNumber].filter(Boolean).join(" ");
            const cleanAddress = [cleanPart1, city].filter(Boolean).join(", ");

            setSearchAddress(cleanAddress || data.display_name);
          } else {
            setSearchAddress(`${latitude}, ${longitude}`);
          }
        } catch (err) {
          setErrorMsg("Failed to translate GPS coordinates to address.");
        } finally {
          setIsLoading(false);
        }
      },
      (_) => {
        setIsLoading(false);
        setErrorMsg("Please allow location permissions in your browser.");
      },
    );
  };

  const handleSearch = async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const data = await fetchSafePoints(
        searchAddress,
        radius,
        forecastDays,
        minTemp,
        maxTemp,
      );
      setApiData(data);
    } catch (err) {
      setErrorMsg("Failed to fetch data.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="header">
          <ShieldCheck size={32} color="#10b981" />
          <h1>Thermal Shield 🥵🥶 </h1>
        </div>
        <p className="subtitle">Protect your parcels from extreme weather.</p>

        <div className="input-group">
          <div className="address-header">
            <label>
              <MapPin size={16} /> Address
            </label>
            <button
              className="locate-btn"
              onClick={handleGeolocation}
              disabled={isLoading}
              title="Locate Me"
            >
              <LocateFixed size={16} /> My Location
            </button>
          </div>
          <input
            type="text"
            value={searchAddress}
            onChange={(e) => setSearchAddress(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>
            <Calendar size={16} /> Forecast: {forecastDays} days
          </label>
          <input
            type="range"
            min="1"
            max="7"
            step="1"
            value={forecastDays}
            onChange={(e) => setForecastDays(Number(e.target.value))}
          />
        </div>

        <div className="input-group">
          <label>Radius: {radius} meters</label>
          <input
            type="range"
            min="100"
            max="3000"
            step="100"
            value={radius}
            onChange={(e) => setRadius(Number(e.target.value))}
          />
        </div>

        <div className="input-group row">
          <div>
            <label>
              <Thermometer size={16} color="#3b82f6" /> Min Temp
            </label>
            <input
              type="number"
              value={minTemp}
              onChange={(e) => setMinTemp(Number(e.target.value))}
            />
          </div>
          <div>
            <label>
              <Thermometer size={16} color="#ef4444" /> Max Temp
            </label>
            <input
              type="number"
              value={maxTemp}
              onChange={(e) => setMaxTemp(Number(e.target.value))}
            />
          </div>
        </div>

        <button
          className="search-btn"
          onClick={handleSearch}
          disabled={isLoading}
        >
          {isLoading ? (
            "Scanning..."
          ) : (
            <>
              <Search size={18} /> Find Safe Points
            </>
          )}
        </button>

        {errorMsg && <div className="error">{errorMsg}</div>}

        {apiData && (
          <div className="results-summary">
            <h3>Scan Complete</h3>
            <p>
              <strong>Min forecasted:</strong>{" "}
              {apiData.metadata.forecasted_min_temperature}°C
            </p>
            <p>
              <strong>Max forecasted:</strong>{" "}
              {apiData.metadata.forecasted_max_temperature}°C
            </p>
            <p>
              <strong>Hazard detected:</strong>{" "}
              {apiData.metadata.hazard_detected ? "YES ⚠️" : "NO ✅"}
            </p>
            <p>
              <strong>Safe machines:</strong>{" "}
              {apiData.metadata.safe_machines_returned} out of{" "}
              {apiData.metadata.total_machines_in_radius}
            </p>
          </div>
        )}
      </aside>

      <main className="map-area">
        {apiData ? (
          <Map center={apiData.metadata.coordinates} points={apiData.points} />
        ) : (
          <div className="map-placeholder">
            Enter an address and click Search.
          </div>
        )}
      </main>
    </div>
  );
}
