#! /usr/bin/env python
import os
import pygame_sdl2 as pygame
from pygame_sdl2.locals import *
import math


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise (SystemExit, message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

chroma_key = (0x8B, 0x8E, 0x8E)


def load_keyed_image(image):
    return load_image(image, colorkey=chroma_key)


class PhysicsBody(object):
    def __init__(self, rects, ground_y_position):
        self.velocity = (0, 0)
        self.acceleration = (0, 0)
        self.friction_multiplier = (0, 0)
        self.direction = K_RIGHT
        self._rect_refs = rects
        self._ground_y_position = ground_y_position

    @staticmethod
    def clamp(value, left, right):
        if value > right:
            return right
        if value < left:
            return left

        return value

    def touching_ground(self):
        if self._rect_refs[0].bottom == self._ground_y_position:
            return True

        return False

    def integrate(self):
        resolved_friction_multipler = self.friction_multiplier
        if not self.touching_ground():
            resolved_friction_multipler = (0, 0)

        self.velocity = (self.velocity[0] + 0.5 * self.acceleration[0],
                         self.velocity[1] + 0.5 * self.acceleration[1])
        self.velocity = (PhysicsBody.clamp(self.velocity[0], -20, 20),
                         PhysicsBody.clamp(self.velocity[1], -50, 20))

        # After integration, reset acceleration
        self.acceleration = (0, 0)

        # Check y position to make sure we haven't gone under the ground
        if (self._rect_refs[0].bottom == self._ground_y_position and
                self.velocity[1] > 0):
            self.velocity = (self.velocity[0], 0)
            self.acceleration = (self.acceleration[0], 0)

        # Stop check for x and y velocity
        if math.fabs(self.velocity[0]) <= 3 and resolved_friction_multipler[0] != 0:
            self.velocity = (0, self.velocity[1])
            self.acceleration = (0, self.acceleration[1])
            self.friction_multiplier = (0, self.friction_multiplier[1])
            return False
        else:
            # Apply friction and gravity
            self.acceleration = (self.acceleration[0] + (self.velocity[0] / 50.0) *
                                 resolved_friction_multipler[0],
                                 self.acceleration[1] + (self.velocity[1] / 50.0) *
                                 resolved_friction_multipler[1])

            if not self.touching_ground():
                self.acceleration = (self.acceleration[0],
                                     self.acceleration[1] + 9.8)

        return True
