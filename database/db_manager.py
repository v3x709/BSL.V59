import sqlite3, json, os

class DatabaseManager:
    def __init__(self, db_path='server.db'):
        self.db_path = db_path
        self.setup()

    def setup(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS players (
                id_high INTEGER, id_low INTEGER, token TEXT, name TEXT,
                trophies INTEGER, highest_trophies INTEGER, exp_points INTEGER,
                gems INTEGER, gold INTEGER, star_points INTEGER,
                ranked_points INTEGER, ranked_level INTEGER, brawlers TEXT,
                friends TEXT, mail TEXT, PRIMARY KEY (id_high, id_low))''')

            conn.execute('''CREATE TABLE IF NOT EXISTS clubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT,
                members TEXT)''')

    def get_player(self, h, l):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute('SELECT * FROM players WHERE id_high = ? AND id_low = ?', (h, l)).fetchone()
            if row:
                data = dict(row)
                data['brawlers'] = json.loads(data['brawlers'])
                data['friends'] = json.loads(data['friends'] or '[]')
                data['mail'] = json.loads(data['mail'] or '[]')
                return data
        return None

    def create_player(self, h, l, token):
        with sqlite3.connect(self.db_path) as conn:
            initial_brawlers = json.dumps({"0": {"id": 16000000, "skin": 29000000, "trophies": 0, "level": 1}})
            conn.execute('''INSERT INTO players (id_high, id_low, token, name, trophies, highest_trophies, exp_points, gems, gold, star_points, ranked_points, ranked_level, brawlers, friends, mail)
                            VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0, 0, 0, 1, ?, '[]', '[]')''',
                         (h, l, token, "Player", initial_brawlers))

    def update_player(self, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''UPDATE players SET name=?, trophies=?, highest_trophies=?, exp_points=?, gems=?, gold=?, star_points=?, ranked_points=?, ranked_level=?, brawlers=?, friends=?, mail=?
                            WHERE id_high=? AND id_low=?''',
                         (data['name'], data['trophies'], data['highest_trophies'], data['exp_points'], data['gems'], data['gold'], data['star_points'], data['ranked_points'], data['ranked_level'], json.dumps(data['brawlers']), json.dumps(data['friends']), json.dumps(data['mail']), data['id_high'], data['id_low']))

    def get_max_id_low(self):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute('SELECT MAX(id_low) FROM players').fetchone()
            return row[0] if row[0] is not None else 0
