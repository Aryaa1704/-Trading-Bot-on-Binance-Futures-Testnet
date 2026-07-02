"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from bot.exceptions import ConfigurationError

DEFAULT_BASE_URL = "https://testnet.binancefuture.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


@dataclass(frozen=True)
class Settings:
    """Runtime settings required to communicate with Binance Futures Testnet."""

    api_key: str
    api_secret: str
    base_url: str = DEFAULT_BASE_URL


def load_settings() -> Settings:
    """Load Binance settings from a local .env file or process environment."""
    load_dotenv(ENV_FILE)

    api_key = getenv("BINANCE_API_KEY", "").strip()
    api_secret = getenv("BINANCE_API_SECRET", "").strip()
    base_url = getenv("BINANCE_BASE_URL", DEFAULT_BASE_URL).strip().rstrip("/")

    missing_fields = []
    if not api_key:
        missing_fields.append("BINANCE_API_KEY")
    if not api_secret:
        missing_fields.append("BINANCE_API_SECRET")

    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ConfigurationError(
            f"Missing required environment value(s): {fields}. "
            "Create a .env file from .env.example and add your Binance Testnet keys."
        )

    return Settings(api_key=api_key, api_secret=api_secret, base_url=base_url)
