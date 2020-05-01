import requests

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse


def download_learning_portfolios(search_url: str):
    search_resp = requests.get(search_url)
    search_resp_soup = BeautifulSoup(search_resp.text, "html.parser")

    table = search_resp_soup.find("table", class_="new_table")
    if not table:
        return

    tr_rows = table.find_all("tr")

    def _thread_download_and_save(tr_row):
        td_rows = tr_row.find_all("td")
        if len(td_rows) < 2 or td_rows[1].text.strip() != "核心資料":
            return
        url = urljoin(search_url, td_rows[1].find("a")["href"])
        filename = td_rows[0].text.strip() + ".pdf"

        page = requests.get(url)

        with open(filename, "wb") as f:
            f.write(page.content)

    with ThreadPoolExecutor(max_workers=8) as executor:
        for row in tr_rows:
            executor.submit(_thread_download_and_save, row)


def download_learning_portfolios_111():
    for i in range(155):
        i_str = "{:03d}".format(i)
        download_learning_portfolios(
            f"https://www.cac.edu.tw/cacportal/jbcrc/LearningPortfolios/ColGsdLP.php?college={i_str}"
        )


if __name__ == "__main__":
    download_learning_portfolios_111()
