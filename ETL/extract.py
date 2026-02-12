
"""
Author: Anthony
"""

from config import LOCAL_PATH, URLS
import requests
import zipfile
import os
import shutil
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def create_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET", "POST"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def download(url, path, session=None, timeout=30):
    session = session or create_session()
    logger.info("Downloading %s -> %s", url, path)
    try:
        with session.get(url, timeout=timeout, stream=True) as resp:
            resp.raise_for_status()
            with open(path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return True
    except requests.RequestException as e:
        logger.error("Failed to download %s: %s", url, e)
        return False


def unzip(zip_path, dest_path):
    if not os.path.exists(zip_path):
        logger.error("ZIP not found: %s", zip_path)
        return []

    if not zipfile.is_zipfile(zip_path):
        logger.error("Invalid ZIP file: %s", zip_path)
        return []

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            namelist = zip_ref.namelist()
            zip_ref.extractall(dest_path)
        try:
            os.remove(zip_path)
        except OSError:
            logger.warning("Could not remove zip %s", zip_path)
        logger.info("Extracted %s files from %s", len(namelist), zip_path)
        return namelist
    except zipfile.BadZipFile:
        logger.exception("Bad zip file %s", zip_path)
        return []
    except Exception:
        logger.exception("Unexpected error extracting %s", zip_path)
        return []


def rename(src, dst):
    try:
        if os.path.exists(src):
            os.replace(src, dst)
            logger.info("Renamed %s -> %s", src, dst)
        else:
            logger.warning("Source file does not exist: %s", src)
    except Exception:
        logger.exception("Failed to rename %s to %s", src, dst)


def main():
    # Recreate local path safely
    if os.path.exists(LOCAL_PATH):
        logger.info("Removing existing local path %s", LOCAL_PATH)
        try:
            shutil.rmtree(LOCAL_PATH)
        except Exception:
            logger.exception("Failed to remove %s", LOCAL_PATH)
    os.makedirs(LOCAL_PATH, exist_ok=True)

    session = create_session()

    for url, name in URLS:
        file_name = os.path.basename(url)
        complete_path = os.path.join(LOCAL_PATH, file_name)

        if not download(url, complete_path, session=session):
            logger.warning("Skipping %s due to download failure", url)
            continue

        extracted = unzip(complete_path, LOCAL_PATH)
        if not extracted:
            logger.warning("No files extracted from %s", complete_path)
            continue

        # prefer first CSV found
        csv_files = [n for n in extracted if n.lower().endswith('.csv')]
        if not csv_files:
            # if no csv, pick first entry
            csv_name = extracted[0]
        else:
            csv_name = csv_files[0]

        src = os.path.join(LOCAL_PATH, csv_name)
        _, ext = os.path.splitext(csv_name)
        final_name = os.path.join(LOCAL_PATH, name + ext)

        rename(src, final_name)
        logger.info("Saved: %s", final_name)


if __name__ == '__main__':
    main()



