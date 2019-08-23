import pygame
import time

from .screen import Screen

COLOR_WHITE = (255, 255, 255)
COLOR_OLT = (255, 102, 0)

def get_centered_position(screen, obj):
    w, h = screen.get_size()
    x = (w - obj.get_width()) // 2
    y = (h - obj.get_height()) // 2
    return (x, y)

class GameScreen(Screen):
    def __init__(self, screen):
        self.screen = screen
        w, h = screen.get_size()
        self.font = pygame.font.SysFont(None, min(h // 6, 100))
        self.score_font = pygame.font.SysFont(None, min(h // 3, 200))
        self.alert_font = pygame.font.SysFont(None, min(h // 4, 40))
        self.team1 = []
        self.team2 = []
        self.rollback_at = None
        self.score1 = 0
        self.score2 = 0
        self.main()

    def main(self):
        self.rollback_at = None
        self.screen.fill(COLOR_OLT)
        w, h = self.screen.get_size()
        # render team 1
        point_length = h // 10
        point_padding = point_length // 10
        point_size = (point_length - 2 * point_padding)

        for i in range(self.score1):
            shape = pygame.draw.rect(self.screen, COLOR_WHITE, (
                2 * point_padding, h - ((i + 1) * point_length),
                point_size, point_size,
            ))
        score_text = self.score_font.render(str(self.score1), True, COLOR_WHITE)
        self.screen.blit(score_text, (
            point_length + 10,
            h - 2 * point_padding - score_text.get_height()
        ))
        for i, player in enumerate(self.team1):
            if player:
                text = self.font.render(player, True, COLOR_WHITE)
                self.screen.blit(text, (
                    point_length + 10 + score_text.get_width() + 10,
                    h - ((i + 1) * (text.get_height() + 2 * point_padding)))
                )

        # render team 2
        for i in range(self.score2):
            shape = pygame.draw.rect(self.screen, COLOR_WHITE, (
                (w - point_length), (2 * point_padding + i * point_length),
                point_size, point_size,
            ))
        score_text = self.score_font.render(str(self.score2), True, COLOR_WHITE)
        # score_text = pygame.transform.rotate(score_text, 180)
        self.screen.blit(score_text, (w - (score_text.get_width() + 10 + point_length), 2 * point_padding))
        for i, player in enumerate(self.team2):
            if player:
                text = self.font.render(player, True, COLOR_WHITE)
                # text = pygame.transform.rotate(text, 180)
                self.screen.blit(text,
                    (w - (text.get_width() + point_length + 10 + score_text.get_width() + 10),
                    2 * point_padding + i * (text.get_height() + 10)))

        pygame.display.flip()

    def add_player(self, team, name):
        if team == 1:
            self.team1.append(name)
        elif team == 2:
            self.team2.append(name)

        self.main()

    def add_score(self, team):
        if team == 1:
            self.score1 += 1
        elif team == 2:
            self.score2 += 1

        self.main()

    def alert(self, team, message, duration=0):
        text = self.font.render(message, True, COLOR_WHITE)
        # if team == 2:
        #     text = pygame.transform.rotate(text, 180)
        self.screen.blit(text, get_centered_position(self.screen, text))
        pygame.display.flip()

        if duration > 0:
            self.rollback_at = time.time() + duration

    def refresh(self):
        if self.rollback_at:
            if time.time() > self.rollback_at:
                self.rollback_at = None
                self.main()
