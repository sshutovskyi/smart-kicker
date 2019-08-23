import json
import time
import ssl
import paho.mqtt.client as mqtt
import strict_rfc3339

def format_datetime(t):
    return strict_rfc3339.timestamp_to_rfc3339_utcoffset(int(t))

class Client:
    def __init__(self, players_container):
        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            result = client.subscribe("devices/f0548d61-7307-4f3e-96df-2fdbd7c4e979/configuration")

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, message):
            parsed_message = json.loads(message.payload)
            if 'configuration' in parsed_message and 'players' in parsed_message['configuration']:
                players_container.save(parsed_message['configuration']['players'])

        self.client = mqtt.Client('smartkicker')
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(cafile = "olt_ca.pem")
        ssl_context.load_cert_chain(certfile = 'device_cert.pem', keyfile = 'device_key.pem')
        self.client.tls_set_context(context = ssl_context)

    def connect(self):
        self.client.connect("mqtt.lightelligence.io", port = 8883)
        self.client.loop_start()

    def publish_finished(self, start_time, sides):
        message = {
            'type': 'matchCompleted',
            'value': {
                'startedAt': format_datetime(start_time),
                'finishedAt': format_datetime(time.time()),
                'participants': []
            }
        }
        for side in sides:
            message['value']['participants'].append({
                'score': side.score,
                'players': [player.id for player in side.players]
            })

        self.client.publish('event-ingest', json.dumps(message))
