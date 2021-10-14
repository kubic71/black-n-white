from object import GameObject
from animator import Animator
import pygame, os, random


class Spike(GameObject):
    NAME = "spike"

    IMG_WIDTH, IMG_HEIGHT = 32, 32

    SPEED = 8

    LENGHT = 30
    WIDTH = 14

    def __init__(self, position, type):
        self.tile_position = position
        super().__init__(position, (Spike.WIDTH, Spike.LENGHT))

        self.type = type

        self.imagerect = pygame.Rect(0, 0, Spike.IMG_WIDTH, Spike.IMG_HEIGHT)
        self.imagerect.topleft = self.tile_position

        folders = {">": "left", "<": "right", "^":"bottom", "v":"up"}
        folder_name = folders[self.type]

        self.spike_images = [
                        pygame.image.load("resources/spike/" + folder_name + "/spike0.png"),
                        pygame.image.load("resources/spike/" + folder_name + "/spike1.png"),
                        pygame.image.load("resources/spike/" + folder_name + "/spike2.png"),
                        pygame.image.load("resources/spike/" + folder_name + "/spike3.png"),
                        pygame.image.load("resources/spike/" + folder_name + "/spike4.png")]

        self.sequence = [0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0, 0, 0]
        self.sequence_index = random.randint(0, len(self.sequence) - 1)
        self.current = self.sequence[self.sequence_index]
        self.frame = 0

    def draw(self, camera):
        camera.blit(self.spike_images[self.current], self.imagerect)
        # self.draw_boundary(camera)

    def update_object_dimensions(self):
        if self.type == ">":
            self.x = self.tile_position[0]
            self.y = self.tile_position[1] + (32 - self.WIDTH) / 2
            self.size = (self.current * 1/4 * self.LENGHT, self.WIDTH)

        elif self.type == "<":
            self.size = (self.current * 1 / 4 * self.LENGHT, self.WIDTH)
            self.right = self.tile_position[0] + 32
            self.y = self.tile_position[1] + (32 - self.WIDTH) / 2

        elif self.type == "v":
            self.x = self.tile_position[0] + (32 - self.WIDTH) / 2
            self.y = self.tile_position[1]
            self.size = (self.WIDTH, self.current * 1/4 * self.LENGHT )

        elif self.type == "^":
            self.size = (self.WIDTH, self.current * 1/4 * self.LENGHT)
            self.x = self.tile_position[0] + (32 - self.WIDTH) / 2
            self.bottom = self.tile_position[1] + 32

    def update(self):
        self.frame += 1
        if self.frame % 10 == 0:
            self.sequence_index += 1
            self.sequence_index %= len(self.sequence)
            self.current = self.sequence[self.sequence_index]

        self.update_object_dimensions()

        


