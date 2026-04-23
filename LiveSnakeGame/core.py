import time

import pygame

from .apple_manager import AppleManager
from .config import FIELD_WIDTH, FPS_IN_GAME, TILESIZE
from .snake import Snake


class Core:
    def __init__(self):
        self._surface = pygame.Surface((FIELD_WIDTH * TILESIZE, FIELD_WIDTH * TILESIZE))

        self._snake = Snake("right", (0, 0), initial_length=3)
        self._apples_manager = AppleManager()
        self._apples_manager.create_apple(self._snake)

        self._time = time.time()

    def update(self):
        now = time.time()
        self._snake.update_input()
        if now - self._time >= 1 / FPS_IN_GAME:
            self._time = now
            if not self._snake.update():
                return False
            if self._snake.get_head() in self._apples_manager.get_apples():
                self._snake.eat()
                self._apples_manager.remove_apple(self._snake.get_head())
                if self._snake.get_size() == FIELD_WIDTH * FIELD_WIDTH:
                    return False
                else:
                    self._apples_manager.create_apple(self._snake)
        return True

    def get_surface(self) -> pygame.Surface:
        self._surface.fill((0, 0, 0))
        self._snake.draw(self._surface)
        for apple in self._apples_manager.get_apples():
            pygame.draw.rect(
                self._surface,
                (255, 0, 0),
                (apple[0] * TILESIZE, apple[1] * TILESIZE, TILESIZE, TILESIZE),
            )
        return self._surface
