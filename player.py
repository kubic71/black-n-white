import pygame
import os
import time

from object import GameObject
from animator import Animator
from properties import Properties
from pygame.locals import *
from obstacle import Obstacle
from bullet import Bullet


class Player(GameObject):
    NAME = "player"

    RUNNING_RIGHT = "running_right"
    RUNNING_LEFT = "running_left"

    RUNNING_SPEED = 4

    # acceleration values should be between 0 and 1
    RUNNING_ACCELERATION = 0.02
    RUNNING_DECELERATION = 0.05
    JUMP_SPEED = 5
    JUMP_BOUNCE = 0.4

    RUNNING_ANIMATION_DELAY = 0.14

    IMG_WIDTH, IMG_HEIGHT = 32, 32

    INVINCIBILITY_TIME = 2

    # Player rectangle size used for detecting collisions
    PLAYER_WIDTH, PLAYER_HEIGHT = 15, 30

    img_standing = pygame.image.load(os.path.join("resources/player/standing.png"))

    def __init__(self, position, collision_engine):
        super().__init__(position, (Player.PLAYER_WIDTH, Player.PLAYER_HEIGHT))
        self.imagerect = Player.img_standing.get_rect()
        self.imagerect.size = (Player.IMG_WIDTH, Player.IMG_HEIGHT)
        self.collision_engine = collision_engine

        self.animations = {}
        self.load_animations()

        self.keyboard_state = None

        self.running_left = False
        self.running_right = False

        self.vx = 0
        self.vy = 0

        self.lives = 3
        self.shots = 5

        self.invincible_until = 0
        self.invincible = False

        self.score = 0
        self.finished = False


        # TODO
        # self.img = img

    def draw(self, camera):
        self.imagerect.center = (int((self.left + self.right)/2), int((self.top + self.bottom)/2))

        img = None
        if self.running_right:
            img = self.animations[Player.RUNNING_RIGHT].get_image()
        elif self.running_left:
            img = self.animations[Player.RUNNING_LEFT].get_image()
        else:
            img = self.img_standing

        # holding both left and right keyboard arrow
        if self.running_right and self.running_left:
            img = Player.img_standing

        if self.invincible:
            if (time.time() % 0.1) > 0.05:
                camera.blit(img, self.imagerect)
        else:
            camera.blit(img, self.imagerect)

        # TODO debug
        # self.draw_boundary(camera)

    def jump(self):
        if self.is_touching_ground():
            self.vy = -abs(self.vy) - Player.JUMP_SPEED

            # player can't gain more than 25% more velocity on second jump
            self.vy = max(self.vy, -Player.JUMP_SPEED*1.25)

    def update(self):
        #print(self.x, self.y)
        # accelerating left
        if self.invincible_until < time.time():
            self.invincible = False

        self.check_fall()

        if self.keyboard_state.is_pressed(K_LEFT):
            self.vx += (-Player.RUNNING_SPEED - self.vx) * Player.RUNNING_ACCELERATION
            self.running_left = True
        else:
            self.running_left = False

        # accelerating right
        if self.keyboard_state.is_pressed(K_RIGHT):
            self.vx += (Player.RUNNING_SPEED - self.vx) * Player.RUNNING_ACCELERATION
            self.running_right = True
        else:
            self.running_right = False

        # decelerating
        if (not self.running_left) and (not self.running_right):
            self.vx *= (1 - Player.RUNNING_DECELERATION)

        self.vy += Properties.GRAVITY

        # try to move horizontally and see, if you collided
        self.x += self.vx
        # checking collisions
        for obj in self.get_collided_objects():
            if obj.NAME == "life":
                self.lives += 1
                obj.die()

            elif obj.NAME == "gun":
                self.shots += 10
                obj.die()

            elif obj.NAME == "finish":
                self.finished = True


            # Obstacle cannot be walked through
            if not self.can_walk_through_object(obj):
                if self.left < obj.right < self.right:
                    self.left = obj.right
                    self.vx = -self.vx * Player.JUMP_BOUNCE

                elif self.left < obj.left < self.right:
                    self.right = obj.left
                    self.vx = -self.vx * Player.JUMP_BOUNCE

        # try to move vertically and see, if you collided
        self.y += self.vy
        for obj in self.get_collided_objects():
            # Obstacle cannot be walked through
            if not self.can_walk_through_object(obj):

                if self.bottom > obj.top > self.top:
                    self.bottom = obj.top
                    self.vy = -self.vy * Player.JUMP_BOUNCE

                elif self.bottom > obj.bottom > self.top:
                    self.top = obj.bottom
                    self.vy = -self.vy * Player.JUMP_BOUNCE

        self.handle_damaging_collisions()

    def check_fall(self):
        if self.y > 3000:
            self.y = 0
            self.vy = -5
            self.vx = 0
            self.die()

    def handle_damaging_collisions(self):
        # try to move to the left
        move_step = 3
        self.x += move_step
        for obj in self.get_collided_objects():
            if obj.NAME == "baddie" or (obj.NAME == "spike" and obj.current != 0):
                self.die()

        self.x -= 2*move_step
        for obj in self.get_collided_objects():
            if obj.NAME == "baddie" or (obj.NAME == "spike" and obj.current != 0):
                self.die()
        self.x += move_step

        self.y += move_step
        for obj in self.get_collided_objects():
            if obj.NAME == "baddie":
                if not obj.dying:
                    self.score += obj.KILL_SCORE
                obj.die()
            elif obj.NAME == "spike" and obj.current != 0:
                self.die()

        self.y -= 2*move_step
        for obj in self.get_collided_objects():
            if obj.NAME == "baddie" or (obj.NAME == "spike" and obj.current != 0):
                self.die()
        self.y += move_step

    def fire(self, direction):
        if self.shots == 0:
            return
        self.shots -= 1

        target = self.center_x + direction[0], self.center_y + direction[1]

        bullet = Bullet((self.center_x, self.center_y), target, fired_by="player", collision_engine=self.collision_engine)
        self.game_objects.add(bullet)

    def fire_right(self):
        self.fire((10, 0))

    def fire_left(self):
        self.fire((-10, 0))

    def fire_down(self):
        self.fire((0, 10))

    def fire_up(self):
        self.fire((0, -10))

    def is_touching_ground(self):
        # try to move a little bit down and see, if you collide with obstacle
        move_size = 10
        self.y += move_size

        for obj in self.get_collided_objects():
            if obj.NAME in ("obstacle", "baddie"):
                self.y -= move_size
                return True
        self.y -= move_size
        return False

    @staticmethod
    def can_walk_through_object(obj):
        return obj.NAME not in ["baddie", "obstacle"]

    def get_collided_objects(self):
        result = []
        for obj in self.collision_engine.get_near_objects(self):
            if self.collided_with(obj):
                result.append(obj)
        return result

    def load_animations(self):
        self.animations = {}

        self.animations[Player.RUNNING_RIGHT] = Animator(Player.RUNNING_ANIMATION_DELAY)
        self.animations[Player.RUNNING_RIGHT].load_from_filesystem(["resources/player/running-right1.png", "resources/player/running-right2.png"])

        self.animations[Player.RUNNING_LEFT] = Animator(Player.RUNNING_ANIMATION_DELAY)
        self.animations[Player.RUNNING_LEFT].load_from_filesystem(["resources/player/running-left1.png", "resources/player/running-left2.png"])

    def set_keyboard_state_memory(self, keyboard_state_memory):
        self.keyboard_state = keyboard_state_memory

    def set_game_objects(self, game_objects):
        self.game_objects = game_objects

    def die(self):
        if self.invincible:
            return

        self.lives -= 1
        self.invincible_until = time.time() + Player.INVINCIBILITY_TIME
        self.invincible = True