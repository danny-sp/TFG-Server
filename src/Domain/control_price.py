"""
Price calculation utilities for the system.
"""

from datetime import datetime
from typing import List, Tuple

import src.Persistance.web_client as WebClient
from src.Utils.logger import setup_logger

_logger = setup_logger("ControlPrice")


def get_price(start_date: datetime, end_date: datetime) -> List[float]:
    """
    Gets the energy price for the given date range.

    Args:
        start_date (datetime): The start date of the period.
        end_date (datetime): The end date of the period.

    Returns:
        List[float]: A list of energy prices (€/kWh) for each hour in the specified date range.
    """
    if start_date < datetime.now().replace(minute=0, second=0, microsecond=0):
        _logger.warning("Start date is in the past.")
        return [-1.0]

    if end_date <= start_date:
        _logger.warning("End date must be after start date.")
        return [-1.0]

    url = "https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "time_trunc": "hour",
    }

    data = WebClient.get_http(url, params)
    if data is None:
        _logger.error("Failed to retrieve price data.")
        return [-1.0]

    value = data["included"][0]["attributes"]["values"]

    return [hour["value"] / 1000 for hour in value]


def total_price(power_kw: float, pvpc_prices: List[float]) -> List[float]:
    """
    Adds a "realistic" margin to the PVPC price based on the power of the charger.

    Args:
        power_kw (float): The power of the charger in kW.
        pvpc_prices (List[float]): A list of PVPC prices for each hour.

    Returns:
        List[float]: A list of total prices for each hour, including the margin.
    """
    margin = 0.15 + (0.0009 * power_kw)
    margin = max(0.15, min(margin, 0.60))  # Clamping the margin between 0.15 and 0.60

    total_prices = [round(pvpc + margin, 3) for pvpc in pvpc_prices]
    return total_prices
