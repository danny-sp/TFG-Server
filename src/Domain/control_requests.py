from datetime import datetime, timedelta
import json

from src.Domain.control_route import ControlRoute

from src.Domain.bookingDAO import BookingDAO
from src.Domain.charging_stationDAO import ChargingStationDAO

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

        charging_station_dao = ChargingStationDAO()
        stations_in_area = charging_station_dao.read_stations_in_area(min_lat, max_lat, min_lon, max_lon)
        cls._logger.info(f"Found {len(stations_in_area)} charging stations in the area for request {request.uuid}")

        options = []
        o_dicts = []
        for s in stations_in_area:
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=7200)
            o = Option(request.uuid, s, None, None, start_time, end_time)
            options.append(o)
            o_dicts.append(o.to_dict())

        o_dicts.sort(key=lambda x: cls.calculate_delay(request, remaining_duration, x), reverse=True)

        o_dicts = o_dicts[:30]

        o_json = json.dumps(o_dicts)
        cls._logger.info(f"Generated {len(options)} options for request {request.uuid}")

        return o_json

    @classmethod
    def calculate_delay(cls, request: Request, remaining_duration: float, option: dict) -> float:
        source = request.position
        stop = option["charging_station"]["location"]
        destination = request.destination
        route = [source, stop, destination]

        charging_time = option["duration_hours"] * 3600

        try:
            new_duration = ControlRoute.get_duration_list(route) + charging_time
        except Exception as e:
            cls._logger.error(f"Error occurred while calculating duration for option {option['request_id']}: {e}")
            return float('inf')

        delay = new_duration - remaining_duration

        return max(delay, 0.0)

    @classmethod
    def check_active_bookings(cls, plate: str) -> bool:
        booking_dao = BookingDAO()
        active_booking = booking_dao.read_active_by_vehicle_plate(plate)
        return active_booking is not None
