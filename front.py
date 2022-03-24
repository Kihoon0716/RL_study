from curses import KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP
import pygame
from enum import Enum

pygame.init()


class Color(Enum):
    BLUE = 1
    RED = 2
    ORANGE = 3
    GREEN = 4
    PURPLE = 5
    YELLO = 6


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 0, 0)
PURPLE = (255, 0, 0)
YELLO = (255, 0, 0)

colors = {
    0: WHITE,
    1: BLUE,
    2: RED,
    3: ORANGE,
    4: GREEN,
    5: PURPLE,
    6: YELLO,
    100: PURPLE,
}

BLOCK_SIZE = 20
LINE_SIZE = 5
START_POINT_X = 300
START_POINT_Y = 200

size = [1000, 800]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")


done = False
clock = pygame.time.Clock()


def draw_block(screen, x, y, color):
    pygame.draw.rect(
        screen,
        color,
        [
            int(START_POINT_X + x * BLOCK_SIZE),
            int(START_POINT_Y + y * BLOCK_SIZE),
            BLOCK_SIZE,
            BLOCK_SIZE,
        ],
        0,
    )
    pygame.draw.rect(
        screen,
        BLACK,
        [
            int(START_POINT_X + x * BLOCK_SIZE),
            int(START_POINT_Y + y * BLOCK_SIZE),
            BLOCK_SIZE,
            BLOCK_SIZE,
        ],
        1,
    )


array = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0,],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0,],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0,],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1,],
]


class Move(Enum):
    TURN = 0
    LEFT = 1
    RIGHT = 2
    DROP = 3
    DOWN = 4


class Front:
    def show(self, map):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(WHITE)
        # pygame.draw.polygon(screen, GREEN, [[30,150], [125,100], [220,150]],5)
        # pygame.draw.polygon(screen, GREEN, [[30,150], [125,100], [220,150]],0)
        # pygame.draw.lines(screen, RED,False, [[50,150], [50,250], [200,250], [200,150]],5)
        pygame.draw.rect(
            screen,
            BLACK,
            [
                int(START_POINT_X - 2),
                int(START_POINT_Y - 2),
                int(BLOCK_SIZE * 10 + LINE_SIZE / 2),
                int(BLOCK_SIZE * 25 + LINE_SIZE / 2),
            ],
            int(LINE_SIZE / 2),
        )
        # pygame.draw.rect(screen, BLUE, [75,175,75,50],0)
        # pygame.draw.line(screen, BLACK, [112,175], [112,225],5)
        # pygame.draw.line(screen, BLACK, [75,200], [150,200],5)

        for y, row in enumerate(map):
            for x, block in enumerate(row):
                if block in colors:
                    draw_block(screen, x, y, colors[block])

        pygame.display.update()

    def get_command(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            return Move.LEFT
        if pressed[pygame.K_RIGHT]:
            return Move.RIGHT
        if pressed[pygame.K_UP]:
            return Move.TURN
        if pressed[pygame.K_DOWN]:
            return Move.DOWN
        if pressed[pygame.K_SPACE]:
            return Move.DROP
        return -1

    def quit(self):
        pygame.quit()
