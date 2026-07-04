import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, text, BIGINT, VARCHAR, FLOAT, DATE

from dags.src.transform import Transform

from datetime import datetime
import re





load_dotenv()

class LoadToDb:
    def __init__(self):
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.day = re.sub(r'[^0-9]','',str(datetime.today()))
        
    def config(self):
        self.engine = create_engine(f'postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}')
        print("Engine created")
        return self
    
    def create_table(self):
        with self.engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS  coin_etl;"))
            conn.execute(text(f"""CREATE TABLE IF NOT EXISTS coin_etl.crypto_coins_{self.day}
                             (
                             id VARCHAR(40),
                             name VARCHAR(40),
                             symbol VARCHAR(30),
                             rank INT,
                             total_supply BIGINT,
                             beta_value FLOAT,
                             first_data_at VARCHAR(50),
                             last_updated VARCHAR(50),
                             usd_price FLOAT,
                             usd_volume_24h FLOAT,
                             usd_market_cap BIGINT
                             )"""))
        print("Table structure ready")
            
    def load_data_to_db(self, df):
        df.to_sql(
            name=f"crypto_coins_{self.day}",
            con=self.engine,
            schema="coin_etl",
            if_exists="append",
            index=False
        )
