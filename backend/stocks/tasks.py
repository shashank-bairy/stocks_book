import os
import requests
import csv
import json
import redis
import pandas as pd
from datetime import datetime
from django.forms.models import model_to_dict
from django.conf import settings
from backend.settings import BASE_DIR, REDIS_HOST, REDIS_PORT
from .utils import download, unzip
from .models import Stock
from .redis_store import RedisStore

def get_bhav_copy():
    BSE_URL = 'https://www.bseindia.com/download/BhavCopy/Equity/'

    date = datetime.now().strftime("%d%m%Y")
    date = date[:4]+date[6:]
    
    # zip_file_name = f"EQ{date}_CSV.ZIP"
    zip_file_name = "EQ060421_CSV.ZIP"
    zip_file_path = os.path.join(BASE_DIR, 'data', zip_file_name)
    download_url = os.path.join(BSE_URL, zip_file_name)
    # download(download_url=download_url, file_path=zip_file_path)
    # unzip(file_path=zip_file_path)
    
    stocks = []
    unzip_file_name = f"EQ{date}.CSV"
    csv_file_name = "EQ060421.CSV"
    csv_file_path = os.path.join(BASE_DIR, 'data', csv_file_name)

    df = pd.read_csv(
        csv_file_path,
        usecols=["SC_CODE", "SC_NAME", "OPEN", "HIGH", "LOW", "CLOSE"]
    )
    df.columns = ["code", "name", "open", "high", "low", "close"]
    df['name'] = df['name'].str.strip()

    stocks = json.loads(df.to_json(orient='table'))["data"]

    rs = RedisStore(connection_pool=settings.REDIS_CONN_POOL)
    rs.delete_stock_data()
    rs.insert_stock_data(stocks)
            

    # print(stocks)


# def get_bhav_copy():
#     BSE_URL = 'https://www.bseindia.com/download/BhavCopy/Equity/'

#     date = datetime.now().strftime("%d%m%Y")
#     date = date[:4]+date[6:]
    
#     # zip_file_name = f"EQ{date}_CSV.ZIP"
#     zip_file_name = "EQ050421_CSV.ZIP"
#     zip_file_path = os.path.join(BASE_DIR, 'data', zip_file_name)
#     download_url = os.path.join(BSE_URL, zip_file_name)
#     # download(download_url=download_url, file_path=zip_file_path)
#     # unzip(file_path=zip_file_path)
    
#     stocks = []
#     unzip_file_name = f"EQ{date}.CSV"
#     csv_file_name = "EQ060421.CSV"
#     csv_file_path = os.path.join(BASE_DIR, 'data', csv_file_name)
#     df = pd.read_csv(csv_file_path)
#     stock_data = json.loads(df.to_json(orient='table'))["data"]

#     for stock in stock_data:
#         obj, created = Stock.objects.get_or_create(
#             code=stock['SC_CODE'],
#         )
#         obj.code = stock['SC_CODE']
#         obj.name = stock['SC_NAME'].strip()
#         obj.open = stock['OPEN']
#         obj.high = stock['HIGH']
#         obj.low = stock['LOW']
#         obj.close = stock['CLOSE']
#         obj.save()

#         stocks.append(model_to_dict(obj))

#     print(stocks)

if __name__ == '__main__':
    get_bhav_copy()