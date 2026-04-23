import random

from .config import FIELD_WIDTH
from .snake import Snake


class AppleManager:
    def __init__(self):
        self._apples: list[tuple[int, int]] = []

    def remove_apple(self, apple: tuple[int, int]):
        self._apples.remove(apple)

    def create_apple(self, snake: Snake):
        snake_fields = snake.get_body()
        if len(snake_fields) / (FIELD_WIDTH * FIELD_WIDTH) < 0.75:
            # if the snake takes up less than 75% of the field, create an apple by randomly selecting one field
            while True:
                apple = (
                    random.randint(0, FIELD_WIDTH - 1),
                    random.randint(0, FIELD_WIDTH - 1),
                )
                if apple not in snake_fields:
                    break
            self._apples.append(apple)
        else:
            # otherwise, calculate all possibilities and select one randomly
            possible_fields = [
                (x, y)
                for x in range(FIELD_WIDTH)
                for y in range(FIELD_WIDTH)
                if (x, y) not in snake_fields
            ]
            self._apples.append(random.choice(possible_fields))

    def get_apples(self):
        return self._apples
