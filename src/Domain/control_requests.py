from datetime import datetime, timedelta
import json

from src.Domain.control_route import ControlRoute

import src.Domain.bookingDAO as BookingDAO
import src.Domain.chargerDAO as chargerDAO
import src.Domain.charging_stationDAO as charging_stationDAO
import src.Domain.serviceDAO as ServiceDAO
import src.Domain.vehicleDAO as VehicleDAO

from src.Domain.option import Option
from src.Domain.request import Request

from src.Utils.logger import setup_logger

class ControlRequests:
    _requests = set()

    _logger = setup_logger("ControlRequests")

    @classmethod
    def process_request(cls, request_data: dict):
        if request_data["uuid"] in cls._requests:
            cls._logger.warning(f"Duplicate request received: {request_data['uuid']}. Ignoring.")
            return "Duplicate request. This request has already been processed."

        request = Request.from_dict(request_data)
        cls._requests.add(request.uuid)
        cls._logger.info(f"Received new request: {request.uuid} for plate {request.plate} to destination {request.destination}")

        if cls.check_active_bookings(request.plate):
            cls._logger.warning(f"Vehicle with plate {request.plate} already has an active booking. Cannot process request {request.uuid}.")
            return "Vehicle already has an active booking. Please complete or cancel the existing booking before making a new request."

        remaining_route, remaining_distance, remaining_duration = ControlRoute.get_route_coords(request.position, request.destination)
        lats = [coord[0] for coord in remaining_route]
        lons = [coord[1] for coord in remaining_route]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        stations_in_area = charging_stationDAO.read_stations_in_area(min_lat, max_lat, min_lon, max_lon)
        cls._logger.info(f"Found {len(stations_in_area)} charging stations in the area for request {request.uuid}")

        vehicle = VehicleDAO.read_by_plate(request.plate)
        vehicle.current_percent = request.current_percent
        if not vehicle:
            cls._logger.error(f"Vehicle with plate {request.plate} not found in database. Cannot process request {request.uuid}.")
            return "Vehicle not found. Please register your vehicle before making a request."

        # Assuming a minimum percent of 20% for the vehicle to be able to reach a charging station
        max_distance = vehicle.distance_percent(20)

        options = []
        for s in stations_in_area:
            vehicle.current_percent = request.current_percent

            _, distance, duration = ControlRoute.get_route_coords(request.position, s.location)
            distance /= 1000

            # FILTERS UNFEASIBLE OPTIONS BASED ON DISTANCE AND VEHICLE CURRENT CHARGE
            if distance > max_distance:
                continue

            start_time = datetime.now() + timedelta(seconds=duration)

            s.chargers = chargerDAO.read_by_station(s)
            vehicle.current_percent = vehicle.percent_after_distance(distance)

            av_speeds = set()
            for c in s.chargers:
                if c.power_kw in av_speeds:
                    continue
                av_speeds.add(c.power_kw)
                # TODO: Charging to the 100% ?
                chg_hours = vehicle.charging_time(80, c.power_kw)

            o = Option(request_id=request.uuid,
                       charging_station=s,
                       price_rate=None,
                       start_time=start_time,
                       duration_hours=chg_hours,
                       kw_speed=c.power_kw)

            options.append(o)
        cls._logger.info(f"{len(stations_in_area)} - {len(options)} = {len(stations_in_area) - len(options)} unfeasible stations based on distance and vehicle {request.plate}.")

        o_dicts = []

        options.sort(key=lambda x: cls.calculate_delay(request, remaining_duration, x), reverse=False)
        options = options[:10]

        for o in options:
            o.services_nearby = ServiceDAO.read_near_point(o.charging_station.location, 100)
            o_dicts.append(o.to_dict())

        o_json = json.dumps(o_dicts)
        cls._logger.info(f"Generated {len(options)} options for request {request.uuid}")

        return o_json

    @classmethod
    def calculate_delay(cls, request: Request, remaining_duration: float, option: Option) -> float:
        source = request.position
        stop = option.charging_station.location
        destination = request.destination
        route = [source, stop, destination]

        charging_time = option.duration_hours * 3600

        try:
            new_duration = ControlRoute.get_duration_list(route) + charging_time
        except Exception as e:
            cls._logger.error(f"Error occurred while calculating duration for option {option.request_id}: {e}")
            return float('inf')

        delay = new_duration - remaining_duration
        option.delay_hours = delay / 3600

        return max(delay, 0.0)

    @classmethod
    def check_active_bookings(cls, plate: str) -> bool:
        active_booking = BookingDAO.read_active_by_vehicle_plate(plate)
        return active_booking is not None
