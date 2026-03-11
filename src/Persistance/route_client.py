import requests
import polyline

from src.Utils.logger import setup_logger

class RouteClient:
    _logger = setup_logger("RouteClient")

    @classmethod
    def get_route_geometry(cls, start_coords, end_coords):
        url = f"http://localhost:5000/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if data["code"] != "Ok":
                cls._logger.error(f"Error with OSRM: {data['code']}")
                return None

            encoded_geometry = data['routes'][0]['geometry']
            distance = data['routes'][0]['distance']
            duration = data['routes'][0]['duration']
            return polyline.decode(encoded_geometry), distance, duration

        except requests.RequestException as e:
            cls._logger.error(f"Connection error: {e}")
            return None

    @classmethod
    def get_route_geometry_list(cls, url: str):
        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if data["code"] != "Ok":
                cls._logger.error(f"Error with OSRM: {data['code']}")
                return None

            encoded_geometry = data['routes'][0]['geometry']
            distance = data['routes'][0]['distance']
            duration = data['routes'][0]['duration']
            return polyline.decode(encoded_geometry), distance, duration

        except requests.RequestException as e:
            cls._logger.error(f"Connection error: {e}")
            return None
