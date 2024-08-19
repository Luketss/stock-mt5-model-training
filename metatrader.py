from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

from error import OrderNotFulfilledError, LoginError, SymbolNotFoundError, RatesError
from setup import USER, PASSWORD
from utils import transform_data

time_rates = {
    1: mt5.TIMEFRAME_M1,
    2: mt5.TIMEFRAME_M2,
    3: mt5.TIMEFRAME_M3,
    10: mt5.TIMEFRAME_M10,
    15: mt5.TIMEFRAME_M15,
    30: mt5.TIMEFRAME_M30,
    60: mt5.TIMEFRAME_H1,
}


class Metatrader:
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    def __init__(self, user, password, server="XPMT5-DEMO"):
        self.user = user
        self.password = password
        self.server = server
        self.authorized = mt5.login(
            self.user, password=self.password, server=self.server
        )

    def send_order(self):
        pass

    def get_account_info(self):
        if self.authorized:
            account_info = mt5.account_info()
            if account_info != None:
                print(account_info)
                print("Show account_info()._asdict():")
                account_info_dict = mt5.account_info()._asdict()
                for prop in account_info_dict:
                    print(f"  {prop}={account_info_dict[prop]}")
        else:
            raise LoginError(self.user, mt5.last_error())

    def buy_stock(self, symbol, lot=500.0, deviation=2):
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol, True):
                print("symbol_select({}}) failed, exit", symbol)
                mt5.shutdown()
                quit()
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "magic": 234000,
            "comment": "python script buy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        print(request)
        result = mt5.order_send(request)
        print(
            f"1. order_send(): by {symbol} {lot} lots at {price} with deviation={deviation} points"
        )
        print("2. order_send done, ", result)

    def sell_stock(self, symbol, lot=500.0, deviation=2):
        point = mt5.symbol_info(symbol).point
        price = mt5.symbol_info_tick(symbol).ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "magic": 234000,
            "comment": "python script sell",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        result = mt5.order_send(request)
        print(
            f"1. order_send(): by {symbol} {lot} lots at {price} with deviation={deviation} points"
        )
        print("2. order_send done, ", result)

    def get_symbol_info(self, stock_code: str):
        symbol_info = mt5.symbol_info(stock_code)
        print(symbol_info)
        if symbol_info != None:
            return symbol_info
        raise SymbolNotFoundError(stock_code)

    def show_positions(self):
        positions_total = mt5.positions_total()
        if positions_total > 0:
            return f"Total positions={positions_total}"
        else:
            return "Positions not found"

    def copy_rates(
        self,
        stock_code: str,
        utc_from_date,
        timeframe=time_rates.get(1),
        number_of_rates: int = 10000,
        write_csv_file: bool = True,
    ):
        utc_from_dt = transform_data(utc_from_date)
        rates = mt5.copy_rates_from(stock_code, timeframe, utc_from_dt, number_of_rates)
        print(rates)
        if rates is not None:
            rates_frame = pd.DataFrame(rates)
            rates_frame = rates_frame.rename_axis("index")
            print(rates_frame)
            # convert time in seconds into the datetime format
            rates_frame["time"] = pd.to_datetime(rates_frame["time"], unit="s")

            if write_csv_file:
                self.write_csv_file_with_results(rates_frame, stock_code)
            return rates_frame
        raise RatesError(stock_code)

    def copy_rates_from_range_date(
        self,
        stock_code: str,
        utc_from_date,
        utc_to_date,
        timeframe=time_rates.get(1),
        write_csv_file: bool = True,
        file_name_constructor="",
    ):
        rates = mt5.copy_rates_range(stock_code, timeframe, utc_from_date, utc_to_date)
        if rates is not None:
            rates_frame = pd.DataFrame(rates)
            rates_frame = rates_frame.rename_axis("index")
            # convert time in seconds into the datetime format
            rates_frame["time"] = pd.to_datetime(rates_frame["time"], unit="s")

            if write_csv_file:
                self.write_csv_file_with_results(
                    rates_frame, f"{file_name_constructor}-{stock_code}"
                )
            return rates_frame
        raise RatesError(stock_code)

    def get_ticks_from_range(self, stock_code, utc_from_date, utc_to_date):
        utc_from_dt = transform_data(utc_from_date)
        utc_to_dt = transform_data(utc_to_date)

        ticks = mt5.copy_ticks_range(
            stock_code, utc_from_dt, utc_to_dt, mt5.COPY_TICKS_ALL
        )
        print("Ticks received:", len(ticks))
        ticks_frame = pd.DataFrame(ticks)
        # convert time in seconds into the datetime format
        ticks_frame["time"] = pd.to_datetime(ticks_frame["time"], unit="s")

        # display data
        print("\nDisplay dataframe with ticks")
        print(ticks_frame.head(10))

    def write_csv_file_with_results(self, df, file_name):
        df.to_csv(f"{file_name}.csv")

    def shutdown(self):
        mt5.shutdown()


if __name__ == "__main__":
    mt = Metatrader(USER, PASSWORD)
    # df = mt.copy_rates("ODPV3", "2024-06-07 19:00:00", 10000)
    mt.shutdown()
