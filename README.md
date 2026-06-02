# 🤖 Binance Futures Testnet Trading Bot

A simplified CLI-based trading bot for Binance Futures Testnet (USDT-M), built with Python 3.x.
Supports Market, Limit, and Stop-Market orders with structured logging and robust error handling.

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance Futures Testnet API wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup (file + console)
├── logs/
│   └── trading_bot.log    # Auto-generated log file
├── cli.py                 # CLI entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/trading_bot.git
cd trading_bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API credentials
```bash
cp .env.example .env
```
Edit `.env` and add your Binance Futures Testnet API keys:
```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

> Get your testnet API keys from: https://testnet.binancefuture.com

---

## 🚀 How to Run

### Place a MARKET order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
```

### Place a STOP_MARKET order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 65000
```

---

## 📋 CLI Arguments

| Argument       | Required | Description                                      |
|----------------|----------|--------------------------------------------------|
| `--symbol`     | ✅ Yes   | Trading pair (e.g. `BTCUSDT`)                    |
| `--side`       | ✅ Yes   | `BUY` or `SELL`                                  |
| `--type`       | ✅ Yes   | `MARKET`, `LIMIT`, or `STOP_MARKET`              |
| `--quantity`   | ✅ Yes   | Order quantity (e.g. `0.001`)                    |
| `--price`      | ❌ No*   | Limit price — required for `LIMIT` orders        |
| `--stop-price` | ❌ No*   | Stop price — required for `STOP_MARKET` orders   |

---

## 📊 Sample Output

```
🤖 Binance Futures Testnet Trading Bot
========================================

📋 Order Request Summary
   Symbol   : BTCUSDT
   Side     : BUY
   Type     : MARKET
   Quantity : 0.001

✅ Order Placed Successfully!
   Order ID     : 4085209520
   Symbol       : BTCUSDT
   Side         : BUY
   Type         : MARKET
   Status       : FILLED
   Executed Qty : 0.001
   Avg Price    : 67842.30
```

---

## 📝 Logging

All requests, responses, and errors are automatically logged to `logs/trading_bot.log`.

Log format:
```
YYYY-MM-DD HH:MM:SS | LEVEL | module | message
```

---

## ✅ Features

- ✅ Place MARKET and LIMIT orders (USDT-M Futures Testnet)
- ✅ Bonus: STOP_MARKET order support
- ✅ CLI interface with argparse
- ✅ Input validation with clear error messages
- ✅ Structured logging to file + console
- ✅ Exception handling (invalid input, API errors, network failures)
- ✅ Separate client/API layer and CLI layer
- ✅ `.env` based credentials (never hardcoded)

---

## ⚠️ Assumptions

- This bot targets the **Binance Futures Testnet** only (`testnet.binancefuture.com`)
- Minimum quantity for BTCUSDT futures is `0.001`
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled) by default
- API keys must have **Futures trading** permissions enabled on testnet

---

## 🔒 Security Note

Never commit your `.env` file. It is listed in `.gitignore` by default.
