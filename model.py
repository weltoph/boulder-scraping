import peewee  # type: ignore
import datetime
import config

db = peewee.SqliteDatabase(config.DATABASE, pragmas={
    'journal_mode': 'wal',
    'foreign_keys': 1,
    'ignore_check_constraints': 0})


class DataPoint(peewee.Model):
    date = peewee.DateTimeField(default=datetime.datetime.now)
    place = peewee.CharField()
    boulder = peewee.IntegerField(null=True)
    climbing = peewee.IntegerField(null=True)

    class Meta:
        database = db


class ErrorPoint(peewee.Model):
    date = peewee.DateTimeField(default=datetime.datetime.now)
    msg = peewee.CharField()

    class Meta:
        database = db

def create_tables():
    with db:
        db.create_tables([DataPoint, ErrorPoint])


if __name__ == "__main__":
    create_tables()
