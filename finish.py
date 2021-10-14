from object import GameObject
from animator import Animator
import pygame, os
import colors


class Finish(GameObject):
    NAME = "finish"

    WIDTH, HEIGHT = 32, 32
    ANIMATION_DELAY = 0.05

    def __init__(self, position):
        super().__init__(position, (Finish.WIDTH, Finish.HEIGHT))

        self.radiuses = [i for i in range(0, 24, 6)]
        self.frame = 0

    def draw(self, camera):
        thickness = 3
        for rad in self.radiuses:
            if rad >= thickness:
                camera.draw_circle(colors.BLACK, (self.center_x, self.center_y), rad, width=thickness)

    def update(self):
        self.frame += 1

        if self.frame % 3 == 0:
            for i in range(len(self.radiuses)):
                self.radiuses[i] = (self.radiuses[i] + 1) % 24

    def die(self):
        self.alive = False



