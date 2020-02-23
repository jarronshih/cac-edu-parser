from typing import List
from cac_parser.utils import SchoolAttr


STANDARD_HEADERS = [
    "校系代碼",
    "校系名稱",
    "學測成績佔甄選總成績比例",
    "術科成績佔甄選總成績比例",
    "審查資料",
    "高中成績綜合審查",
    "面試/口試/面談",
    "All",
]


def standard_formatter(result: dict):
    row = [
        result[SchoolAttr.INDEX],
        result[SchoolAttr.NAME],
    ]

    if SchoolAttr.EXAM in result:
        row.append(result[SchoolAttr.EXAM])
    else:
        row.append("")

    if SchoolAttr.SPECIAL_EXAM in result:
        row.append(result[SchoolAttr.SPECIAL_EXAM])
    else:
        row.append("")

    if "審查資料" in result:
        row.append(result["審查資料"])
    else:
        row.append("")

    if "高中成績綜合審查" in result:
        row.append(result["高中成績綜合審查"])
    else:
        row.append("")

    for key in result:
        if not isinstance(key, str):
            continue
        if "面試" in key or "口試" in key or "面談" in key:
            row.append(result[key])
            break
    else:
        row.append("")

    row.append(
        ";".join(
            f"{k}:{v}" for k, v in result.items() if isinstance(v, str) and v[-1] == "%"
        )
    )
    return row
