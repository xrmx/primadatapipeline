import os

from datetime import timedelta, datetime


DIRNAME = os.path.abspath(os.path.dirname(__file__))
DUMP_BIN = os.path.join(DIRNAME, 'luigi.sh')


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        date = start_date + timedelta(n)
        yield date.strftime('%Y-%m-%d')


if __name__ == '__main__':
    start_date = datetime.strptime("2017-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2017-04-09", "%Y-%m-%d")

    for date in daterange(start_date, end_date):
       print(
           '{} {}'.format(DUMP_BIN, date)
       )
