import peewee  # type: ignore
import datetime
import config

db = peewee.SqliteDatabase(config.DATABASE, pragmas={
    'journal_mode': 'wal',
    'foreign_keys': 1,
    'ignore_check_constraints': 0})


class Scrap(peewee.Model):
    date = peewee.DateTimeField(default=datetime.datetime.now)
    free_spaces = peewee.IntegerField(null=True)
    error = peewee.CharField(null=True)

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Scrap])
