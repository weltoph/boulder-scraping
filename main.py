from urllib import request
from bs4 import BeautifulSoup  # type: ignore

import model
import config

try:
    with request.urlopen(config.URL) as page:
        if page.code == 200:
            soup = BeautifulSoup(page, "html.parser")
            freimann = soup.find("div", "sys-hall-title", string="KB Freimann")
            parent = freimann.parent
            values = parent.find_all("div", "sys-hall-limit-value")
            boulder = values[-1]
            value_text = boulder.find("span").text
            if not value_text:
                raise ValueError("could not find correct value")
            else:
                try:
                    value = int(value_text)
                    print(f"logging value: {value}")
                    scrap = model.Scrap(free_spaces=value, error=None)
                    scrap.save()
                except ValueError:
                    raise ValueError(f"could not convert {value_text} to int")
        else:
            raise ValueError(f"error code: {page.code}")
except Exception as e:
    print(f"logging error: {e}")
    scrap = model.Scrap(error=str(e), free_spaces=None)
    scrap.save()
