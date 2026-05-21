"""
Route calculation utilities for the system.
"""

from typing import List, Tuple

from geopy.distance import geodesic  # type: ignore

import src.Persistence.web_client as RouteClient
from src.Utils.logger import setup_logger

_logger = setup_logger("ControlRoute")


def get_route_str(
    coords: Tuple[float, float], destination: str
) -> Tuple[List[Tuple[float, float]], float, float] | None:
    """
    Gets the route geometry, distance, and duration between a starting coordinate and a predefined destination.
    Args:
        coords (Tuple[float, float]): A tuple of (latitude, longitude) for the starting point.
        destination (str): A string representing the destination, either "BILBAO" or "MADRID".

    Returns:
        Tuple[List[Tuple[float, float]], float, float]: A tuple containing the route geometry as a list of coordinates, the distance in kilometers, and the duration in seconds.
    """

    start_coords = coords

    if destination == "BILBAO":
        end_coords = (43.262873, -2.947564)
    elif destination == "MADRID":
        end_coords = (40.451843, -3.686502)
    else:
        _logger.warning(f"Unknown destination '{destination}' requested")
        return None

    _logger.debug(
        f"Fetching route from {start_coords} to {end_coords} for destination '{destination}'"
    )
    response = RouteClient.get_route_geometry(start_coords, end_coords)

    if response is None:
        _logger.warning(f"No route found for destination '{destination}'")
        return None

    return response


def get_route_coords(
    coords: Tuple[float, float], destination: Tuple[float, float]
) -> Tuple[List[Tuple[float, float]], float, float] | None:
    """
    Gets the route geometry, distance, and duration between two coordinates.

    Args:
        coords (Tuple[float, float]): A tuple of (latitude, longitude) for the starting point.
        destination (Tuple[float, float]): A tuple of (latitude, longitude) for the destination point.

    Returns:
        Tuple[List[Tuple[float, float]], float, float]: A tuple containing the route geometry as a list of coordinates, the distance in kilometers, and the duration in seconds.
    """

    start_coords = coords
    end_coords = destination

    # cls._logger.debug(f"Fetching route from {start_coords} to {end_coords} for custom coordinates")
    response = RouteClient.get_route_geometry(start_coords, end_coords)

    if response is None:
        _logger.warning(f"No route found for custom coordinates {destination}")
        return None

    return response


def get_distance_coords(
    coords: Tuple[float, float], destination: Tuple[float, float]
) -> float:
    """
    Gets the distance in kilometers between two coordinates.

    Args:
        coords (Tuple[float, float]): A tuple of (latitude, longitude) for the starting point.
        destination (Tuple[float, float]): A tuple of (latitude, longitude) for the destination point.

    Returns:
        float: The distance between the two points in kilometers.
    """

    start_coords = coords
    end_coords = destination

    _logger.debug(
        f"Fetching distance from {start_coords} to {end_coords} for custom coordinates"
    )
    response = RouteClient.get_route_geometry(start_coords, end_coords)

    if response is None:
        _logger.warning(f"No route found for custom coordinates {destination}")
        distance = geodesic(start_coords, end_coords).kilometers
    else:
        _, distance, _ = response
        distance /= 1000

    return distance


def get_duration_list(coords: List[Tuple[float, float]]) -> float:
    """
    Gets the total duration of a route defined by a list of coordinates.

    Args:
        coords (List[Tuple[float, float]]): A list of (latitude, longitude) tuples representing the route waypoints.

    Returns:
            float: The total duration of the route in seconds.
    """

    if len(coords) < 2:
        _logger.warning("At least two coordinates are required to calculate duration")
        raise ValueError("At least two coordinates are required to calculate duration")

    url = "http://localhost:5000/route/v1/driving/"

    for c in coords:
        url += f"{c[1]},{c[0]};"

    url = url[:-1]  # Remove semicolon
    url += "?overview=full"

    response = RouteClient.get_http(url)

    if response is None:
        _logger.warning("No route found for given coordinates")
        raise Exception("No route found for given coordinates")

    duration = response["routes"][0]["duration"]

    return duration
