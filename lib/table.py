import time

class Table:
    def __init__(self, sides, players_container):
        self.state = 'waiting'
        self.players_container = players_container
        self.sides = sides

        self.display = None
        self.client = None

    def reset(self):
        self.state = 'waiting'
        for side in self.sides:
            side.reset()
        self.display.welcome_screen()

    def tick(self):
        self.display.refresh()
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
            self.display.game_screen().alert(target.index, 'Team ' + target.name + ' is full')
            return

        player = self.players_container.get(key)
        if not player:
            self.display.game_screen().alert(target.index, 'Unknown player')
            return

        for side in self.sides:
            if side != target and side.players.count(player) > 0:
                self.display.game_screen().alert(target.index, 'Already registered')
                return

        target.players.append(player)
        self.display.game_screen().alert(target.index, 'Player ' + player.name + ' joined team ' + target.name)
        self.display.game_screen().add_player(target.index, player.name)

        teams_full = True
        for side in self.sides:
            if len(side.players) < 2:
                teams_full = False

        if teams_full:
            self.start_game()

    def start_game(self):
        self.state = 'running'
        self.started_at = time.time()
        self.display.game_screen()

    def register_goal(self, receiver):
        for side in self.sides:
            if side == receiver:
                continue
            self.display.game_screen().add_score(side.index)
            side.score += 1
            if side.score >= 10:
                self.end_game(side)

    def end_game(self, winner):
        self.display.game_screen().alert(winner.index, 'Team ' + winner.name + ' won')
        self.client.publish_finished(self.started_at, self.sides)

        time.sleep(5)
        self.reset()
