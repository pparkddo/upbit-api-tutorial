import api
from api import Client


def clear_console():
    import os
    command = "cls" if os.name in ("nt", "dos") else "clear"  # If Machine is running on Windows, use cls
    os.system(command)


def get_moving_average(prices, unit):
    if len(prices) < unit:
        return None
    return sum(prices[-unit:]) / unit


def my_awesome_trade_algorithm(current_price, moving_average):
    return current_price > moving_average


if __name__ == "__main__":
    import time

    access_key = input("access key 를 입력해주세요 : ")
    clear_console()

    secret_key = input("secret key 를 입력해주세요 : ")
    clear_console()

    for market in api.get_all_markets():
        print(market)

    client = Client(access_key, secret_key)

    while True:
        current_candle = api.get_minute_candles("KRW-DOGE", 1)[0]
        current_price = current_candle["trade_price"]

        unit = 5
        prices = list(reversed([candle["trade_price"] for candle in api.get_minute_candles("KRW-DOGE", 1, count=unit)]))
        moving_average = get_moving_average(prices, unit)
        print("moving_average:", moving_average)
        print(prices)

        if my_awesome_trade_algorithm(current_price, moving_average):
            print("sell")
            # print(client.sell("KRW-DOGE", 10, current_price, "limit"))
            # break
        else:
            print("hold...", "(current_price:", current_price, ")")

        time.sleep(60)
