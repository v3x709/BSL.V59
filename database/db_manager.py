import sqlite3, json
class DatabaseManager:
    def __init__(self, db_path='server.db'):
        self.db_path = db_path
        self.setup()
    def setup(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS players (id_high INTEGER, id_low INTEGER, token TEXT, name TEXT, trophies INTEGER, brawlers TEXT, PRIMARY KEY (id_high, id_low))''')
    def get_player(self, h, l):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute('SELECT * FROM players WHERE id_high = ? AND id_low = ?', (h, l)).fetchone()
            if row: return {'id_high': row[0], 'id_low': row[1], 'token': row[2], 'name': row[3], 'trophies': row[4], 'brawlers': json.loads(row[5])}
        return None
