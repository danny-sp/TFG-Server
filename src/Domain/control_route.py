from typing import Tuple, List
from geopy.distance import geodesic

from src.Persistance.route_client import RouteClient

from src.Utils.logger import setup_logger

class ControlRoute:

    _logger = setup_logger("ControlRoute")

    @classmethod
    def get_route_str(cls, coords: Tuple[float, float], destination: str):
        start_coords = coords

        if destination == "BILBAO":
            end_coords = (43.262873, -2.947564)
        elif destination == "MADRID":
            end_coords = (40.451843, -3.686502)
        else:
            cls._logger.warning(f"Unknown destination '{destination}' requested")
            return None

        cls._logger.debug(f"Fetching route from {start_coords} to {end_coords} for destination '{destination}'")
        response = RouteClient.get_route_geometry(start_coords, end_coords)

        if response is None:
            cls._logger.warning(f"No route found for destination '{destination}'")
            return None

        return response

    @classmethod
    def get_route_coords(cls, coords: Tuple[float, float], destination: Tuple[float, float]):
        start_coords = coords
        end_coords = destination

        # cls._logger.debug(f"Fetching route from {start_coords} to {end_coords} for custom coordinates")
        response = RouteClient.get_route_geometry(start_coords, end_coords)

        if response is None:
            cls._logger.warning(f"No route found for custom coordinates {destination}")
            return None

        return response

    @classmethod
    def get_distance_coords(cls, coords: Tuple[float, float], destination: Tuple[float, float]) -> float:
        start_coords = coords
        end_coords = destination

        cls._logger.debug(f"Fetching distance from {start_coords} to {end_coords} for custom coordinates")
        response = RouteClient.get_route_geometry(start_coords, end_coords)

        if response is None:
            cls._logger.warning(f"No route found for custom coordinates {destination}")
            distance = geodesic(start_coords, end_coords).kilometers
        else:
            _, distance, _ = response
            distance /= 1000

        return distance

    @classmethod
    def get_duration_list(cls, coords: List[Tuple[float, float]]) -> float:
        if len(coords) < 2:
            cls._logger.warning("At least two coordinates are required to calculate duration")
            return None

        url = "http://localhost:5000/route/v1/driving/"

        for c in coords:
            url += f"{c[1]},{c[0]};"

        url = url[:-1]  # Remove semicolon
        url += "?overview=full"

        response = RouteClient.get_route_geometry_list(url)

        if response is None:
            cls._logger.warning("No route found for given coordinates")
            return None

        _, _, duration = response

        return duration
