#!/usr/bin/env python

import serial
import pygame
import os

# Depends on which Arduino device is connected to USB, ls /dev/tty* will show the list
port1 = "/dev/ttyACM0"
port2 = "/dev/ttyACM1"

s1 = serial.Serial(port1, 9600)
s1.flushInput()

s2 = serial.Serial(port2, 9600)
s2.flushInput()

inputValue1 = ""
inputValue2 = ""
character1 = ""
character2 = ""
WHITE = (255, 255, 255)
os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()
lcd = pygame.display.set_mode((900, 700))
lcd.fill((255, 0, 0))
pygame.mouse.set_visible(False)
pygame.display.update()
font_big = pygame.font.Font(None, 60)
lcd.fill((0, 0, 0))
text_surface = font_big.render('Hatem', True, WHITE)
rect = text_surface.get_rect(center=(240, 160))
lcd.blit(text_surface, rect)
pygame.display.update()

while True:
    if s1.inWaiting() > 0 :
        character1 = s1.read(1)
        inputValue1 += character1
        if '}' in character1 :
            print(inputValue1)
            lcd.fill((0, 0, 50))
            text_surface = font_big.render(inputValue1.strip(), True, WHITE)
            rect = text_surface.get_rect(center=(500, 300))
            lcd.blit(text_surface, rect)
            pygame.display.update()
            inputValue1 = ""
    if s2.inWaiting() > 0 :
        character2 = s2.read(1)
        inputValue2 += character2
        if '}' in character2 :
            print(inputValue2)
            lcd.fill((0, 0, 50))
            text_surface = font_big.render(inputValue2.strip(), True, WHITE)
            rect = text_surface.get_rect(center=(500, 300))
            lcd.blit(text_surface, rect)
            pygame.display.update()
            inputValue2 = ""
