from object import GameObject
from animator import Animator
import pygame, os


class Gun(GameObject):
    NAME = "gun"

    IMG_WIDTH, IMG_HEIGHT = 32, 32

    WIDTH, HEIGHT = 25, 25
    ANIMATION_DELAY = 0.05

    def __init__(self, position):
        position = (position[0] + 3, position[1] + 3)

        super().__init__(position, (Gun.WIDTH, Gun.HEIGHT))
        self.imagerect = pygame.Rect(0, 0, Gun.IMG_WIDTH, Gun.IMG_HEIGHT)

        self.animations = Animator(Gun.ANIMATION_DELAY)

        images = []
        for i in range(1, 17):
            images.append("resources/gun/gun{}.png".format(i))

        for i in range(15, 1, -1):
            images.append("resources/gun/gun{}.png".format(i))

        self.animations.load_from_filesystem(images)
        self.alive = True

    def draw(self, camera):
        self.imagerect.center = (self.center_x, self.center_y)
        camera.blit(self.animations.get_image(), self.imagerect)

    def update(self):
        pass

    def die(self):
        self.alive = False



