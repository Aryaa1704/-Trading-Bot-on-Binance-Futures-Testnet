"""Custom exceptions used by the trading bot."""


class TradingBotError(Exception):
    """Base exception for all user-facing trading bot errors."""


class ConfigurationError(TradingBotError):
    """Raised when required environment configuration is missing or invalid."""


class ValidationError(TradingBotError):
    """Raised when CLI input fails validation."""


class OrderPlacementError(TradingBotError):
    """Raised when an order cannot be placed successfully."""
