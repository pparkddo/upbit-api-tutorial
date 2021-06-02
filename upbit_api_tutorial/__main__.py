import api
from api import Client


def clear_console():
    import os
    command = "cls" if os.name in ("nt", "dos") else "clear"  # If Machine is running on Windows, use cls
    os.system(command)


if __name__ == "__main__":
    access_key = input("access key 를 입력해주세요 : ")
    clear_console()

    secret_key = input("secret key 를 입력해주세요 : ")
    clear_console()

    print(api.get_all_markets())
    print(api.get_minute_candles("KRW-DOT", 1))

    client = Client(access_key, secret_key)
    print(client.get_order_chance("KRW-ETH"))