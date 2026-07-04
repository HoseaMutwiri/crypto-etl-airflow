from dags.src.extract import FetchData
from datetime import datetime

class Transform:
    def __init__(self,coins):
        self.coins = coins
    
    def transform(self,data):
        self.df_filtered = data[data["id"].isin(self.coins.keys())]
        self.filtered_columns =['id', 'name', 'symbol', 'rank', 'total_supply',
                    'beta_value', 'first_data_at', 'last_updated',
                    'quotes.USD.price','quotes.USD.volume_24h','quotes.USD.market_cap']
        self.df_filtered = self.df_filtered[self.filtered_columns]
        self.df_filtered = self.df_filtered.rename(columns = {
            'quotes.USD.price':'usd_price',
            'quotes.USD.volume_24h':'usd_volume_24h',
            'quotes.USD.market_cap':'usd_market_cap'
        })
        print("Data has been cleaned now ready for load")
        return self.df_filtered
