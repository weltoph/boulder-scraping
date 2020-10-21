from urllib import request
from bs4 import BeautifulSoup  # type: ignore

import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <url>")

try:
    with request.urlopen(sys.argv[1]) as page:
        if page.code == 200:
            soup = BeautifulSoup(page, "html.parser")
            freimann = soup.find("div", "sys-hall-title", string="KB Freimann")
            parent = freimann.parent
            values = parent.find_all("div", "sys-hall-limit-value")
            boulder = values[-1]
            value = int(boulder.find("span").text)
            print(value)
        else:
            raise ValueError("Oppps")
except Exception:
    # report this via Telegram
    pass
