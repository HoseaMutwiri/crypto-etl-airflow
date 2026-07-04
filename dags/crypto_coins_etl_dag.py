

from airflow.sdk import dag, task

from datetime import datetime,timedelta


COINS = {
    "btc-bitcoin": "Bitcoin",
    "eth-ethereum": "Ethereum",
    "usdt-tether": "Tether",
    "usdc-usd-coin": "USD Coin",
    "sol-solana": "Solana",
}

DATA_URL = "https://api.coinpaprika.com/v1/tickers"


@dag(
    dag_id="pipeline_coins",
    start_date=datetime(2026, 6, 29),
    schedule="@daily",
    max_active_runs=1,
    default_args={"owner": "Hosea Mutwiri", "retries": 3},
    tags=["coin", "etl","crypto_assignment"],
    catchup=False,
)
def pipeline():

    @task()
    def extract_task():
        from src.extract import FetchData

        fetcher = FetchData(DATA_URL)
        fetcher.fetchdata()
        df = fetcher.to_data_frame()
        return df.to_dict(orient="records")

    @task()
    def transform_task(raw_data_dict):
        import pandas as pd
        from src.transform import Transform
        raw_df = pd.DataFrame(raw_data_dict)
        transformer = Transform(COINS)
        transformed_df = transformer.transform(raw_df)
        return transformed_df.to_dict(orient="records")

    @task()
    def load_task(transformed_data_dict):
        import pandas as pd
        from src.load import LoadToDb
        transformed_df = pd.DataFrame(transformed_data_dict)
        loader = LoadToDb()
        loader.config()
        loader.create_table()
        loader.load_data_to_db(transformed_df)
        print("The pipeline finished END-END")

    raw_data = extract_task()
    transformed_data = transform_task(raw_data)
    load_task(transformed_data)


pipeline()
