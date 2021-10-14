import colors
import pygame
from pygame.locals import *


class GameObject:
    NAME = "object"

    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.color = colors.WHITE

    # returns true, if object rectangle collides with another object
    def collided_with(self, game_object):
        if self.left < game_object.right and self.right > game_object.left and self.bottom > game_object.top and self.top < game_object.bottom:
            return True
        return False

    # returns true, if point is inside object rectangle
    @staticmethod
    def point_collided(obj, point):
        if obj.left < point[0] < obj.right and obj.top < point[1] < obj.bottom:
            return True
        else:
            return False

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, x):
        y = self.position[1]
        self.position = (x, y)

    @property
    def y(self):
        return self.position[1]

    @property
    def center_x(self):
        return self.position[0] + self.size[0] / 2

    @property
    def center_y(self):
        return self.position[1] + self.size[1] / 2

    @y.setter
    def y(self, y):
        x = self.position[0]
        self.position = (x, y)

    @property
    def left(self):
        return self.position[0]

    @left.setter
    def left(self, left):
        self.x = left

    @property
    def right(self):
        return self.position[0] + self.size[0]

    @right.setter
    def right(self, right):
        self.x = right - self.size[0]

    @property
    def top(self):
        return self.position[1]

    @top.setter
    def top(self, top):
        self.y = top

    @property
    def bottom(self):
        return self.position[1] + self.size[1]

    @bottom.setter
    def bottom(self, bottom):
        self.y = bottom - self.size[1]

    # Engine calls self.update() on object after every frame render
    def update(self):
        pass

    # engine passes object pygame screen instance, on which object is supposed to draw itself
    def draw(self, camera):
        camera.draw_rect(self.color, Rect(self.position, self.size))

    def draw_boundary(self, camera):
        camera.draw_rect(colors.RED, Rect(self.position, self.size), 2)








