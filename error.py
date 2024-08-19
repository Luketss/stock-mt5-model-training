class OrderNotFulfilledError(Exception):
    """Raised when order is not executed"""

    def __init__(
        self, action: str, symbol: str, price: float, action_type: str, result
    ):
        super().__init__(
            f"Order not fullfilled execution price {price} on stock {symbol}. Action = {action} and Type = {action_type}, {result}"
        )
        self.action = action
        self.symbol = symbol
        self.price = price
        self.action_type = action_type
        self.result = result


class LoginError(Exception):
    """Raised when login is not possible"""

    def __init__(self, account: str, error):
        super().__init__(
            f"failed to connect to trade account {account} error code = {error}"
        )
        self.account = account


class SymbolNotFoundError(Exception):
    """Raised when symbol is not present in mt5 list"""

    def __init__(self, symbol: str):
        super().__init__(f"failed to find stock code {symbol}")
        self.symbol = symbol

class RatesError(Exception):
    """Raised when an issue was found wher trying to retrieve rates"""

    def __init__(self, symbol: str):
        super().__init__(f"failed to find rates for code {symbol}")
        self.symbol = symbol
