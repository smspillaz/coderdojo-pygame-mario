import pygame_sdl2 as pygame
from helpers import *
from pygame_sdl2.locals import *
import math
import time
import sys

pygame.display.set_caption("Super Mario Test")
screen = pygame.display.set_mode((640, 480))


class Mario(pygame.sprite.Sprite, PhysicsBody):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self._images, self._rects = zip(*[load_keyed_image("mario_sprite_1.png"),
                                          load_keyed_image("mario_sprite_2.png"),
                                          load_keyed_image("mario_sprite_3.png")])

        PhysicsBody.__init__(self, self._rects, screen.get_rect().height - 32)

        self.switch_to_stationary_sprite()

        # Start in the bottom-left corner
        for rect in self._rects:
            rect.y = screen.get_height() - (self.rect.height + 32)

    def update_sprite(self):
        self.image = self._images[self._active_sprite]
        self.rect = self._rects[self._active_sprite]

    def switch_to_stationary_sprite(self):
        self._active_sprite = 0
        self.update_sprite()

    def apply_direction(self, direction):
        if self.direction != direction:
            self._images = [pygame.transform.flip(i, True, False)
                            for i in self._images]
            self.direction = direction
            self.come_to_stop()
            return True

        return False

    def come_to_stop(self):
        # Determine what kind of friction to apply
        if self.direction == K_RIGHT:
            if self.velocity[0] > 0:
                self.friction_multiplier = (-5, self.velocity[1])
            elif self.velocity[0] < 0:
                self.friction_multiplier = (-10, self.velocity[1])
                self.switch_to_stationary_sprite()
        elif self.direction == K_LEFT:
            if self.velocity[0] > 0:
                self.friction_multiplier = (-10, self.velocity[1])
                self.switch_to_stationary_sprite()
            elif self.velocity[0] < 0:
                self.friction_multiplier = (-5, self.velocity[1])

    def move(self, key):
        amount = (0.5, 0.5)
        direction = dict([
            (K_RIGHT, (1, 0)),
            (K_LEFT, (-1, 0))
        ])

        # Check if we should finish coming to a stop first
        if self.friction_multiplier[0] != 0:
            self.come_to_stop()
        else:
            self.acceleration = (self.acceleration[0] + amount[0] * direction[key][0],
                                 self.acceleration[1] + amount[1] * direction[key][1])

    def apply_movement(self, screen):
        if self.velocity[0] != 0:
            if math.fabs(self.velocity[0]) > 2:
                # Always pick between running sprites
                self._active_sprite = (self._active_sprite % 2) + 1
            else:
                self._active_sprite = (self._active_sprite + 1) % 3
            self.update_sprite()

        for rect in self._rects:
            rect.move_ip(self.velocity[0], self.velocity[1])
            rect.bottom = PhysicsBody.clamp(rect.bottom, 0, screen.get_height() - 32)


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

        # Now, populate the bottom part of the grid with floor tiles

        # The grassy part of the floor
        self.grid[(self.grid_height - 2) * self.grid_width] = self.left_tile_image
        self.grid[(self.grid_height - 1) * self.grid_width - 1] = self.right_tile_image
        for i in range(0, self.grid_width - 2):
            self.grid[(self.grid_height - 2) * self.grid_width + 1 + i] = self.center_tile_image

        # The solid part of the floor
        for i in range(0, self.grid_width):
            self.grid[(self.grid_height - 1) * self.grid_width + i] = self.ground_tile_image

    def draw(self, screen):
        for index, tile in enumerate(self.grid):
            if not tile:
                continue

            x_grid_position = index % self.grid_width
            y_grid_position = index // self.grid_width

            screen.blit(tile, (x_grid_position * 16, y_grid_position * 16))


def make_background(image_name, screen):
    background, background_rect = load_image(image_name)
    background_rect.width, background_rect.height = screen.get_size()
    return pygame.transform.scale(background,
                                  (background_rect.width,
                                   background_rect.height))

background = make_background("background.png", screen)
tile_grid = TileGrid(screen)
mario = Mario(screen)
mario_sprites = pygame.sprite.RenderPlain(mario)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key in (K_RIGHT, K_LEFT):
                if not mario.apply_direction(event.key):
                    mario.move(event.key)
        if event.type == KEYUP:
            if event.key in (K_RIGHT, K_LEFT):
                mario.come_to_stop()

    # Physics
    if not mario.integrate():
        mario.switch_to_stationary_sprite()
    else:
        mario.apply_movement(screen)

    screen.blit(background, (0, 0))
    tile_grid.draw(screen)
    mario_sprites.draw(screen)
    pygame.display.flip()
    time.sleep(16.66 / 1000)
