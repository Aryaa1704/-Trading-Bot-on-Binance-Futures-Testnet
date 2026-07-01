# -Trading-Bot-on-Binance-Futures-Testnet
Python CLI trading bot for Binance USDT-M Futures Testnet with Market &amp; Limit orders, BUY/SELL support, argparse CLI, input validation, structured logging, robust error handling, and modular architecture.
# Binance USDT-M Futures Testnet CLI Trading Bot

A clean, production-quality Python 3.11+ command line trading bot for placing **Market** and **Limit** orders on the **Binance USDT-M Futures Testnet**.

> Simple meaning: this project lets you type one command in your terminal to ask Binance Testnet to buy or sell a futures contract using fake testnet funds.

## Project Overview

This project is built like a small real backend application, not as a one-file script. Each file has one clear job:

| Simple idea | Technical name | Where it lives |
|---|---|---|
| Read your secret keys safely | Environment configuration | `bot/config.py` |
| Talk to Binance | API client wrapper | `bot/client.py` |
| Decide what kind of order to place | Business logic/service layer | `bot/orders.py` |
| Check your command before sending it | Input validation | `bot/validators.py` |
| Save what happened | File logging | `bot/logging_config.py` |
| Show nice terminal output | CLI and Rich formatting | `cli.py` |

## Features

- Supports Binance **USDT-M Futures Testnet**.
- Uses the official `python-binance` library.
- Loads API key and secret from `.env`; credentials are never hardcoded.
- Supports:
  - Market orders
  - Limit orders
  - BUY
  - SELL
- Validates CLI input with clear messages:
  - `--symbol` is required
  - `--side` must be `BUY` or `SELL`
  - `--type` must be `MARKET` or `LIMIT`
  - `--quantity` must be greater than `0`
  - `LIMIT` orders require `--price`
  - `MARKET` orders reject `--price`
- Creates `logs/` automatically.
- Logs requests, endpoints, parameters, responses, errors, and stack traces.
- Handles validation errors, Binance API errors, request errors, timeouts, invalid credentials, server errors, and unexpected errors without crashing.
- Uses `rich` for colored output and readable tables.

## Folder Structure

```text
trading_bot/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── cli.py
├── logs/
│   └── .gitkeep
└── bot/
    ├── __init__.py
    ├── client.py
    ├── orders.py
    ├── validators.py
    ├── logging_config.py
    ├── config.py
    ├── exceptions.py
    └── utils.py
```

## Installation

### 1. Open the project folder

```bash
cd trading_bot
```

If your folder has a different name, use that folder name instead.

### 2. Create a virtual environment

A virtual environment is like a separate toolbox for this project, so the project dependencies do not mix with other Python projects.

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Creating `.env`

Copy the example file:

```bash
cp .env.example .env
```

Then open `.env` and fill in your keys:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

## Getting Binance Testnet API Keys

1. Go to the Binance Futures Testnet website: <https://testnet.binancefuture.com>
2. Sign in or create a testnet account.
3. Create an API key and secret.
4. Put those values into your `.env` file.

Important: these keys are for the Binance **testnet**, not the real-money Binance exchange.

## Running Examples

### Market Order Example

A market order means: “Buy or sell now at the best available testnet price.”

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit Order Example

A limit order means: “Buy or sell only at my chosen price or better.”

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 110000
```

## CLI Arguments

| Argument | Required? | Example | Meaning |
|---|---:|---|---|
| `--symbol` | Yes | `BTCUSDT` | The trading pair |
| `--side` | Yes | `BUY` | Buy or sell |
| `--type` | Yes | `MARKET` | Market or limit order |
| `--quantity` | Yes | `0.001` | How much to buy or sell |
| `--price` | Only for LIMIT | `110000` | Your limit price |

## Output

When an order is placed, the bot prints two tables:

1. **Order Request** — what you asked the bot to send.
2. **Order Response** — what Binance replied.

You will see fields like:

- Order ID
- Status
- Executed Quantity
- Average Price
- Transaction Time

## Logs

Logs are saved in:

```text
logs/trading_bot.log
```

The bot logs:

- Timestamp
- Request endpoint
- Request parameters
- Binance response
- Errors
- Stack traces for exceptions

Simple meaning: if something goes wrong, this file is the “black box recorder” that helps you understand what happened.

## Error Handling

The bot catches and explains common problems:

- Missing `.env` values
- Invalid command input
- Binance API errors
- Binance request errors
- Network timeouts
- Invalid credentials
- Binance server errors
- Unexpected exceptions

The CLI prints friendly messages instead of scary Python tracebacks.

## Assumptions

- You are using Python 3.11 or newer.
- You are using Binance Futures Testnet credentials.
- You have enough testnet balance for the order you place.
- The symbol you choose exists on Binance USDT-M Futures Testnet.
- This project is for learning and hiring-assignment demonstration, not financial advice.

## Future Improvements

- Add stop-loss and take-profit orders.
- Add account balance display.
- Add open-order cancellation commands.
- Add order history lookup.
- Add automated tests with mocked Binance responses.
- Add Docker support.
- Add structured JSON logs for production observability.

## Beginner Glossary

| Word | Easy explanation |
|---|---|
| CLI | A tool you run by typing commands in the terminal |
| API | A way for two computer systems to talk to each other |
| Testnet | A practice version of Binance that does not use real money |
| Market order | Buy/sell immediately at the current available price |
| Limit order | Buy/sell only at a price you choose |
| `.env` file | A private file where your secret keys live |
| Dependency | A package this project needs to work |
| Log | A saved record of what the program did
