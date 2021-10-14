from object import GameObject
from animator import Animator
import pygame, os


class Life(GameObject):
    NAME = "life"

    IMG_WIDTH, IMG_HEIGHT = 16, 16

    WIDTH, HEIGHT = 10, 10
    ANIMATION_DELAY = 0.05

    def __init__(self, position):
        position = (position[0] + 11, position[1] + 11)

        super().__init__(position, (Life.WIDTH, Life.HEIGHT))
        self.imagerect = pygame.Rect(0, 0, Life.IMG_WIDTH, Life.IMG_HEIGHT)

        self.animations = Animator(Life.ANIMATION_DELAY)
        self.animations.load_from_filesystem(["resources/ui/heart.png",
                                              "resources/ui/heart2.png",
                                              "resources/ui/heart3.png",
                                              "resources/ui/heart4.png",
                                              "resources/ui/heart5.png",
                                              "resources/ui/heart6.png",
                                              "resources/ui/heart7.png",
                                              "resources/ui/heart8.png",
                                              "resources/ui/heart7.png",
                                              "resources/ui/heart6.png",
                                              "resources/ui/heart5.png",
                                              "resources/ui/heart4.png",
                                              "resources/ui/heart3.png",
                                              "resources/ui/heart2.png"])

        self.alive = True

    def draw(self, camera):
        self.imagerect.center = (int((self.left + self.right)/2), int((self.top + self.bottom)/2))
        camera.blit(self.animations.get_image(), self.imagerect)

    def update(self):
        pass

    def die(self):
        self.alive = False



