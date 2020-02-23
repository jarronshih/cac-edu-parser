from collections import defaultdict
from utils import zipfile_reader, school_parser


def _zipfile_reader(filename):
    import itertools

    yield from itertools.islice(zipfile_reader(filename), 5)


if __name__ == "__main__":
    attrs = defaultdict(int)
    for filename, content in zipfile_reader("data/109.zip"):
        d = school_parser(content)
        # print(d)
        for name in d:
            attrs[name] += 1

    # print(sorted(attrs.items(), key=lambda x: x[1], reverse=True))
