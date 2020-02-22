import requests
from bs4 import BeautifulSoup
from os import path
from pathlib import Path
from urllib.parse import urljoin, urlparse


def download(search_url: str, form_data: dict):
    search_resp = requests.post(search_url, data=form_data)
    search_resp_soup = BeautifulSoup(search_resp.text, "html.parser")

    table = search_resp_soup.find("table")
    rows = table.find_all("a")

    for row in rows:
        url = urljoin(search_url, row["href"])
        filename = Path(urlparse(url).path).name

        if path.exists(filename):
            continue

        page = requests.get(url)
        page.encoding = "utf8"

        with open(filename, "x") as f:
            f.write(page.text)


def download_108():
    # Entrance: https://www.cac.edu.tw/apply108/system/108ColQry_forapply_3r5k9d/gsd_search_php.php?part=part_1
    search_url = "https://www.cac.edu.tw/apply108/system/108ColQry_forapply_3r5k9d/ShowGsd.php"  # 108 year
    payload = {"TxtSTest": "審查", "SubSTest": "依指定項目名稱查詢", "action": "SubSTest"}

    download(search_url, payload)


def download_109():
    pass


if __name__ == "__main__":
    download_108()
    # download_109()
