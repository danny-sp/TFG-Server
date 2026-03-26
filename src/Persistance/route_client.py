"""
Module containing methods for interacting with an OSRM HTTP server to retrieve route geometry, distance, and duration.
"""

import polyline
import requests

from src.Utils.logger import setup_logger

_logger = setup_logger("RouteClient")


def get_route_geometry(
    start_coords, end_coords
) -> tuple[list[tuple[float, float]], float, float] | None:
    """
    Gets the route geometry, distance, and duration between two coordinates using an OSRM HTTP server.

    Args:
        start_coords (tuple): A tuple of (latitude, longitude) for the starting point.
        end_coords (tuple): A tuple of (latitude, longitude) for the destination point.

    Returns:
        geometry (list of tuples): A list of (latitude, longitude) tuples representing the route geometry.
        distance (float): The total distance of the route in meters.
        duration (float): The total duration of the route in seconds.
    """

    url = f"http://localhost:5000/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["code"] != "Ok":
            _logger.error(f"Error with OSRM: {data['code']}")
            return None

        encoded_geometry = data["routes"][0]["geometry"]
        distance = data["routes"][0]["distance"]
        duration = data["routes"][0]["duration"]
        return polyline.decode(encoded_geometry), distance, duration

    except requests.RequestException as e:
        _logger.error(f"Connection error: {e}")
        return None


def get_route_geometry_list(
    url: str,
) -> tuple[list[tuple[float, float]], float, float] | None:
    """
    Executes a GET request to the specified URL to retrieve route geometry, distance, and duration.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        geometry (list of tuples): A list of (latitude, longitude) tuples representing the route geometry.
        distance (float): The total distance of the route in meters.
        duration (float): The total duration of the route in seconds.
    """

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["code"] != "Ok":
            _logger.error(f"Error with OSRM: {data['code']}")
            return None

        encoded_geometry = data["routes"][0]["geometry"]
        distance = data["routes"][0]["distance"]
        duration = data["routes"][0]["duration"]
        return polyline.decode(encoded_geometry), distance, duration

    except requests.RequestException as e:
        _logger.error(f"Connection error: {e}")
        return None
