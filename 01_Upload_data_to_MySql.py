
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus


df = pd.read_csv('train.csv') # 1. CSV read karega

# 2. Column names ke spaces ko underscore (_) se replace karta hai taaki MySQL mein dikkat na ho
df.columns = [c.replace(' ', '_').replace('-', '_') for c in df.columns]

user = 'root'
row_password = 'YOUR_MYSQL_PASSWORD'      
host = 'localhost'
port = '3306'
db_name = 'data_analysis'   
password=quote_plus(row_password) 
# Connection create karta hai
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}")

# MySQL table mein upload karne per (chunksize se fast aur safe upload hota hai) yada data ko tokdo me upload karta hai
df.to_sql('sales_data', con=engine, if_exists='replace', index=False, chunksize=1000)

print(f"Success! Pure {len(df)} rows MySQL me upload ho gaye.")