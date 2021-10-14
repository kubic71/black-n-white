from object import GameObject
import pygame, os


class Obstacle(GameObject):
    NAME = "obstacle"

    img = pygame.image.load(os.path.join("resources/wall.png"))

    def __init__(self, position, size):
        super().__init__(position, size)
        self.imagerect = Obstacle.img.get_rect()
        self.imagerect.size = size

        # TODO
        # self.img = img

    def draw(self, camera):
        self.imagerect.topleft = self.position
        camera.blit(Obstacle.img, self.imagerect)







