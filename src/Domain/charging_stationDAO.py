
from src.Domain.charging_station import ChargingStation

from src.Persistance.db_broker import DBBroker

def insert(charging_station: ChargingStation) -> int:
    query = """
    INSERT INTO charging_stations (station_name, operator, location)
    VALUES (?, ?, ST_GeomFromText(?))
    """
    params = (
        charging_station.name,
        charging_station.operator,
        f"POINT({charging_station.longitude} {charging_station.latitude})"
    )
    db = DBBroker()
    _, inserted_id = db.execute_write_query(query, params)
    return inserted_id

def update(charging_station: ChargingStation) -> None:
    query = """
    UPDATE charging_stations
    SET station_name = ?, operator = ?, location = ST_GeomFromText(?)
    WHERE id = ?
    """
    params = (
        charging_station.name,
        charging_station.operator,
        f"POINT({charging_station.longitude} {charging_station.latitude})",
        charging_station.id
    )
    db = DBBroker()
    return db.execute_write_query(query, params)

def delete(charging_station: ChargingStation) -> None:
    query = "DELETE FROM charging_stations WHERE id = ?"
    params = (charging_station.id,)
    db = DBBroker()
    return db.execute_write_query(query, params)

def read_stations_in_area(min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> list[ChargingStation]:
    polygon_wkt = f"POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, {max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))"

    query = """
        SELECT cs.id, cs.station_name, o.operator_name as operator, 
                ST_Y(cs.location) as latitude, 
                ST_X(cs.location) as longitude
        FROM charging_stations cs, operators o
        WHERE o.id = cs.operator_id AND MBRContains(
            ST_GeomFromText(?),
            cs.location
        )
        """

    params = (polygon_wkt,)
    db = DBBroker()
    rows = db.execute_read_query(query, params)
    return [_row_to_charging_station(row) for row in rows]

def read_by_id(station_id: int) -> ChargingStation:
    query = """
    SELECT cs.id, cs.station_name, o.operator_name as operator, 
            ST_Y(cs.location) as latitude, 
            ST_X(cs.location) as longitude
    FROM charging_stations cs, operators o
    WHERE o.id = cs.operator_id AND cs.id = ?
    """
    db = DBBroker()
    rows = db.execute_read_query(query, (station_id,))
    return _row_to_charging_station(rows[0]) if rows else None

def _row_to_charging_station(row) -> ChargingStation:
    return ChargingStation(
        id=row["id"],
        name=row["station_name"],
        operator=row["operator"],
        location=(row["latitude"], row["longitude"]),
    )
