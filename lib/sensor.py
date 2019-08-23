import serial
import json

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
