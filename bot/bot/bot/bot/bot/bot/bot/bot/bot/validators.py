"""Validation helpers for CLI order input."""

from decimal import Decimal, InvalidOperation
from typing import Optional

from bot.exceptions import ValidationError

BUY = "BUY"
SELL = "SELL"
MARKET = "MARKET"
LIMIT = "LIMIT"
VALID_SIDES = {BUY, SELL}
VALID_ORDER_TYPES = {MARKET, LIMIT}


def parse_positive_decimal(value: str, field_name: str) -> Decimal:
    """Parse a string into a positive Decimal value."""
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a valid number.") from exc

    if number <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")
    return number


def validate_order_input(
    symbol: Optional[str],
    side: Optional[str],
    order_type: Optional[str],
    quantity: Optional[str],
    price: Optional[str] = None,
) -> dict[str, str]:
    """Validate raw CLI values and return normalized order parameters."""
    if not symbol or not symbol.strip():
        raise ValidationError("symbol is required. Example: --symbol BTCUSDT")

    if not side or side.upper() not in VALID_SIDES:
        raise ValidationError("side must be BUY or SELL. Example: --side BUY")

    if not order_type or order_type.upper() not in VALID_ORDER_TYPES:
        raise ValidationError("type must be MARKET or LIMIT. Example: --type MARKET")

    if quantity is None:
        raise ValidationError("quantity is required. Example: --quantity 0.001")

    normalized_type = order_type.upper()
    normalized_price = None
    normalized_quantity = parse_positive_decimal(quantity, "quantity")

    if normalized_type == LIMIT:
        if price is None:
            raise ValidationError("LIMIT orders require price. Example: --price 110000")
        normalized_price = parse_positive_decimal(price, "price")

    if normalized_type == MARKET and price is not None:
        raise ValidationError("MARKET orders should not include price. Remove --price.")

    validated = {
        "symbol": symbol.strip().upper(),
        "side": side.upper(),
        "type": normalized_type,
        "quantity": format(normalized_quantity, "f"),
    }
    if normalized_price is not None:
        validated["price"] = format(normalized_price, "f")

    return validated
