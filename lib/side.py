class Side:
    def __init__(self, index, name, sensor):
        self.index = index
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
