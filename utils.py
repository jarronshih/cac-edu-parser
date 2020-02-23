from bs4 import BeautifulSoup
from enum import Enum, auto
from zipfile import ZipFile


class SchoolAttr(Enum):
    INDEX = auto()
    NAME = auto()


def zipfile_reader(zip_file_path: str):
    zip_file = ZipFile(zip_file_path)
    for filename in zip_file.namelist():
        content = zip_file.read(filename).decode()
        yield filename, content


def school_parser(content: str):
    soup = BeautifulSoup(content, "html.parser")
    tables = soup.find_all("table")

    result = {}

    # index
    index = tables[1].find_all("td", limit=2)[1].text.strip()
    result[SchoolAttr.INDEX.name.lower()] = index

    # name
    school_name_raw = tables[0].find("p").text
    school_name = "".join(school_name_raw.split())
    result[SchoolAttr.NAME.name.lower()] = school_name

    # others
    for tr in tables[1].find_all("tr"):
        tds = tr.find_all("td")
        for i in range(8, min(10, len(tds))):
            percentage = tds[i].text.strip()
            if "%" not in percentage:
                continue
            attr = tds[i - 2].text.strip()
            result[attr] = percentage
            break

    return result

