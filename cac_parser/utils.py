from bs4 import BeautifulSoup
from enum import Enum, auto
from zipfile import ZipFile
import re


class SchoolAttr(Enum):
    INDEX = "校系代碼"
    NAME = "校系名稱"
    EXAM = "學測成績"
    SPECIAL_EXAM = "術科成績"

    def __str__(self):
        return str(self.value)


def zipfile_reader(zip_file_path: str, decode=True):
    zip_file = ZipFile(zip_file_path)
    for filename in zip_file.namelist():
        content = zip_file.read(filename)
        if decode:
            content = content.decode()
        yield filename, content


def school_parser(content: str):
    soup = BeautifulSoup(content, "html.parser")
    tables = soup.find_all("table")

    result = {}

    # index
    index = tables[1].find_all("td", limit=2)[1].text.strip()
    assert index
    result[SchoolAttr.INDEX] = index

    # name
    school_name_raw = tables[0].find("p").text
    school_name = "".join(school_name_raw.split())
    assert school_name, f"School Name not found: {school_name_raw}"
    result[SchoolAttr.NAME] = school_name

    # exam
    exam_tds = tables[1].find("tr").find_all("td", limit=7)
    exam = exam_tds[6].text.strip()
    assert "%" in exam, f"Exam not found: {exam_tds}"
    result[SchoolAttr.EXAM] = exam

    # special exam
    special_exam_tds = tables[1].find("tr").find_all("td")
    if len(special_exam_tds) >= 15:
        special_exam = special_exam_tds[14].text.strip()
        if "%" in special_exam and special_exam[:-1]:
            result[SchoolAttr.SPECIAL_EXAM] = special_exam

    # others
    for tr in tables[1].find_all("tr"):
        tds = tr.find_all("td")
        for i in range(8, min(10, len(tds))):
            percentage = tds[i].text.strip()
            if "%" not in percentage:
                continue
            if not percentage[:-1] or percentage == "0%":
                continue
            attr = tds[i - 2].text.strip()
            result[attr] = percentage
            break

    # validate total percentage is 100%
    total = 0
    for value in result.values():
        if "%" in value:
            total += int(value[:-1])
    assert total == 100, result

    return result


class LearningPortfolioAttr(Enum):
    UNIVERSITY = "大學"
    MAJOR = "科系"
    COURSE_RECORD = "修課紀錄"
    STUDY_RESULT = "課程學習成果"
    DIVERSITY = "多元表現"


learning_portfolios_name_pattern = re.compile(r".*-.*")
learning_portfolios_pattern = re.compile(r"(\(\d+\).*)|(\d+\..*)")


def learning_portfolios_parser(content):
    result = {}

    soup = BeautifulSoup(content, "html.parser")
    texts = [div.text.strip() for div in soup.find_all("div", class_="t")]

    for text in texts:
        if learning_portfolios_name_pattern.match(text):
            (
                result[LearningPortfolioAttr.UNIVERSITY],
                result[LearningPortfolioAttr.MAJOR],
            ) = text.split("-", 1)
            break
    else:
        raise Exception("UNIVERSITY not found")

    title_and_content_div = soup.select("div.x5,div.x6")
    contents = [""]

    for div in title_and_content_div:
        if "x5" in div["class"]:
            if contents[-1]:
                contents.append("")
        else:
            if not contents[-1] and not learning_portfolios_pattern.match(
                div.text.strip()
            ):
                continue
            contents[-1] += div.text.strip()

    (
        result[LearningPortfolioAttr.COURSE_RECORD],
        result[LearningPortfolioAttr.STUDY_RESULT],
        result[LearningPortfolioAttr.DIVERSITY],
    ) = contents
    return result
