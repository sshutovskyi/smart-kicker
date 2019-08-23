import json
from .player import Player

class PlayersContainer:
    def __init__(self, path):
        self.path = path
        self.players = []

    def load(self):
        with open(self.path) as json_file:
            items = json.load(json_file)
            self.set_list(items)

    def set_list(self, items):
        self.players = {}
        for item in items:
            player = Player(item['id'], item['name'], item['key'])
            self.players[player.key] = player

    def save(self, items):
        with open(self.path, 'w') as outfile:
            json.dump(items, outfile)
        self.set_list(items)

    def get(self, key):
        return self.players.get(key, None)
