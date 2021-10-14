import pygame

from object import GameObject
from animator import Animator
from properties import Properties
import colors
import time

import random


class Baddie(GameObject):
    NAME = "baddie"

    RUNNING_RIGHT = "running_right"
    RUNNING_LEFT = "running_left"
    STANDING = "standing"

    RUNNING_SPEED = 2

    # acceleration values should be between 0 and 1
    RUNNING_ACCELERATION = 0.02
    RUNNING_DECELERATION = 0.05
    JUMP_SPEED = 5
    JUMP_BOUNCE = 0.4

    ACTIVE_RADIUS = 1000
    SIGHT_RADIUS = 700

    DYING_TIME = 0.3

    RUNNING_ANIMATION_DELAY = 0.14

    IMG_WIDTH, IMG_HEIGHT = 32, 32

    KILL_SCORE = 3

    # Player rectangle size used for detecting collisions
    WIDTH, HEIGHT = 20, 30

    def __init__(self, position, collision_engine, game_instance):
        super().__init__(position, (Baddie.WIDTH, Baddie.HEIGHT))
        self.imagerect = pygame.Rect(0, 0, Baddie.IMG_WIDTH, Baddie.IMG_HEIGHT)

        self.collision_engine = collision_engine

        self.running_left = False
        self.running_right = False

        self.vx = 0
        self.vy = 0

        self.steps = 0

        self.animations = {}
        self.game_objects = []

        self.load_animations()

        self.dying = False
        self.when_to_die = 0

        self.last_seen_player = 0

        self.alive = True

        self.game_instance = game_instance

    def draw(self, camera):
        self.imagerect.center = (int((self.left + self.right)/2), int((self.top + self.bottom)/2))

        img = None
        if self.running_right:
            img = self.animations[Baddie.RUNNING_RIGHT].get_image()
        elif self.running_left:
            img = self.animations[Baddie.RUNNING_LEFT].get_image()
        else:
            img = self.animations[Baddie.STANDING].get_image()

        if self.dying:
            if (time.time() % 0.1) > 0.03:
                camera.blit(img, self.imagerect)
        else:
            camera.blit(img, self.imagerect)

        # TODO debug
        # self.draw_boundary(camera)

    def jump(self):
        if self.is_touching_ground():
            self.vy = -abs(self.vy) - Baddie.JUMP_SPEED
            self.vy = max(self.vy, - Baddie.JUMP_SPEED*1.25)

    def update(self, player):
        if not self.is_active(player):
            return

        if self.dying and time.time() > self.when_to_die:
            self.alive = False

        self.move_ai(player)

        if self.running_left:
            self.vx += (-Baddie.RUNNING_SPEED - self.vx) * Baddie.RUNNING_ACCELERATION
        elif self.running_right:
            self.vx += (Baddie.RUNNING_SPEED - self.vx) * Baddie.RUNNING_ACCELERATION
        else:
            self.vx *= (1 - Baddie.RUNNING_DECELERATION)

        self.vy += Properties.GRAVITY

        # try to move horizontally and see, if you collided
        self.x += self.vx
        # checking collisions
        for obj in self.get_collided_objects():
            # Obstacle cannot be walked through
            if not self.can_walk_through_object(obj):
                if self.left < obj.right < self.right:
                    self.left = obj.right
                    self.vx = -self.vx * Baddie.JUMP_BOUNCE

                elif self.left < obj.left < self.right:
                    self.right = obj.left
                    self.vx = -self.vx * Baddie.JUMP_BOUNCE

        # try to move vertically and see, if you collided
        self.y += self.vy
        for obj in self.get_collided_objects():
            # Obstacle cannot be walked through
            if not self.can_walk_through_object(obj):
                if self.bottom > obj.top > self.top:
                    self.bottom = obj.top
                    self.vy = -self.vy * Baddie.JUMP_BOUNCE

                elif self.bottom > obj.bottom > self.top:
                    self.top = obj.bottom
                    self.vy = -self.vy * Baddie.JUMP_BOUNCE

        self.steps += 1

    @staticmethod
    def can_walk_through_object(obj):
        return obj.NAME not in ["baddie", "player", "obstacle"]

    def is_touching_ground(self):
        # try to move a little bit down and see, if you collide with obstacle
        move_size = 1
        self.y += move_size

        for obj in self.get_collided_objects():
            if obj.NAME in ["baddie", "player", "obstacle"]:
                self.y -= move_size
                return True
        self.y -= move_size
        return False

    def get_collided_objects(self):
        result = []
        for obj in self.collision_engine.get_near_objects(self):
            if self.collided_with(obj):
                result.append(obj)
        return result

    def is_active(self, player):
        # freeze baddie completely, if it is out of sight
        if ((self.x - player.x)**2 + (self.y - player.y)**2)**0.5 < Baddie.ACTIVE_RADIUS:
            return True
        return False

    def go_right(self):
        self.running_right = True
        self.running_left = False

    def go_left(self):
        self.running_right = False
        self.running_left = True

    def dont_move(self):
        self.running_right = False
        self.running_left = False

    def load_animations(self):
        self.animations[Baddie.RUNNING_RIGHT] = Animator(Baddie.RUNNING_ANIMATION_DELAY)
        self.animations[Baddie.RUNNING_RIGHT].load_from_filesystem(["resources/baddies/baddie-running-right.png"])

        self.animations[Baddie.RUNNING_LEFT] = Animator(Baddie.RUNNING_ANIMATION_DELAY)
        self.animations[Baddie.RUNNING_LEFT].load_from_filesystem(["resources/baddies/baddie-running-left.png"])

        self.animations[Baddie.STANDING] = Animator(Baddie.RUNNING_ANIMATION_DELAY)
        self.animations[Baddie.STANDING].load_from_filesystem(["resources/baddies/baddie-standing.png"])

    def set_game_objects(self, game_objects):
        self.game_objects = game_objects

    def die(self):
        # starts dying procedure
        if not self.dying:
            self.dying = True
            self.when_to_die = time.time() + Baddie.DYING_TIME

    def distance_to_player(self, player):
        return ((self.x - player.x)**2 + (self.y - player.y)**2) ** 0.5

    def can_see_player(self, player):

        if self.distance_to_player(player) < Baddie.SIGHT_RADIUS:
            steps = max(1, int(self.distance_to_player(player) / 20))
            dx, dy = player.center_x - self.center_x, player.center_y - self.center_y
            stepx, stepy = dx / steps, dy / steps

            for i in range(steps):
                p = self.center_x + i * stepx, self.center_y + i * stepy
                # self.draw_point(p)
                for obj in self.collision_engine.get_objects_near_point(p, radius=1):
                    if obj.NAME == "obstacle" and self.point_collided(obj, p):
                        return False

            self.last_seen_player = time.time()
            return True
        else:
            return False

    def move_randomly(self):
        probability = 200
        rn = random.randint(1, probability)
        if rn == 1:
            self.go_right()
        elif rn == 2:
            self.go_left()
        elif rn == 3 and self.is_touching_ground():
            self.dont_move()

        if random.randint(1, 500) == 1:
            self.jump()

    def point_collide_with_obstacle(self, point):
        for obj in self.collision_engine.get_objects_colliding_with_point(point):
            if obj.NAME == "obstacle":
                return True
        return False

    def obstacle_to_the_right(self, distance=5):
        return self.point_collide_with_obstacle((self.right + distance, self.center_y))

    def obstacle_to_the_left(self, distance=5):
        return self.point_collide_with_obstacle((self.left - distance, self.center_y))

    def jump_in_front_of_obstacle(self):
        lookahead = 20
        if self.running_left and self.obstacle_to_the_left(lookahead):
            self.jump()
        elif self.running_right and self.obstacle_to_the_right(lookahead):
            self.jump()

    # TODO debug
    def draw_point(self, point, color=colors.RED):
        self.game_instance.camera.draw_circle(color, point, 2)

    def move_ai(self, player):
        if self.can_see_player(player):
            if self.x < player.x:
                self.go_right()
            else:
                self.go_left()

            self.jump_in_front_of_obstacle()

        elif time.time() - self.last_seen_player < 2:
            # continues in the last seen direction
            self.jump_in_front_of_obstacle()

        else:
            self.move_randomly()

        p = (self.left + 10, self.top + self.HEIGHT + 15)
        # self.draw_point(p, colors.GREEN)
        jump = True
        for obj in self.collision_engine.get_objects_colliding_with_point(p):
            if not self.can_walk_through_object(obj):
                jump = False
                break
        if jump:
            self.jump()







