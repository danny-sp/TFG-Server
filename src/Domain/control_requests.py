"""
Processes routing requests from EV users.
"""

import json
from datetime import datetime, timedelta

import src.Domain.bookingDAO as BookingDAO
import src.Domain.charging_stationDAO as charging_stationDAO
import src.Domain.control_route as ControlRoute
import src.Domain.serviceDAO as ServiceDAO
import src.Domain.vehicleDAO as VehicleDAO
from src.Domain.option import Option
from src.Domain.request import Request
from src.Utils.logger import setup_logger


class ControlRequests:
    """
    Processes routing requests from EV users.
    """

    _requests: set[str] = set()

    _logger = setup_logger("ControlRequests")

    @classmethod
    def process_request(cls, request_data: dict) -> str:
        """
        Processes a routing request from an EV user:
            1. Validates the request and checks for duplicates.
            2. Checks if the vehicle has any active bookings.
            3. Calculates the remaining route and duration to the destination.
            4. Retrieves charging stations in the area of the remaining route.
            5. Filters stations based on the vehicle's current charge and distance.
            6. For each feasible station, calculates the total delay compared to the original route.
            7. Generates a list of charging options and returns them as a JSON string.

        Args:
            request_data (dict): A dictionary containing the routing request data.

        Returns:
            str: A JSON string containing a list of charging options for the request.
        """
        if request_data["uuid"] in cls._requests:
            cls._logger.warning(
                f"Duplicate request received: {request_data['uuid']}. Ignoring."
            )
            return "Duplicate request. This request has already been processed."

        request = Request.from_dict(request_data)
        cls._requests.add(request.uuid)
        cls._logger.info(
            f"Received new request: {request.uuid} for plate {request.plate} to destination {request.destination}"
        )

        if cls.check_active_bookings(request.plate):
            cls._logger.warning(
                f"Vehicle with plate {request.plate} already has an active booking. Cannot process request {request.uuid}."
            )
            return "Vehicle already has an active booking. Please complete or cancel the existing booking before making a new request."

        remaining_route, _, remaining_duration = ControlRoute.get_route_coords(
            request.position, request.destination
        )

        stations_in_area = cls.get_stations_in_area(remaining_route)

        vehicle = VehicleDAO.read_by_plate(request.plate)
        if not vehicle:
            cls._logger.error(
                f"Vehicle with plate {request.plate} not found in database. Cannot process request {request.uuid}."
            )
            return "Vehicle not found. Please register your vehicle before making a request."

        # Assuming a minimum percent of 20% for the vehicle to be able to reach a charging station
        max_distance = vehicle.distance_percent(request.current_percent, 20)

        options = []
        for s in stations_in_area:
            if "unknown" in s.operator.lower():
                # If the station name contains "unknown", we skip it.
                continue

            _, distance, duration = ControlRoute.get_route_coords(
                request.position, s.location
            )
            distance /= 1000

            # FILTERS UNFEASIBLE OPTIONS BASED ON DISTANCE AND VEHICLE CURRENT CHARGE
            if distance > max_distance:
                continue

            # Calculates the new route duration with the stop at the charging station
            # to calculate the delay compared to the original route without stops.
            source = request.position
            stop = s.location
            destination = request.destination
            route = [source, stop, destination]
            try:
                new_route_duration = ControlRoute.get_duration_list(route)
            except ValueError as e:
                cls._logger.error(
                    f"Error calculating new route duration for station {s.id}: {e}"
                )
                continue
            routing_delay_hours = (new_route_duration - remaining_duration) / 3600

            start_time = datetime.now() + timedelta(seconds=duration)

            new_percent = vehicle.percent_after_distance(
                request.current_percent, distance
            )

            av_speeds = set()
            for c in s.chargers:
                # For each charger in the station, calculates
                # the charging time and the total delay compared to the original route.
                if c.power_kw in av_speeds:
                    # If a charger from the same station has the same power,
                    # we skip it.
                    continue
                av_speeds.add(c.power_kw)

                # TODO: Charging to the 100% ?
                chg_hours = vehicle.charging_time(new_percent, 80, c.power_kw)

                o = Option(
                    request_id=request.uuid,
                    charging_station=s,
                    start_time=start_time,
                    charging_hours=chg_hours,
                    route_hours=duration / 3600,
                    kw_speed=c.power_kw,
                )
                o.delay_hours = routing_delay_hours + chg_hours

                options.append(o)

        cls._logger.info(
            f"{len(stations_in_area)} - {len(options)} = {len(stations_in_area) - len(options)} unfeasible stations based on distance and vehicle {request.plate}."
        )

        options.sort(
            key=lambda x: x.delay_hours,
            reverse=False,
        )
        options = options[:10]

        o_dicts = []
        for o in options:
            o.services_nearby = ServiceDAO.read_near_point(
                o.charging_station.location, 100
            )
            o_dicts.append(o.to_dict())
            cls._logger.debug(o.debug_str())

        o_json = json.dumps(o_dicts)
        cls._logger.info(f"Generated {len(options)} options for request {request.uuid}")

        return o_json

    @classmethod
    def get_stations_in_area(cls, remaining_route: list):
        """
        Gets the charging stations in the area of the remaining route.

        Args:
            remaining_route (list): A list of coordinates representing the remaining route.

        Returns:
            list: A list of charging stations in the area.
        """

        lats = [coord[0] for coord in remaining_route]
        lons = [coord[1] for coord in remaining_route]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        stations_in_area = charging_stationDAO.read_stations_in_area(
            min_lat, max_lat, min_lon, max_lon
        )
        cls._logger.info(
            f"Found {len(stations_in_area)} charging stations in the area."
        )

        return stations_in_area

    @classmethod
    def check_active_bookings(cls, plate: str) -> bool:
        """
        Checks if the vehicle with the given plate has any active bookings.

        Args:
            plate (str): The license plate of the vehicle.

        Returns:
            bool: True if there is an active booking for the vehicle, False otherwise.
        """

        active_booking = BookingDAO.read_active_by_vehicle_plate(plate)
        return active_booking is not None
