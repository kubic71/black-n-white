from pygame.locals import *
from properties import Properties
import pygame


class Camera:
    MOVEMENT_SENSITIVY = 0.1

    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.vy = 0
        self.vx = 0



        self.inner_left = 0
        self.inner_right = 0
        self.inner_top = 0
        self.inner_bottom = 0

        self.following = None

    def blit(self, img, rect):
        shifted_rect = Rect(rect.left - self.x, rect.top - self.y, rect.width, rect.height)
        self.screen.blit(img, shifted_rect)

    def follow(self, obj):
        self.following = obj

    def update(self):
        self.inner_left = self.x + Properties.WINDOW_WIDTH / 3
        self.inner_right = self.x + Properties.WINDOW_WIDTH * 2/3
        self.inner_top = self.y + Properties.WINDOW_HEIGHT / 3
        self.inner_bottom = self.y + Properties.WINDOW_HEIGHT * 2/3

        if self.following.right > self.inner_right:
            self.vx = (self.following.right - self.inner_right) * Camera.MOVEMENT_SENSITIVY
        elif self.following.left < self.inner_left:
            self.vx = (self.following.left - self.inner_left) * Camera.MOVEMENT_SENSITIVY
        else:
            self.vx = 0

        if self.following.bottom > self.inner_bottom:
            self.vy = (self.following.bottom - self.inner_bottom) * Camera.MOVEMENT_SENSITIVY
        elif self.following.top < self.inner_top:
            self.vy = (self.following.top - self.inner_top) * Camera.MOVEMENT_SENSITIVY
        else:
            self.vy = 0
    
        self.x += self.vx
        self.y += self.vy

    def draw_rect(self, color, rect, width=0):
        shifted_rect = Rect(rect.left - self.x, rect.top - self.y, rect.width, rect.height)
        pygame.draw.rect(self.screen, color, shifted_rect, width)

    def get_shifted_position(self, position):
        return position[0] - self.x, position[1] - self.y

    def draw_circle(self, color, position, radius, width=0):
        position = tuple(map(int, self.get_shifted_position(position)))
        pygame.draw.circle(self.screen, color, position, radius, width)



