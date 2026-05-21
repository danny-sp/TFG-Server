"""
Price calculation utilities for the system.
"""

from datetime import datetime
from typing import List, Tuple

import src.Persistence.web_client as WebClient
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
    if power_kw <= 0:
        raise ValueError("Power must be greater than 0 kW.")

    if power_kw <= 22:
        margin_cents = 20.0
    elif power_kw <= 55:
        margin_cents = 0.606 * power_kw + 6.667
    elif power_kw <= 100:
        margin_cents = 0.111 * power_kw + 33.889
    elif power_kw <= 200:
        margin_cents = 0.1 * power_kw + 35.0
    else:
        margin_cents = 55.0

    margin = margin_cents / 100

    total_prices = [round(pvpc + margin, 3) for pvpc in pvpc_prices]
    return total_prices
