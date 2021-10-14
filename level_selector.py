import os
import pygame
import colors
import sys
import time
from properties import Properties
from pygame.locals import *


class LevelSelector:
    def __init__(self, screen):
        self.screen = screen

    def select_level(self, selected=0):
        levels = os.listdir("levels")
        if selected >= len(levels):
            selected = 0

        while True:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        selected = (selected + 1) % len(levels)
                    elif event.key == K_UP:
                        selected = (selected - 1) % len(levels)
                    elif event.key == K_RETURN:
                        return selected, levels[selected]

                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)

            self.screen.fill(colors.BLACK)

            for i, level in enumerate(levels):
                text = pygame.font.SysFont('arial', 25 if selected == i else 15).render(level, True, colors.WHITE)
                rect = text.get_rect()
                rect.center = Properties.WINDOW_WIDTH / 2, Properties.WINDOW_HEIGHT/2 - len(levels)/2*30 + i * 30
                self.screen.blit(text, rect)

            self.show_key_mappings()

            pygame.display.flip()
            time.sleep(0.01)

    def show_key_mappings(self):
        instructions = ["left arrow: move left",
                        "right arrow: move right",
                        "spacebar: jump",
                        "W: fire up",
                        "A: fire left",
                        "S: fire down",
                        "D: fire right",
                        "Esc: Exit game"]

        text = pygame.font.SysFont('arial', 20).render("Controls: ", True, colors.WHITE)
        rect = text.get_rect()
        rect.left = 20
        rect.centery = 570
        self.screen.blit(text, rect)

        for i, ins in enumerate(instructions):
            text = pygame.font.SysFont('arial', 13).render(ins, True, colors.WHITE)
            rect = text.get_rect()
            rect.left = 20
            rect.centery = 600 + i * 20
            self.screen.blit(text, rect)



