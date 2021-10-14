import pygame

from animator import Animator
from properties import Properties
import colors
import time
from baddie import Baddie
from bullet import Bullet

import random


class BaddieShooting(Baddie):
    NAME = "baddie"

    KILL_SCORE = 6

    def update(self, player):
        super().update(player)

        if random.randint(1, 100) == 1 and self.can_see_player(player):
            self.fire_at(player)

    def fire_at(self, player):
        target = player.center_x, player.center_y
        bullet = Bullet((self.center_x, self.center_y), target, fired_by="baddie", collision_engine=self.game_instance.collision_engine)
        self.game_instance.objects_to_add.append(bullet)






