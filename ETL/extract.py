
"""
Author: Anthony
"""

from config import *
import requests
import zipfile
import os
import shutil

def download(url,path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(path, "wb") as f:
                f.write(response.content)
                
    else:
        print(f"Error downloading {url}")

def unzip(zip_path, dest_path):
    try:
        if not zipfile.is_zipfile(zip_path):
            print(f"Error: {zip_path} invalid ZIP.")
            return
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_path)

        os.remove(zip_path)

    except FileNotFoundError:
        print(f"Error: File not found in {zip_path}")
    except zipfile.BadZipFile:
        print(f"Error: File {zip_path} damaged [10].")
    except PermissionError:
        print(f"Error: Access denied to {zip_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return zip_ref.namelist()

def rename (name,new_name):
    if os.path.exists(name):
        os.rename(name, new_name)

shutil.rmtree(LOCAL_PATH)
os.makedirs(LOCAL_PATH)

for url,name in URLS:

    file_name = url.split("/")[-1]
    complete_path = LOCAL_PATH + file_name
    print(f"Dowloading: {file_name}")

    download(url,complete_path)

    csv = "".join(unzip(complete_path,LOCAL_PATH))
    extension = "." + csv.split(".")[-1]
    final_name = LOCAL_PATH + name + extension

    rename(LOCAL_PATH + csv,final_name)
    print(f"Saved: {final_name}")



