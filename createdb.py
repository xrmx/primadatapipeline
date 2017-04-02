import os.path
import sqlite3


CURRENT_DIR = os.path.dirname(__file__)

conn = sqlite3.connect('sales.db')
c = conn.cursor()
c.execute("""
    CREATE TABLE sale (
        id INTEGER PRIMARY KEY,
        amount DECIMAL(10, 2),
        payment_type TEXT,
        dt DATETIME
    );
""")
conn.commit()
conn.close()
