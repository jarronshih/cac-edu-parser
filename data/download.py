import requests

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from os import path
from pathlib import Path
from urllib.parse import urljoin, urlparse


def download(search_url: str, form_data: dict):
    search_resp = requests.post(search_url, data=form_data)
    search_resp_soup = BeautifulSoup(search_resp.text, "html.parser")

    table = search_resp_soup.find("table")
    rows = table.find_all("a")

    def _thread_download_and_save(row_href: str):
        url = urljoin(search_url, row_href)
        filename = Path(urlparse(url).path).name

        if path.exists(filename):
            return

        page = requests.get(url)
        page.encoding = "utf8"

        with open(filename, "x") as f:
            f.write(page.text)

    with ThreadPoolExecutor(max_workers=8) as executor:
        for row in rows:
            executor.submit(_thread_download_and_save, row["href"])


def download_108():
    # Entrance: https://www.cac.edu.tw/apply108/system/108ColQry_forapply_3r5k9d/gsd_search_php.php?part=part_1
    search_url = "https://www.cac.edu.tw/apply108/system/108ColQry_forapply_3r5k9d/ShowGsd.php"  # 108 year
    payloads = [
        {"TxtGsdCode": "0", "SubTxtGsdCode": "依校系代碼查詢", "action": "SubTxtGsdCode",},
        {"TxtGsdCode": "1", "SubTxtGsdCode": "依校系代碼查詢", "action": "SubTxtGsdCode",},
        {"TxtSTest": "審查", "SubSTest": "依指定項目名稱查詢", "action": "SubSTest"},
    ]

    for payload in payloads:
        download(search_url, payload)


def download_109():
    # Entrance: https://www.cac.edu.tw/apply109/system/109ColQrytk4p_forapply_os92k5w/gsd_search_php.php?part=part_1
    search_url = "https://www.cac.edu.tw/apply109/system/109ColQrytk4p_forapply_os92k5w/ShowGsd.php"  # 108 year
    payloads = [
        {"TxtGsdCode": "0", "SubTxtGsdCode": "依校系代碼查詢", "action": "SubTxtGsdCode",},
        {"TxtGsdCode": "1", "SubTxtGsdCode": "依校系代碼查詢", "action": "SubTxtGsdCode",},
        {"TxtSTest": "審查", "SubSTest": "依指定項目名稱查詢", "action": "SubSTest"},
    ]

    for payload in payloads:
        download(search_url, payload)


if __name__ == "__main__":
    # download_108()
    download_109()
