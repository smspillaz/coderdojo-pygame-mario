import pygame_sdl2 as pygame
from helpers import *
from pygame_sdl2.locals import *
import math
import time
import sys

pygame.display.set_caption("Super Mario Test")
screen = pygame.display.set_mode((640, 480))

def make_background(image_name, screen):
    background, background_rect = load_image(image_name)
    background_rect.width, background_rect.height = screen.get_size()
    return pygame.transform.scale(background,
                                  (background_rect.width,
                                   background_rect.height))

background = make_background("background.png", screen)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key in (K_RIGHT, K_LEFT):
                pass

    screen.blit(background, (0, 0))
    pygame.display.flip()
    time.sleep(16.66 / 1000)
