import os
from zipfile import BadZipFile
from celery import shared_task
from django.conf import settings

from .utils import download, unzip, get_date_IST, get_csv_data
from .redis_store import RedisStore


@shared_task
def get_bhav_copy():
    """
    Function used to get Bhavcopy from BSE website, unzip it, extract CSV file and insert
    it's contents into Redis.
    """
    BSE_URL = 'https://www.bseindia.com/download/BhavCopy/Equity/'

    # Get date according to Indian Standard Time
    date = get_date_IST()

    zip_file_name = f"EQ{date}_CSV.ZIP"
    zip_file_path = os.path.join(settings.BASE_DIR, 'data', zip_file_name)
    csv_file_name = f"EQ{date}.CSV"
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', csv_file_name)
    
    download_url = os.path.join(BSE_URL, zip_file_name)
    
    # Download the zip file from BSE website
    download(download_url=download_url, file_path=zip_file_path)

    # Handles BadZipFile exception thrown when Bhavcopy is not uploaded on that particular day 
    try:
        # Unzip downloaded file
        unzip(file_path=zip_file_path)
    except BadZipFile:
        print('Bhavcopy was not uploaded today.')
        return
    finally:
        # Remove the zip file downloaded
        os.remove(zip_file_path)

    # Read data from downloaded CSV file
    stocks = get_csv_data(
        csv_file_path=csv_file_path,
        usecols=["SC_CODE", "SC_NAME", "OPEN", "HIGH", "LOW", "CLOSE"],
        columns=["code", "name", "open", "high", "low", "close"]
    )
    # Remove the downloaded CSV file
    os.remove(csv_file_path)

    # Establsh Redis connection, delete previous data and insert new data
    rs = RedisStore(connection_pool=settings.REDIS_CONN_POOL)
    rs.delete_stock_data()
    rs.insert_stock_data(stocks)
