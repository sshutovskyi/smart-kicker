#!/usr/bin/env python

from lib.players_container import PlayersContainer
from lib.client import Client
from lib.table import Table
from lib.display import Display
from lib.sensor import Sensor
from lib.side import Side

players_container = PlayersContainer('players.json')
players_container.load()

client = Client(players_container)
client.connect()

table = Table([
    Side(1, '1', Sensor("/dev/ttyACM0")),
    Side(2, '2', Sensor("/dev/ttyACM1")),
], players_container)

table.display = Display()
table.client = client

table.reset()

while True:
    table.tick()
