import typing
import datetime as dt
import dataclasses
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.colors as clrs  # type: ignore

import model
import numpy as np  # type: ignore
from peewee import fn  # type: ignore


WEEKDAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"]


@dataclasses.dataclass(frozen=True)
class Weekmap:
    start_day: dt.date

    def __post_init__(self):
        values = tuple(model.Scrap
                       .select()
                       .where((self.start_day <= model.Scrap.date)
                              & (model.Scrap.date < (self.start_day
                                                     + dt.timedelta(days=7)))))
        object.__setattr__(self, "_values", values)

    @property
    def values(self) -> typing.Tuple[model.Scrap]:
        return self._values  # type: ignore

    def day_values(self, offset: int) -> typing.List[
            typing.Tuple[typing.Optional[float], typing.Optional[int]]]:
        day = self.start_day + dt.timedelta(days=offset)
        if day.weekday() in [1,2,3]:
            beginning = 7
            hours: typing.List[typing.Tuple[typing.Optional[float],
                               typing.Optional[int]]] = []
        else:
            beginning = 9
            hours = [(None, None), (None, None)]
        for hour in range(beginning, 24):
            values = [value.free_spaces for value in self.values
                                        if (value.date.date() == day and
                                            value.date.hour == hour and
                                            not value.error)]
            hours.append(
                    (sum(values)/len(values) if values else None, len(values))
                    )
        return hours

    @property
    def img(self):
        xaxis = [WEEKDAYS[(self.start_day + dt.timedelta(days=i)).weekday()]
                 for i in range(0, 7)]
        yaxis = [i for i in range(7, 24)]
        data = [self.day_values(offset) for offset in range(0, 7)]

        values = np.array(
                [[(f if f else -1.0) for f, _ in data[i]]
                 for i in range(len(data))],
                dtype=float, ndmin=2).transpose()
        values = np.ma.masked_less(values, 0)

        confidence = np.array(
                [[(1 - v/4 if v else 1) for _, v in data[i]]
                 for i in range(len(data))],
                dtype=float, ndmin=2).transpose()

        display_values = plt.cm.Greens(clrs.Normalize()(values))
        display_confidence = plt.cm.Reds(clrs.Normalize()(confidence))

        print(display_values)
        print(display_confidence)

        actual_data = [[None for _ in range(len(xaxis))]
                       for _ in range(len(yaxis))]

        for x in range(len(xaxis)):
            for y in range(len(yaxis)):
                actual_data[y][x] = ((display_values[y][x][0]
                                        + display_confidence[y][x][0])/2,
                                     (display_values[y][x][1]
                                      + display_confidence[y][x][1])/2,
                                     (display_values[y][x][2]
                                      + display_confidence[y][x][2])/2)
                places, tests = data[x][y]
                if places is None and tests is None:
                    actual_data[y][x] += (0,)
                else:
                    actual_data[y][x] += (1,)

        fig, ax = plt.subplots()
        im = ax.imshow(actual_data)

        ax.set_xticklabels(xaxis)
        ax.set_yticklabels(yaxis)
        ax.set_xticks(np.arange(len(xaxis)))
        ax.set_yticks(np.arange(len(yaxis)))

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")


        fig.tight_layout()
        plt.show()



day = dt.date(2020, 10, 26)
Weekmap(day).img
