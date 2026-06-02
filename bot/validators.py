"""
validators.py — Input validation for order parameters.
"""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of: {VALID_SIDES}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be one of: {VALID_ORDER_TYPES}")
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")
    return quantity


def validate_price(price: float, order_type: str) -> float:
    if order_type == "LIMIT" and price <= 0:
        raise ValueError(f"Price must be greater than 0 for LIMIT orders. Got: {price}")
    return price


def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    return symbol
