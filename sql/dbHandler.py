import sqlite3
from os import getcwd
from os.path import join

dbPath = join(getcwd(), "database.db")
createHistory = """
    CREATE TABLE if NOT EXISTS history (
        id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        n01 text,
        n02 text,
        n03 text,
        n04 text,
        n05 text,
        n06 text,
        n07 text,
        n08 text,
        n09 text,
        n10 text,
        n11 text,
        n12 text,
        radno integer,
        date text,
        count integer
    )
"""

class DBHandler(object):
    def __init__(self):
        self._conn = sqlite3.connect(dbPath)
        self._cursor = self._conn.cursor()
        self._createTable()

    def _createTable(self):
        self._cursor.execute(createHistory)
        self._conn.commit()

    def getRecent(self):
        query = """
            SELECT MAX(radno) FROM history
        """
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        return result[0]

    def getAll(self):
        query = """
            SELECT * FROM history
        """
        self._cursor.execute(query)
        self.result = self._cursor.fetchall()
        self.headers = [h[0] for h in self._cursor.description]
        return self.result

    def insert(self, data):
        query = """
            INSERT INTO history
            (n01, n02, n03, n04, n05, n06, n07, n08, n09, n10, n11, n12, radno, date, count)
            VALUES
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        self._cursor.execute(query, data)
        self._conn.commit()

    def getNewest(self):
        query = """
            SELECT * FROM history
            ORDER BY radno DESC
            LIMIT 1
        """
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        return result
