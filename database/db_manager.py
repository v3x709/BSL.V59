import sqlite3
import json
import os

class DatabaseManager:
    def __init__(self, db_path='server.db'):
        self.db_path = db_path
        self.setup()

    def setup(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id_high INTEGER,
                id_low INTEGER,
                token TEXT,
                name TEXT,
                trophies INTEGER,
                highest_trophies INTEGER,
                exp_points INTEGER,
                gems INTEGER,
                gold INTEGER,
                star_points INTEGER,
                ranked_points INTEGER,
                brawlers TEXT,
                last_online TEXT,
                PRIMARY KEY (id_high, id_low)
            )
        ''')
        conn.commit()
        conn.close()

    def get_player(self, id_high, id_low):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players WHERE id_high = ? AND id_low = ?', (id_high, id_low))
        row = cursor.fetchone()
        conn.close()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None

    def create_player(self, id_high, id_low, token):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Default brawlers: only Shelly (ID 16, CSV index 0)
        initial_brawlers = json.dumps({
            "0": {"id": 16000000, "skin": 29000000, "trophies": 0, "highest_trophies": 0, "level": 1, "points": 0}
        })
        cursor.execute('''
            INSERT INTO players (id_high, id_low, token, name, trophies, highest_trophies, exp_points, gems, gold, star_points, ranked_points, brawlers, last_online)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (id_high, id_low, token, "Player", 0, 0, 0, 0, 0, 0, 0, initial_brawlers))
        conn.commit()
        conn.close()

    def update_player(self, player_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE players SET
                name = ?, trophies = ?, highest_trophies = ?, exp_points = ?, gems = ?, gold = ?, star_points = ?, ranked_points = ?, brawlers = ?, last_online = datetime('now')
            WHERE id_high = ? AND id_low = ?
        ''', (
            player_data['name'], player_data['trophies'], player_data['highest_trophies'],
            player_data['exp_points'], player_data['gems'], player_data['gold'],
            player_data['star_points'], player_data['ranked_points'],
            json.dumps(player_data['brawlers']) if isinstance(player_data['brawlers'], dict) else player_data['brawlers'],
            player_data['id_high'], player_data['id_low']
        ))
        conn.commit()
        conn.close()

    def get_player_by_token(self, token):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players WHERE token = ?', (token,))
        row = cursor.fetchone()
        conn.close()
        if row:
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, row))
            data['brawlers'] = json.loads(data['brawlers'])
            return data
        return None

    def get_max_id_low(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id_low) FROM players')
        row = cursor.fetchone()
        conn.close()
        return row[0] if row[0] is not None else 0
