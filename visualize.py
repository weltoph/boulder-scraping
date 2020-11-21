import typing
import datetime as dt
import dataclasses
import matplotlib.pyplot as plt
import matplotlib.colors as clrs

import model
import numpy as np
from peewee import fn


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
        object.__setattr__(self, "values", values)

    def day_values(self, offset: int) -> typing.List[
            typing.Tuple[typing.Optional[float], typing.Optional[int]]]:
        day = self.start_day + dt.timedelta(days=offset)
        if day.weekday() in [1,2,3]:
            beginning = 7
            hours = []
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

        # TODO: make alpha values a bit more useful
        alpha = np.array(
                [[(v/4 if v else 0) for _, v in data[i]]
                 for i in range(len(data))],
                dtype=float, ndmin=2).transpose()

        cmap = plt.cm.Greens
        display_data = clrs.Normalize()(values)
        display_data = cmap(display_data)


        for x in range(len(xaxis)):
            for y in range(len(yaxis)):
                display_data[y][x][-1] = alpha[y][x]

        fig, ax = plt.subplots()
        im = ax.imshow(display_data)

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
