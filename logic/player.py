import random

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
        self.ranked_level = data['ranked_level']
        self.brawlers = data['brawlers']
        self.friends = data.get('friends', [])
        self.mail = data.get('mail', [])

    def process_win(self):
        rgain = random.randint(200, 900)
        tgain = random.randint(80, 350)
        self.ranked_points += rgain
        self.trophies += tgain
        if self.trophies > self.highest_trophies:
            self.highest_trophies = self.trophies
        return rgain, tgain

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
            'ranked_level': self.ranked_level,
            'brawlers': self.brawlers,
            'friends': self.friends,
            'mail': self.mail
        }
