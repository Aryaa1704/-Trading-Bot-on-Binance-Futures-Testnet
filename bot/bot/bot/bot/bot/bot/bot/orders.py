"""Business logic for placing Binance Futures orders."""

import logging
from typing import Any

from bot.client import BinanceFuturesClient
from bot.validators import LIMIT, MARKET

TIME_IN_FORCE_GTC = "GTC"


class OrderService:
    """Order orchestration service for market and limit orders."""

    def __init__(self, client: BinanceFuturesClient, logger: logging.Logger) -> None:
        self._client = client
        self._logger = logger

    def place_order(self, order: dict[str, str]) -> dict[str, Any]:
        """Place a validated market or limit order."""
        if order["type"] == MARKET:
            return self.place_market_order(order)
        if order["type"] == LIMIT:
            return self.place_limit_order(order)
        raise ValueError(f"Unsupported order type: {order['type']}")

    def place_market_order(self, order: dict[str, str]) -> dict[str, Any]:
        """Place a market order."""
        parameters = {
            "symbol": order["symbol"],
            "side": order["side"],
            "type": MARKET,
            "quantity": order["quantity"],
        }
        self._logger.info("placing_market_order | parameters=%s", parameters)
        return self._client.create_order(parameters)

    def place_limit_order(self, order: dict[str, str]) -> dict[str, Any]:
        """Place a limit order using Good-Til-Canceled time in force."""
        parameters = {
            "symbol": order["symbol"],
            "side": order["side"],
            "type": LIMIT,
            "timeInForce": TIME_IN_FORCE_GTC,
            "quantity": order["quantity"],
            "price": order["price"],
        }
        self._logger.info("placing_limit_order | parameters=%s", parameters)
        return self._client.create_order(parameters)
