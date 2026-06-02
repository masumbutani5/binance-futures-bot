"""
cli.py — Command-line interface for the Binance Futures Trading Bot.

Usage examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 95000
  python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 90000
"""

import argparse
import os
import sys
from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.orders import place_order
from bot.logging_config import get_logger

load_dotenv()
logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Market BUY:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  Limit SELL:
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 95000

  Stop Market SELL (Bonus):
    python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 90000
        """
    )
    parser.add_argument("--symbol",     type=str,   required=True,  help="Trading pair (e.g. BTCUSDT)")
    parser.add_argument("--side",       type=str,   required=True,  help="BUY or SELL")
    parser.add_argument("--type",       type=str,   required=True,  help="MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--quantity",   type=float, required=True,  help="Order quantity")
    parser.add_argument("--price",      type=float, required=False, help="Price (required for LIMIT orders)")
    parser.add_argument("--stop-price", type=float, required=False, help="Stop price (required for STOP_MARKET orders)")
    return parser.parse_args()


def main():
    args = parse_args()

    # Load API credentials from environment
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("\n❌ ERROR: API credentials not found.")
        print("   Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.\n")
        logger.error("Missing API credentials in environment variables.")
        sys.exit(1)

    print(f"\n🤖 Binance Futures Testnet Trading Bot")
    print(f"{'=' * 40}")

    # Initialize client
    client = BinanceClient(api_key=api_key, api_secret=api_secret)

    # Place the order
    try:
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )
        logger.info("Order process completed successfully.")
    except ValueError as e:
        print(f"\n❌ Validation Error: {e}\n")
        logger.error(f"Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
