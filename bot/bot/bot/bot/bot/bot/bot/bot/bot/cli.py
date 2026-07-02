"""Command line interface for the Binance Futures Testnet trading bot."""

import argparse
import sys
from typing import Any

import requests
from binance.exceptions import BinanceAPIException, BinanceRequestException
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bot.client import BinanceFuturesClient
from bot.config import load_settings
from bot.exceptions import ConfigurationError, TradingBotError, ValidationError
from bot.logging_config import configure_logging
from bot.orders import OrderService
from bot.utils import calculate_average_price, milliseconds_to_utc_string
from bot.validators import validate_order_input

console = Console()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Place BUY and SELL orders on Binance USDT-M Futures Testnet."
    )
    parser.add_argument("--symbol", help="Trading pair symbol, for example BTCUSDT")
    parser.add_argument("--side", help="Order side: BUY or SELL")
    parser.add_argument("--type", help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", help="Order quantity, for example 0.001")
    parser.add_argument("--price", help="Limit order price. Not allowed for MARKET orders")
    return parser


def print_order_request(order: dict[str, str]) -> None:
    """Print a formatted order request table."""
    table = Table(title="Order Request", show_header=True, header_style="bold cyan")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("Symbol", order["symbol"])
    table.add_row("Side", order["side"])
    table.add_row("Type", order["type"])
    table.add_row("Quantity", order["quantity"])
    table.add_row("Price", order.get("price", "N/A"))
    console.print(table)


def print_order_response(response: dict[str, Any]) -> None:
    """Print a formatted order response table."""
    table = Table(title="Order Response", show_header=True, header_style="bold green")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("Order ID", str(response.get("orderId", "N/A")))
    table.add_row("Status", str(response.get("status", "N/A")))
    table.add_row("Executed Quantity", str(response.get("executedQty", "N/A")))
    table.add_row("Average Price", calculate_average_price(response))
    table.add_row(
        "Transaction Time",
        milliseconds_to_utc_string(response.get("updateTime") or response.get("transactTime")),
    )
    console.print(table)


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(Panel(message, title="Success", style="bold green"))


def print_failure(message: str) -> None:
    """Print a failure message."""
    console.print(Panel(message, title="Failure", style="bold red"))


def user_friendly_error(error: Exception) -> str:
    """Map low-level exceptions to safe messages for CLI users."""
    if isinstance(error, BinanceAPIException):
        if error.status_code in {401, 403}:
            return "Binance rejected the request. Please check your API key and secret."
        if 500 <= error.status_code <= 599:
            return "Binance server error. Please try again later."
        return f"Binance API error: {error.message}"

    if isinstance(error, BinanceRequestException):
        return "Could not reach Binance. Please check your internet connection and try again."

    if isinstance(error, requests.exceptions.Timeout):
        return "The network request timed out. Please try again."

    if isinstance(error, requests.exceptions.RequestException):
        return "Network error while contacting Binance. Please try again."

    if isinstance(error, TradingBotError):
        return str(error)

    return "Unexpected error. Please check logs/trading_bot.log for details."


def main() -> int:
    """Run the trading bot CLI."""
    logger = configure_logging()
    parser = build_parser()
    args = parser.parse_args()

    try:
        order = validate_order_input(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )
        settings = load_settings()
        client = BinanceFuturesClient(settings=settings, logger=logger)
        service = OrderService(client=client, logger=logger)

        console.rule("[bold cyan]Order Request")
        print_order_request(order)
        response = service.place_order(order)
        console.rule("[bold green]Order Response")
        print_order_response(response)
        print_success("Order placed successfully on Binance Futures Testnet.")
        return 0

    except (ValidationError, ConfigurationError) as exc:
        logger.error("user_error | error=%s", exc)
        print_failure(user_friendly_error(exc))
        return 2
    except (
        BinanceAPIException,
        BinanceRequestException,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException,
    ) as exc:
        logger.exception("binance_or_network_error")
        print_failure(user_friendly_error(exc))
        return 1
    except Exception as exc:  # noqa: BLE001 - CLI must never expose a traceback to users.
        logger.exception("unexpected_error")
        print_failure(user_friendly_error(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
