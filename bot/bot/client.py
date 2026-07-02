"""Binance Futures client wrapper."""

import logging
from typing import Any

from binance.client import Client

from bot.config import Settings


class BinanceFuturesClient:
    """Thin wrapper around python-binance for USDT-M Futures API calls."""

    def __init__(self, settings: Settings, logger: logging.Logger) -> None:
        self._logger = logger
        self._client = Client(settings.api_key, settings.api_secret)
        self._client.FUTURES_URL = f"{settings.base_url}/fapi"

    def create_order(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Create a futures order using the Binance Futures endpoint."""
        endpoint = "POST /fapi/v1/order"
        self._logger.info(
            "request | endpoint=%s | parameters=%s",
            endpoint,
            _safe_parameters(parameters),
        )
        response = self._client.futures_create_order(**parameters)
        self._logger.info("response | endpoint=%s | response=%s", endpoint, response)
        return response


def _safe_parameters(parameters: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of request parameters safe for logs."""
    return dict(parameters)
