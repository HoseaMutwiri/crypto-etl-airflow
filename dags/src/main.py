from dags.src.extract import FetchData

from dags.src.transform import Transform

from dags.src.load import LoadToDb


'''COINS = {
    "btc-bitcoin": "Bitcoin",
    "eth-ethereum": "Ethereum",
    "usdt-tether": "Tether",
    "usdc-usd-coin": "USD Coin",
    "sol-solana": "Solana"}'''

def main():
    COINS = {
    "btc-bitcoin": "Bitcoin",
    "eth-ethereum": "Ethereum",
    "usdt-tether": "Tether",
    "usdc-usd-coin": "USD Coin",
    "sol-solana": "Solana"}

    dataurl= "https://api.coinpaprika.com/v1/tickers"

    fetcher = FetchData(dataurl)

    fetcher.fetchdata()

    raw_data = fetcher.to_data_frame()

    transformer = Transform(COINS)
    transforemed_data = transformer.transform(raw_data)
    loader = LoadToDb()
    loader.config()
    loader.create_table()
    loader.load_data_to_db(transforemed_data)
    print("The pipeline finished END-END")




if __name__ == "__main__":

    main()