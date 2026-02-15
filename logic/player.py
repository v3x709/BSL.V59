import random
import json

class Player:
    def __init__(self, data):
        self.data = data
        self.id_high = data['id_high']
        self.id_low = data['id_low']
        self.name = data['name']
        self.trophies = data['trophies']
        self.highest_trophies = data['highest_trophies']
        self.exp_points = data['exp_points']
        self.gems = data['gems']
        self.gold = data['gold']
        self.star_points = data['star_points']
        self.ranked_points = data['ranked_points']
        self.brawlers = data['brawlers'] # Dict of brawler_id -> stats

    def add_battle_reward(self, win=True):
        if win:
            trophy_gain = random.randint(80, 350)
            ranked_gain = random.randint(200, 900)
            self.trophies += trophy_gain
            self.ranked_points += ranked_gain
            if self.trophies > self.highest_trophies:
                self.highest_trophies = self.trophies
            return trophy_gain, ranked_gain
        else:
            # Losing might still give some points in this "modded" server or just 0
            return 0, 0

    def to_dict(self):
        return {
            'id_high': self.id_high,
            'id_low': self.id_low,
            'name': self.name,
            'trophies': self.trophies,
            'highest_trophies': self.highest_trophies,
            'exp_points': self.exp_points,
            'gems': self.gems,
            'gold': self.gold,
            'star_points': self.star_points,
            'ranked_points': self.ranked_points,
            'brawlers': self.brawlers
        }
