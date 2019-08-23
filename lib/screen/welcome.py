import pygame
from .screen import Screen

COLOR_WHITE = (255, 255, 255)
COLOR_OLT = (255, 102, 0)

class WelcomeScreen(Screen):
    def __init__(self, screen):
        self.screen = screen
        self.main()

    def main(self):
        self.screen.fill(COLOR_OLT)
        w, h = self.screen.get_size()

        image = pygame.image.load('logo.png')
        self.screen.blit(image, ((w - image.get_width()) // 2, 20))

        font = pygame.font.SysFont(None, min(h // 4, 100))
        title = font.render("SMART KICKER", True, COLOR_WHITE)
        self.screen.blit(title, ((w - title.get_width()) // 2, 20 + image.get_height()))

        font = pygame.font.SysFont(None, title.get_height() // 2)
        subtitle = font.render("scan RFID to start", True, COLOR_WHITE)
        self.screen.blit(subtitle, ((w - subtitle.get_width()) // 2, 20 + image.get_height() + title.get_height()))
        pygame.display.flip()
