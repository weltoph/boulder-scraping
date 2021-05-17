from urllib import request
from bs4 import BeautifulSoup  # type: ignore

import model
import config
import sys

def log_error(msg: str):
    error: model.ErrorPoint = model.ErrorPoint(msg)
    error.save()

try:
    with request.urlopen(config.URL) as page:
        if page.code != 200:
            log_error(f"Unexpected return code <{page.code}>")
            sys.exit(1)
        soup = BeautifulSoup(page, "html.parser")
        block = soup.find("div", {"class": "sys2-block"})
        if block is None:
            log_error("Could not find div of class 'sys2-block'")
            sys.exit(1)
        for point in block("div", recursive=False):
            name = point.find("div", {"class": "sys-hall-title"}).text
            climbing = None
            bouldering = None
            for value in point.find_all("div", {"class": "sys-hall-limit-value"}):
                number = int(value.find("span").text)
                number_type = value.text[:value.text.find(":")].strip()
                if number_type == "Klettern":
                    climbing = number
                elif number_type == "Bouldern":
                    bouldering = number
                else:
                    log_error(f"Unknown number type <{number_type}>")
            data_point = model.DataPoint(
                    place=name,
                    boulder=bouldering,
                    climbing=climbing)
            data_point.save()
except Exception as e:
    log_error(f"Unexpected exception: {e}")
    sys.exit(1)
