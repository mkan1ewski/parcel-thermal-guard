import { useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { type SafePoint } from "./api";
import { memo } from "react";

function MapUpdater({ center }: { center: [number, number] }) {
  const map = useMap();
  useEffect(() => {
    map.flyTo(center, 14, { duration: 1.5 });
  }, [center, map]);
  return null;
}

interface MapProps {
  center: { lat: number; lon: number };
  points: SafePoint[];
}

function Map({ center, points }: MapProps) {
  const centerPosition: [number, number] = [center.lat, center.lon];

  return (
    <MapContainer
      center={centerPosition}
      zoom={14}
      style={{ height: "100%", width: "100%", zIndex: 0 }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <MapUpdater center={centerPosition} />

      <CircleMarker
        center={centerPosition}
        pathOptions={{
          color: "#3b82f6",
          fillColor: "#3b82f6",
          fillOpacity: 0.8,
        }}
        radius={10}
      >
        <Popup>
          <strong>Scan Center</strong>
          <br />
          You are here.
        </Popup>
      </CircleMarker>

      {points.map((point) => {
        const isGold = point.safety_category === "GOLD";
        const dotColor = isGold ? "#f59e0b" : "#10b981";

        return (
          <CircleMarker
            key={point.id}
            center={[point.latitude, point.longitude]}
            pathOptions={{
              color: dotColor,
              fillColor: dotColor,
              fillOpacity: 0.8,
            }}
            radius={7}
          >
            <Popup>
              <strong>{point.id}</strong> {isGold && "⭐"} <br />
              {point.address.street} {point.address.building_number} <br />
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}

export default memo(Map);
