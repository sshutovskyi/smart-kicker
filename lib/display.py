import pygame
import lib.screen

class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode()

        self.state = 'none'
        self.current_screen = None

        self.welcome_screen()

    def welcome_screen(self):
        if self.state != 'welcome':
            self.current_screen = WelcomeScreen(self.screen)
            self.state = 'welcome'
        return self.current_screen

    def game_screen(self):
        if self.state != 'game':
            self.current_screen = GameScreen(self.screen)
            self.state = 'game'
        return self.current_screen

    def refresh(self):
        if self.current_screen:
            self.current_screen.refresh()
