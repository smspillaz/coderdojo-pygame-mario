import pygame_sdl2 as pygame
from helpers import *
from pygame_sdl2.locals import *
import math
import time
import sys

pygame.display.set_caption("Super Mario Test")
screen = pygame.display.set_mode((640, 480))

class TileGrid(object):
    def __init__(self, screen):
        super(TileGrid, self).__init__()
        screen_size = screen.get_size()
        self.grid_width = screen_size[0] // 16
        self.grid_height = screen_size[1] // 16
        self.grid = [None for i in range(0, self.grid_width * self.grid_height)]

        self.left_tile_image, self.left_tile_rect = load_image("ground_tiles_1_1.png")
        self.center_tile_image, self.center_tile_rect = load_image("ground_tiles_1_2.png")
        self.right_tile_image, self.right_tile_rect = load_image("ground_tiles_1_3.png")
        self.ground_tile_image, self.ground_tile_rect = load_image("ground_tiles_1_4.png")



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
