import json
import luigi
import os
import requests
import sqlite3

from datetime import datetime
from decimal import Decimal


SALES_API = 'http://127.0.0.1:8888/dailysales'
CURRENT_DIR = os.getcwd()


class ConsumeApi(luigi.Task):
    """Consumes the sales api, data is stored on an json file"""
    date = luigi.DateParameter()

    def run(self):
        data = {
            'day': self.date
        }
        response = requests.post(SALES_API, data=data)
        data = response.json()

        # Our API returns the amount as integer in cents, how unfortunate!
        # We want a proper decimal field instead!
        # Our storage does not support timestamp fields, how lame!
        # We are going to use a datetime!
        def ts_to_dt(ts):
            return datetime.strptime(ts[:-6], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        sales = [{
            'amount': '{}'.format(Decimal(r['amount']) / 100),
            'payment_type': r['payment_type'],
            'dt': ts_to_dt(r['timestamp']),
        } for r in data]

        with self.output().open('w') as f:
            json.dump(sales, f)

    def output(self):
        return luigi.LocalTarget('sales-{}.json'.format(self.date))


class StoreData(luigi.Task):
    """Store the normalized data into our db"""
    date = luigi.DateParameter()

    """
    CREATE TABLE sale (
        id INTEGER PRIMARY KEY,
        amount DECIMAL(10, 2),
        payment_type STRING,
        dt DATETIME
    )
    """

    def run(self):
        with open('sales-{}.json'.format(self.date), 'r') as f:
            conn = sqlite3.connect(os.path.join(CURRENT_DIR, 'sales.db'))
            c = conn.cursor()
            data = json.load(f)
            sales = [(r['amount'], r['payment_type'], r['dt']) for r in data]
            c.executemany('INSERT INTO sale (amount, payment_type, dt) VALUES (?,?,?)', sales)
            conn.commit()
            conn.close()

    def requires(self):
        return ConsumeApi(self.date)
