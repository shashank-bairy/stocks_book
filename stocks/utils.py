import os
import json
import requests
import pytz
import zipfile
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

def get_date_IST():
    """
    Returns the date value in Indian Standard Time in ddmmyy format.
    If we are making request before 18:00 then it needs to return previous
    day's date.
    """
    IST = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(IST)
    upload_time = datetime.now(IST).replace(hour=18, minute=0, second=0, microsecond=0)
    if current_time.time() < upload_time.time():
        current_time = current_time - timedelta(1)
    date = current_time.strftime("%d%m%Y")
    date = date[:4]+date[6:]
    return date

def download(download_url, file_path):
    """
    Function is download data from given url and save it in given file path. 
    """
    if not os.path.exists(file_path):
        file_to_save = open(file_path, "wb")
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
        with requests.get(download_url, headers=headers, verify=False, stream=True) as response:
            for chunk in response.iter_content(chunk_size=1024):
                file_to_save.write(chunk)
    else:
        print("File already cached locally")

def unzip(file_path):
    """
    Function used to unzip downloaded file and extract it's contents.
    """
    with zipfile.ZipFile(file_path, "r") as compressed_file:
        compressed_file.extractall(Path(file_path).parent)

def get_csv_data(csv_file_path, usecols, columns):
    """
    Read data in given csv file path from given columns 'usecols' and renaming the columns according to given 'columns' value. 
    """
    df = pd.read_csv(
        csv_file_path,
        usecols=usecols
    )
    df.columns = columns
    df['name'] = df['name'].str.strip()

    csv_data = json.loads(df.to_json(orient='table'))["data"]
    return csv_data