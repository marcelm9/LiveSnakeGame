from typing import Literal

import pygame

from .config import FIELD_WIDTH, TILESIZE


class Snake:
    def __init__(
        self,
        direction: Literal["left", "right", "up", "down"],
        head: tuple[int, int],
        initial_length: int = 3,
    ):
        self.direction = direction
        self.desired_direction = direction
        self.body: list[tuple[int, int]] = [head]
        self.apples = initial_length - 1

    def update_input(self):
        # update direction
        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_w] and keys[pygame.K_s]):
            if keys[pygame.K_w] and not self.direction == "down":
                self.desired_direction = "up"
            elif keys[pygame.K_s] and not self.direction == "up":
                self.desired_direction = "down"
        if not (keys[pygame.K_a] and keys[pygame.K_d]):
            if keys[pygame.K_a] and not self.direction == "right":
                self.desired_direction = "left"
            elif keys[pygame.K_d] and not self.direction == "left":
                self.desired_direction = "right"

    def update(self):
        self.direction = self.desired_direction

        # move snake
        if self.direction == "up":
            self.body.insert(0, (self.body[0][0], self.body[0][1] - 1))
        elif self.direction == "down":
            self.body.insert(0, (self.body[0][0], self.body[0][1] + 1))
        elif self.direction == "left":
            self.body.insert(0, (self.body[0][0] - 1, self.body[0][1]))
        elif self.direction == "right":
            self.body.insert(0, (self.body[0][0] + 1, self.body[0][1]))

        # remove tail if no apple eaten
        if self.apples == 0:
            del self.body[-1]
        else:
            self.apples -= 1

        # die if eaten itself
        if len(self.body) != len(set(self.body)):
            return False

        # die if out of bounds
        if (
            self.body[0][0] < 0
            or self.body[0][0] >= FIELD_WIDTH
            or self.body[0][1] < 0
            or self.body[0][1] >= FIELD_WIDTH
        ):
            return False

        # return True if not dead
        return True

    def eat(self):
        self.apples += 1

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (
                self.body[0][0] * TILESIZE,
                self.body[0][1] * TILESIZE,
                TILESIZE,
                TILESIZE,
            ),
        )
        for pos in self.body[1:]:
            pygame.draw.rect(
                surface,
                (0, 200, 0),
                (pos[0] * TILESIZE, pos[1] * TILESIZE, TILESIZE, TILESIZE),
            )

    def get_body(self):
        return self.body

    def get_head(self) -> tuple[int, int]:
        return self.body[0]

    def get_size(self):
        return len(self.body)
