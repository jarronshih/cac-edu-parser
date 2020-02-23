from bs4 import BeautifulSoup
from enum import Enum, auto
from zipfile import ZipFile


class SchoolAttr(Enum):
    INDEX = auto()
    NAME = auto()
    EXAM = auto()
    SPECIAL_EXAM = auto()


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
    assert index
    result[SchoolAttr.INDEX.name.lower()] = index

    # exam
    exam_tds = tables[1].find("tr").find_all("td", limit=7)
    exam = exam_tds[6].text.strip()
    assert "%" in exam, f"Exam not found: {exam_tds}"
    result[SchoolAttr.EXAM.name.lower()] = exam

    # name
    school_name_raw = tables[0].find("p").text
    school_name = "".join(school_name_raw.split())
    assert school_name, f"School Name not found: {school_name_raw}"
    result[SchoolAttr.NAME.name.lower()] = school_name

    # special exam
    special_exam_tds = tables[1].find("tr").find_all("td")
    if len(special_exam_tds) >= 15:
        special_exam = special_exam_tds[14].text.strip()
        if "%" in special_exam and special_exam[:-1]:
            result[SchoolAttr.SPECIAL_EXAM.name.lower()] = special_exam

    # others
    for tr in tables[1].find_all("tr"):
        tds = tr.find_all("td")
        for i in range(8, min(10, len(tds))):
            percentage = tds[i].text.strip()
            if "%" not in percentage and percentage[:-1]:
                continue
            attr = tds[i - 2].text.strip()
            result[attr] = percentage
            break

    # assert 100%
    total = 0
    for value in result.values():
        if "%" in value:
            total += int(value[:-1])
    if total != 100:
        print(result)
    assert total == 100, result

    return result

