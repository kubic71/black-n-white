from object import GameObject
from animator import Animator
import pygame, os


class Bullet(GameObject):
    NAME = "bullet"

    IMG_WIDTH, IMG_HEIGHT = 8, 8

    WIDTH, HEIGHT = 8, 8
    ANIMATION_DELAY = 0.04
    FLY_TIME = 70 # number of frames
    SPEED = 8


    def __init__(self, position, target, fired_by, collision_engine):

        position = (position[0] - 4, position[1] - 4)
        super().__init__(position, (Bullet.WIDTH, Bullet.HEIGHT))

        dx, dy = target[0] - self.center_x, target[1] - self.center_y
        self.vx, self.vy = self.scale(dx, dy, Bullet.SPEED)

        self.alive = True
        self.imagerect = pygame.Rect(0, 0, Bullet.IMG_WIDTH, Bullet.IMG_HEIGHT)

        self.animations = Animator(Bullet.ANIMATION_DELAY)
        self.animations.load_from_filesystem(["resources/bullet/bullet1.png",
                                              "resources/bullet/bullet2.png",
                                              "resources/bullet/bullet3.png",
                                              "resources/bullet/bullet4.png",
                                              "resources/bullet/bullet5.png",
                                              "resources/bullet/bullet6.png",
                                              "resources/bullet/bullet7.png",
                                              "resources/bullet/bullet8.png"])

        self.fired_by = fired_by
        self.collision_engine = collision_engine

    def draw(self, camera):
        self.imagerect.center = (self.center_x, self.center_y)
        camera.blit(self.animations.get_image(), self.imagerect)

    def scale(self, dx, dy, lenght):
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        return dx / magnitude * lenght, dy / magnitude * lenght

    def distance_to_player(self):
        return ((self.x - self.player.x)**2 + (self.y - self.player.y) ** 2) ** 0.5

    def update(self, player):
        self.x += self.vx
        self.y += self.vy

        self.FLY_TIME -= 1
        if self.FLY_TIME == 0:
            self.alive = False

        for obj in self.collision_engine.get_colliding_objects(self):
            if obj.NAME == "obstacle":
                self.alive = False
            elif obj.NAME == "player" and self.fired_by == "baddie":
                self.alive = False
                obj.die()
            elif obj.NAME == "baddie" and not obj.dying and self.fired_by == "player":
                obj.die()
                player.score += obj.KILL_SCORE
                self.alive = False



