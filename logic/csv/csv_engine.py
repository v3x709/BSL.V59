import csv
import os

class CSVRow:
    def __init__(self, data):
        self._data = data

    def get_value(self, key):
        return self._data.get(key, "")

class CSVTable:
    def __init__(self, filepath):
        self.rows = []
        self.filepath = filepath
        self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            types = next(reader)
            for row in reader:
                if row:
                    data = dict(zip(headers, row))
                    self.rows.append(CSVRow(data))

class CSVEngine:
    def __init__(self, csv_path='data/csv'):
        self.csv_path = csv_path
        self.tables = {}

    def load_table(self, name):
        filepath = os.path.join(self.csv_path, f"{name}.csv")
        self.tables[name] = CSVTable(filepath)

    def get_table(self, name):
        if name not in self.tables:
            self.load_table(name)
        return self.tables[name]
