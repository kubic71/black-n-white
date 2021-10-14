import pygame, sys, os, time
from pygame.locals import *

from obstacle import Obstacle
from player import Player
from baddie import Baddie
from baddie_shooting import BaddieShooting
from life import Life
from gun import Gun
from spike import Spike
from finish import Finish

from level_selector import LevelSelector

from properties import Properties
from keyboard_helper import KeyboardStateMemory
from camera import Camera
from collision_engine import CollisionEngine


import colors

class Game:


    objects = None

    def __init__(self, level="testlevel"):
        self.screen = pygame.display.set_mode((Properties.WINDOW_WIDTH, Properties.WINDOW_HEIGHT))

        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 16)

        self.heart_img = pygame.image.load(os.path.join("resources/ui/heart.png"))
        self.gun_img = pygame.image.load(os.path.join("resources/gun/gun_small.png"))

        # initialize the sound mixer
        pygame.mixer.init()

        self.objects_to_add = []

        # initialize fps clock object
        self.clock = pygame.time.Clock()  # load clock
        self.keyboardState = None
        self.player = None
        self.camera = None
        self.last_frame_times = [0] * 10
        self.collision_engine = None
        self.start_time = 0
        self.last_level_index = 0
        self.current_level = ""

    def load_level(self, level):
        self.current_level = level
        self.objects = set()
        self.collision_engine = CollisionEngine(self.objects)
        # loading obstacles
        print("loading level:", level)

        f = open(os.path.join("levels/" + level), "r")
        for y, line in enumerate(f.read().split("\n")):
            for x, obj_code in enumerate(line):
                obj = None
                current_position = x * Properties.OBJECT_SIZE, y * Properties.OBJECT_SIZE

                if obj_code == "X":   # Obstacle
                    obj = Obstacle(position=current_position, size=(Properties.OBJECT_SIZE, Properties.OBJECT_SIZE))
                elif obj_code == "P":  # Player
                    obj = Player(position=current_position, collision_engine=self.collision_engine)
                    # print("Player position:", x, y)
                    obj.set_game_objects(self.objects)
                    self.player = obj

                elif obj_code == "B":  # Baddie
                    obj = Baddie(position=current_position, collision_engine=self.collision_engine, game_instance=self)
                    obj.set_game_objects(self.objects)

                elif obj_code == "S":  # Baddie
                    obj = BaddieShooting(position=current_position, collision_engine=self.collision_engine, game_instance=self)
                    obj.set_game_objects(self.objects)

                elif obj_code == "L":
                    obj = Life(position=current_position)

                elif obj_code == "G":
                    obj = Gun(position=current_position)

                elif obj_code in ["v", "^", "<", ">"]:
                    obj = Spike(position=current_position, type=obj_code)

                elif obj_code == "F":
                    obj = Finish(position=current_position)

                if obj:
                    self.objects.add(obj)
                else:
                    pass
                    # print("Unknown object code: {}".format(obj_code))

        self.player.set_game_objects(self.objects)

        # setup camera object
        self.camera = Camera(self.screen)
        self.camera.follow(self.player)

        print("level loaded!")

    def render(self):
        self.screen.fill(colors.WHITE)

        self.draw_stats()

        if Properties.SHOW_FPS:
            self.last_frame_times = self.last_frame_times[1:] + [time.time()]
            average_fps = 1 / ((self.last_frame_times[-1] - self.last_frame_times[0]) / (len(self.last_frame_times) - 1))

            textsurface = self.font.render("FPS: {0:.2f}".format(average_fps), False, (200, 0, 0, 5))
            self.screen.blit(textsurface, (0, 100))

        for obj in self.objects:
            obj.draw(self.camera)

    def draw_stats(self):
        # draw lives
        imgrect = self.heart_img.get_rect()
        imgrect.top = 10
        for i in range(self.player.lives):
            imgrect.left = (i + 1) * 20
            self.screen.blit(self.heart_img, imgrect)

        # draw gun
        imgrect = self.gun_img.get_rect()
        imgrect.topleft = (20, 30)
        self.screen.blit(self.gun_img, imgrect)

        # show score
        self.screen.blit(self.font.render(str(self.player.shots), True, (0, 0, 0)), (50, 30))




        # show score
        self.screen.blit(self.font.render("Score: {}".format(self.player.score), True, (0, 0, 0)), (20, 50))

        # show play-time
        playtime = time.time() - self.start_time
        self.screen.blit(self.font.render("Time: {0:.2f}".format(playtime), True, (0, 0, 0)), (20, 70))

    def update(self):
        self.collision_engine.update()

        for obj in self.objects:
            if obj.NAME in ["baddie", "bullet"]:
                obj.update(self.player)
            else:
                obj.update()

        for obj in self.objects_to_add:
            self.objects.add(obj)
        self.objects_to_add = []

        self.camera.update()
        self.cleanup_dead_objects()

    def cleanup_dead_objects(self):
        new_set = set()
        for obj in self.objects:
            if obj.NAME in ["baddie", "life", "bullet", "gun"]:
                if obj.alive:
                    new_set.add(obj)
            else:
                new_set.add(obj)

        self.objects.clear()
        for obj in new_set:
            self.objects.add(obj)

    def gameover(self):
        red_fadein = pygame.Surface((Properties.WINDOW_WIDTH, Properties.WINDOW_HEIGHT))
        red_fadein.fill(colors.RED)

        text = pygame.font.SysFont('arial', 50).render("Game Over!", True, colors.BLACK)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH/2, Properties.WINDOW_HEIGHT/2
        red_fadein.blit(text, rect)

        text = pygame.font.SysFont('arial', 15).render("Score: {}".format(self.player.score), True, colors.BLACK)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2 + 70
        red_fadein.blit(text, rect)

        text = pygame.font.SysFont('arial', 15).render("Time: {0:.2f}s".format(time.time() - self.start_time), True, colors.BLACK)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2 + 90
        red_fadein.blit(text, rect)

        text = pygame.font.SysFont('arial', 15).render("Press any key to continue...", True, colors.BLACK)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2 + 120
        red_fadein.blit(text, rect)

        self.fadein(red_fadein)
        self.wait_for_keypress()

    def level_finished(self):
        green_fadein = pygame.Surface((Properties.WINDOW_WIDTH, Properties.WINDOW_HEIGHT))
        green_fadein.fill(colors.GREEN)

        text = pygame.font.SysFont('arial', 50).render("You successfully finished this level!", True, colors.WHITE)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2
        green_fadein.blit(text, rect)

        text = pygame.font.SysFont('arial', 15).render("Score: {}".format(self.player.score), True, colors.BLACK)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2 + 70
        green_fadein.blit(text, rect)

        text = pygame.font.SysFont('arial', 15).render("Time: {0:.2f}s".format(time.time() - self.start_time), True, colors.BLACK)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2 + 90
        green_fadein.blit(text, rect)

        text = pygame.font.SysFont('arial', 15).render("Press any key to continue...", True, colors.BLACK)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2 + 120
        green_fadein.blit(text, rect)

        self.player.keyboard_state = KeyboardStateMemory()

        self.fadein(green_fadein)
        self.wait_for_keypress()

    def fadein(self, surface):

        for i in range(0, 256, 3):
            self.render()
            self.update()
            surface.set_alpha(i)
            self.screen.blit(surface, (0, 0))
            pygame.display.flip()

            self.clock.tick(Properties.FPS_LIMITING)

    def wait_for_keypress(self):
        _ = pygame.event.get()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit()
                    else:
                        running = False
            pygame.display.flip()
            self.clock.tick(Properties.FPS_LIMITING)

    def quit(self):
        self.screen.fill(colors.BLACK)

        text = pygame.font.SysFont('arial', 50).render("Are you sure you want to exit the game?", True, colors.WHITE)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2
        self.screen.blit(text, rect)

        text = pygame.font.SysFont('arial', 20).render("Press ENTER to exit, ESCAPE to return to the game", True, colors.WHITE)
        rect = text.get_rect()
        rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT / 2 + 80
        self.screen.blit(text, rect)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        pygame.quit()
                        sys.exit(0)

            pygame.display.flip()
            self.clock.tick(Properties.FPS_LIMITING)


    def start(self):
        self.keyboardState = KeyboardStateMemory()
        self.player.set_keyboard_state_memory(self.keyboardState)
        self.start_time = time.time()

        # gameloop
        playing = True
        while playing:
            self.clock.tick(Properties.FPS_LIMITING)

            # get events from the user
            events = pygame.event.get()
            self.keyboardState.update(events)
            for event in events:
                # # check if presses a key or left it
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.jump()
                    elif event.key == K_w:
                        self.player.fire_up()
                    elif event.key == K_a:
                        self.player.fire_left()
                    elif event.key == K_d:
                        self.player.fire_right()
                    elif event.key == K_s:
                        self.player.fire_down()

                    elif event.key == K_ESCAPE:
                        self.quit()

            #print(len(self.objects))

            self.render()
            self.update()

            if self.player.lives == 0 or self.player.finished:
                playing = False

            pygame.display.flip()

        if self.player.lives == 0:
            self.gameover()
        elif self.player.finished:
            self.level_finished()

    def select_level(self):
        self.last_level_index, level_name = LevelSelector(self.screen).select_level(self.last_level_index)
        return level_name


g = Game()

while True:
    level = g.select_level()
    g.load_level(level)
    g.start()