import os

import pygame
import PygameXtras as px

from .config import (
    FIELD_WIDTH,
    FPS,
    HIGHSCORE_PATH,
    TILESIZE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from .core import Core

pygame.init()
pygame.display.set_caption("Snake")


class Game:
    def __init__(self, name: str):
        self._name = name
        if not os.path.exists(HIGHSCORE_PATH):
            with open(HIGHSCORE_PATH, "w") as f:
                f.write("3")
                self._highscore = 3
        else:
            with open(HIGHSCORE_PATH, "r") as f:
                self._highscore = int(f.read())

        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()

    def run(self):
        title = px.Label(
            self._screen,
            "Snake",
            100,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
            "midbottom",
            tc=(0, 255, 0),
            f="verdana",
        )

        info_label_1 = px.Label(
            self._screen,
            "Press SPACE to start",
            30,
            (title.center[0], title.bottom + 50),
            "midtop",
            tc=(0, 255, 0),
            f="verdana",
        )

        info_label_2 = px.Label(
            self._screen,
            f"Highscore: {self._highscore}",
            30,
            (info_label_1.center[0], info_label_1.bottom + 20),
            "midtop",
            tc=(0, 255, 0),
            f="verdana",
        )

        start_game = False

        while True:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_SPACE:
                        start_game = True

            if start_game:
                start_game = False
                while self.main():
                    pass

            self._screen.fill((0, 0, 0))
            title.draw()
            info_label_1.draw()
            info_label_2.draw()

            pygame.display.flip()
            self._clock.tick(FPS)

    def main(self):
        game = Core()
        r = pygame.Rect(0, 0, FIELD_WIDTH * TILESIZE, FIELD_WIDTH * TILESIZE)
        r.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            if not game.update():
                return self.game_over_screen(game._snake.get_size())

            self._screen.fill((0, 0, 0))
            self._screen.blit(game.get_surface(), r)
            pygame.draw.rect(self._screen, (255, 255, 255), r, 1)

            pygame.display.flip()
            self._clock.tick(FPS)

    def game_over_screen(self, score: int):
        is_highscore = False
        if score > self._highscore:
            is_highscore = True
            self._highscore = score
            with open(HIGHSCORE_PATH, "w") as f:
                f.write(str(score))

        score_label = px.Label(
            self._screen,
            "Score: " + str(score),
            50,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60),
            "midbottom",
            tc=(0, 255, 0),
            f="verdana",
        )
        highscore_label = px.Label(
            self._screen,
            "NEW HIGHSCORE" if is_highscore else f"Highscore: {self._highscore}",
            50,
            (score_label.center[0], score_label.bottom + 20),
            "midtop",
            tc=(0, 255, 0),
            f="verdana",
        )

        info_label_1 = px.Label(
            self._screen,
            "Press SPACE to restart",
            30,
            (highscore_label.center[0], highscore_label.bottom + 50),
            "midtop",
            tc=(0, 255, 0),
            f="verdana",
        )

        info_label_2 = px.Label(
            self._screen,
            "Press ESC to exit",
            30,
            (info_label_1.center[0], info_label_1.bottom + 20),
            "midtop",
            tc=(0, 255, 0),
            f="verdana",
        )

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_SPACE:
                        return True

            self._screen.fill((0, 0, 0))

            score_label.draw()
            highscore_label.draw()

            info_label_1.draw()
            info_label_2.draw()

            pygame.display.flip()
            self._clock.tick(FPS)
