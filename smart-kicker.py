#!/usr/bin/env python

import ssl
import serial
import pygame
import os
import json
import time
import paho.mqtt.client as mqtt
import random
import strict_rfc3339

def get_datetime():
    return strict_rfc3339.timestamp_to_rfc3339_utcoffset(int(time.time()))

WHITE = (255, 255, 255)
class Screen:
    def __init__(self):
        os.putenv('SDL_FBDEV', '/dev/fb0')
        pygame.init()
        self.lcd = pygame.display.set_mode((900, 700))
        self.lcd.fill((255, 0, 0))
        pygame.mouse.set_visible(False)
        pygame.display.update()
        self.font_big = pygame.font.Font(None, 60)
        self.lcd.fill((0, 0, 0))
        text_surface = self.font_big.render('SMART KICKER', True, WHITE)
        rect = text_surface.get_rect(center=(240, 160))
        self.lcd.blit(text_surface, rect)
        pygame.display.update()

    def render(self, text):
        self.lcd.fill((0, 0, 50))
        text_surface = self.font_big.render(text, True, WHITE)
        rect = text_surface.get_rect(center=(500, 300))
        self.lcd.blit(text_surface, rect)
        pygame.display.update()

class Sensor:
    def __init__(self, port):
        self.serial = serial.Serial(port, 9600)
        self.serial.flushInput()
        self.buffer = ''

    def read(self):
        if self.serial.inWaiting() > 0 :
            char = self.serial.read(1)
            self.buffer += char
            if '}' in char :
                event = json.loads(self.buffer)
                self.buffer = ''
                return event

        return None

class Player:
    def __init__(self, id, name, key):
        self.id = id
        self.name = name
        self.key = key
    def __eq__(self, other):
        return self.id == other.id

class Table:
    def __init__(self, sides):
        self.state = 'waiting'
        self.registered_players = {}
        self.sides = sides

        self.screen = None
        self.client = None

    def set_registered_players(self, players):
        self.registered_players = {}
        for player in players:
            self.registered_players[player.key] = player

    def reset(self):
        self.state = 'waiting'
        for side in self.sides:
            side.reset()
        self.screen.render('Scan RFID cards to start')

    def tick(self):
        for side in self.sides:
            event = side.get_event()
            if event == None:
                continue

            eventType = event.get('type', None)
            if self.state == 'waiting' and eventType == 'rfid':
                self.add_player(side, event['card'])
            elif self.state == 'running' and eventType == 'presence':
                self.register_goal(side)

    def add_player(self, target, key):
        if len(target.players) >= 2:
            self.screen.render('Team ' + target.name + ' is full')
            return

        if key not in self.registered_players:
            self.screen.render('Unknown player')
            return

        player = self.registered_players[key]
        for side in self.sides:
            if side != target and side.players.count(player) > 0:
                self.screen.render('Already registered')
                return

        target.players.append(player)
        self.screen.render('Player ' + player.name + ' joined team ' + target.name)

        teams_full = True
        for side in self.sides:
            if len(side.players) < 2:
                teams_full = False

        if teams_full:
            self.start_game()

    def start_game(self):
        self.state = 'running'
        self.started_at = get_datetime()
        self.render_score()

    def register_goal(self, receiver):
        for side in self.sides:
            if side == receiver:
                continue
            side.score += 1
            if side.score >= 10:
                self.end_game(side)
            else:
                self.render_score()

    def end_game(self, winner):
        self.screen.render('Team ' + winner.name + ' won')
        message = {
            'type': 'matchCompleted',
            'value': {
                'startedAt': self.started_at,
                'finishedAt': get_datetime(),
                'participants': []
            }
        }
        for side in self.sides:
            message['value']['participants'].append({
                'score': side.score,
                'players': [player.id for player in side.players]
            })

        self.client.publish('event-ingest', json.dumps(message))

        time.sleep(5)
        self.reset()

    def render_score(self):
        scores = [str(side.score) for side in self.sides]
        self.screen.render(':'.join(scores))

class Side:
    def __init__(self, name, sensor):
        self.name = name
        self.score = 0
        self.players = []
        self.sensor = sensor

    def get_event(self):
        return self.sensor.read()

    def reset(self):
        self.score = 0
        self.players = []

    def __eq__(self, other):
        return self.name == other.name

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    result = client.subscribe("devices/f0548d61-7307-4f3e-96df-2fdbd7c4e979/configuration")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    parsedMessage = json.loads(message.payload)
    if 'configuration' in parsedMessage and 'players' in parsedMessage['configuration']:
        with open('players.json', 'w') as outfile:
            json.dump(parsedMessage['configuration']['players'], outfile)
        load_players(parsedMessage['configuration']['players'])

def load_players(items):
    players = []
    for item in items:
        players.append(Player(item['id'], item['name'], item['key']))
    table.set_registered_players(players)

# Depends on which Arduino device is connected to USB, ls /dev/tty* will show the list
class FakeScreen:
    def render(self, text):
        print("PRINT: " + text)
class FakeSensor:
    def read(self):
        return random.choice([
            None,
            None,
            None,
            None,
            None,
            None,
            { 'type': 'presence' },
            { 'type': 'presence' },
            { 'type': 'rfid', 'card': '1' },
            { 'type': 'rfid', 'card': '2' },
            { 'type': 'rfid', 'card': '3' },
            { 'type': 'rfid', 'card': '4' },
            { 'type': 'rfid', 'card': 'fake' },
        ])
table = Table([
    Side('1', Sensor("/dev/ttyACM0")),
    Side('2', Sensor("/dev/ttyACM1")),
])

with open('players.json') as json_file:
    items = json.load(json_file)
    load_players(items)

client = mqtt.Client('smartkicker')
client.on_connect = on_connect
client.on_message = on_message
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(cafile = "olt_ca.pem")
ssl_context.load_cert_chain(certfile = 'device_cert.pem', keyfile = 'device_key.pem')
client.tls_set_context(context = ssl_context)
client.connect("mqtt.lightelligence.io", port = 8883)
client.loop_start()

table.screen = Screen()
table.client = client

while True:
    table.tick()
