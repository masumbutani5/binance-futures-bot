"""
orders.py — Order placement logic for Binance Futures Testnet.
Supports MARKET, LIMIT, and STOP_MARKET orders.
"""

from bot.client import BinanceClient
from bot.validators import validate_side, validate_order_type, validate_quantity, validate_price, validate_symbol
from bot.logging_config import get_logger

logger = get_logger(__name__)

ORDER_ENDPOINT = "/fapi/v1/order"


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    stop_price: float = None
) -> dict:
    """
    Place a futures order on Binance Testnet.

    Args:
        client: BinanceClient instance
        symbol: Trading pair e.g. BTCUSDT
        side: BUY or SELL
        order_type: MARKET, LIMIT, or STOP_MARKET
        quantity: Amount to trade
        price: Required for LIMIT orders
        stop_price: Required for STOP_MARKET orders

    Returns:
        dict: Order response from Binance API
    """
    # Validate inputs
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)

    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        price = validate_price(price, order_type)
        params["price"] = price
        params["timeInForce"] = "GTC"

    if order_type == "STOP_MARKET":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders.")
        params["stopPrice"] = stop_price

    # Log the order request summary
    logger.info("=" * 50)
    logger.info("ORDER REQUEST SUMMARY")
    logger.info(f"  Symbol     : {symbol}")
    logger.info(f"  Side       : {side}")
    logger.info(f"  Type       : {order_type}")
    logger.info(f"  Quantity   : {quantity}")
    if price:
        logger.info(f"  Price      : {price}")
    if stop_price:
        logger.info(f"  Stop Price : {stop_price}")
    logger.info("=" * 50)

    print(f"\n📋 Order Request Summary")
    print(f"   Symbol   : {symbol}")
    print(f"   Side     : {side}")
    print(f"   Type     : {order_type}")
    print(f"   Quantity : {quantity}")
    if price:
        print(f"   Price    : {price}")

    # Place the order
    try:
        response = client.post(ORDER_ENDPOINT, params=params)
        _log_order_response(response)
        return response
    except Exception as e:
        logger.error(f"Order placement FAILED: {e}")
        print(f"\n❌ Order FAILED: {e}")
        raise


def _log_order_response(response: dict):
    """Log and print a clean order response."""
    order_id = response.get("orderId", "N/A")
    status = response.get("status", "N/A")
    executed_qty = response.get("executedQty", "N/A")
    avg_price = response.get("avgPrice", "N/A")
    symbol = response.get("symbol", "N/A")
    side = response.get("side", "N/A")
    order_type = response.get("type", "N/A")

    logger.info("ORDER RESPONSE")
    logger.info(f"  Order ID     : {order_id}")
    logger.info(f"  Status       : {status}")
    logger.info(f"  Executed Qty : {executed_qty}")
    logger.info(f"  Avg Price    : {avg_price}")

    print(f"\n✅ Order Placed Successfully!")
    print(f"   Order ID     : {order_id}")
    print(f"   Symbol       : {symbol}")
    print(f"   Side         : {side}")
    print(f"   Type         : {order_type}")
    print(f"   Status       : {status}")
    print(f"   Executed Qty : {executed_qty}")
    print(f"   Avg Price    : {avg_price}\n")
