import pytest
from collections import defaultdict
from cac_parser.formatter import standard_formatter, STANDARD_HEADERS
from cac_parser.utils import *


def test_attr_analysis():
    attrs = defaultdict(int)
    for _, content in zipfile_reader("data/109.zip"):
        d = school_parser(content)
        for name in d:
            attrs[name] += 1

    return sorted(attrs.items(), key=lambda x: x[1], reverse=True)


def test_csv():
    with open("output.csv", "w+") as f:
        # headers
        f.write(",".join(STANDARD_HEADERS))
        f.write("\n")

        for _, content in zipfile_reader("data/109.zip"):
            result = school_parser(content)
            row = standard_formatter(result)
            f.write(",".join(row))
            f.write("\n")


@pytest.mark.skip(reason="no data")
def test_parse_learning_portfolios_html():
    with open("output.csv", "w+") as f:
        f.write(",".join(e.value for e in LearningPortfolioAttr))
        f.write("\n")

        for _, content in zipfile_reader("data/111_learning_portfolios_html.zip"):
            result = learning_portfolios_parser(content)

            f.write(",".join(result[e] for e in LearningPortfolioAttr))
            f.write("\n")
