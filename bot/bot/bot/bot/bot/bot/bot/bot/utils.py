"""Formatting helpers for CLI output."""

from datetime import datetime, timezone
from typing import Any


def milliseconds_to_utc_string(value: Any) -> str:
    """Convert Binance millisecond timestamp into a readable UTC string."""
    if not value:
        return "N/A"
    try:
        timestamp = int(value) / 1000
    except (TypeError, ValueError):
        return str(value)
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )


def calculate_average_price(response: dict[str, Any]) -> str:
    """Return the best available average execution price from an order response."""
    average_price = response.get("avgPrice")
    if average_price and str(average_price) != "0.00000":
        return str(average_price)

    cumulative_quote = _to_float(response.get("cumQuote"))
    executed_quantity = _to_float(response.get("executedQty"))
    if cumulative_quote and executed_quantity:
        return f"{cumulative_quote / executed_quantity:.8f}".rstrip("0").rstrip(".")

    return "N/A"


def _to_float(value: Any) -> float | None:
    """Convert a value to float when possible."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
