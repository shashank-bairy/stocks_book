import os
import requests
import datetime
import zipfile
from pathlib import Path

def download(download_url, file_path):
    """
    download function is used to fetch the data
    """
    print("Downloading file at", file_path)

    if not os.path.exists(file_path):
        file_to_save = open(file_path, "wb")
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
        with requests.get(download_url, headers=headers, verify=False, stream=True) as response:
            for chunk in response.iter_content(chunk_size=1024):
                file_to_save.write(chunk)
        print("Completed downloading file")
    else:
        print("We already have this file cached locally")

def unzip(file_path):
    """
    unzip function used to unzip downloaded file
    """
    print(file_path)
    with zipfile.ZipFile(file_path, "r") as compressed_file:
        compressed_file.extractall(Path(file_path).parent)
    print("Completed un-compressing")