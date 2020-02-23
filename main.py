from collections import defaultdict
from utils import zipfile_reader, school_parser, SchoolAttr


def _test_zipfile_reader(filename):
    import itertools

    yield from itertools.islice(zipfile_reader(filename), 5)


def attr_analysis():
    attrs = defaultdict(int)
    for _, content in zipfile_reader("data/109.zip"):
        d = school_parser(content)
        for name in d:
            attrs[name] += 1

    return sorted(attrs.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    HEADERS = [
        "校系代碼",
        "校系名稱",
        "學測成績佔甄選總成績比例",
        "術科成績佔甄選總成績比例",
        "審查資料",
        "高中成績綜合審查",
        "面試/口試/面談",
        "All",
    ]
    with open("output.csv", "w+") as f:
        # headers
        f.write(",".join(HEADERS))
        f.write("\n")

        for filename, content in zipfile_reader("data/109.zip"):
            result = school_parser(content)
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
                    f"{k}:{v}"
                    for k, v in result.items()
                    if isinstance(v, str) and v[-1] == "%"
                )
            )

            f.write(",".join(row))
            f.write("\n")
