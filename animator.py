import time
import pygame


class Animator:
    # Takes care of automatic animation of sprite's images with constant time delay

    def __init__(self, delay = 0.3):
        self.delay = delay
        self.last_change = time.time()
        self.images = []
        self.current_image = 0


    def reset(self):
        self.current_image = 0
        self.last_change = time.time()

    def set_delay(self, delay):
        self.delay = delay

    def get_image(self):
        delta = time.time() - self.last_change
        if delta > self.delay:
            self.current_image = (self.current_image + int(delta / self.delay)) % len(self.images)
            self.last_change = time.time() - (delta % self.delay)

        return self.images[self.current_image]

    def load_from_filesystem(self, image_paths):
        # image_paths list must be in correct order
        for path in image_paths:
            self.images.append(pygame.image.load(path))

    def set_images(self, images):
        # set images list, if they are already loaded
        self.images = images


