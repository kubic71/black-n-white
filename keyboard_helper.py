from pygame.locals import *


class KeyboardStateMemory:
    # Remembers the state (Pressed or not pressed) of keyboard keys
    def __init__(self):
        self.pressed_keys = set()

    def is_pressed(self, key_code):
        return key_code in self.pressed_keys

    def update(self, events):
        for event in events:
            if event.type == KEYDOWN:
                self.pressed_keys.add(event.key)
            elif event.type == KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)