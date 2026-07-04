# import python libraries


import pandas as pd
from datetime import datetime
import requests


# create data extraction class and methods

class DataExtraction:
    def __init__(self,url):
        self.url = url



# inherite from DataExtration class


class FetchData(DataExtraction):
    def fetchdata(self):
        print("fetching data ...")
        self.response = requests.get(self.url)
        self.data = self.response.json()
        print("Raw json data fetched")
        return self.data
    
    def to_data_frame(self):
        self.df_all = pd.json_normalize(self.data)
        print("Raw data df has been created")
        return self.df_all
