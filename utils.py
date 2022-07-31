import random
from typing import Tuple

import arcade

from constants import COLUMN_COUNT, HEIGHT, MARGIN, ROW_COUNT, WIDTH

EMPTY = arcade.color.WHITE
SNAKE = arcade.color.SPRING_GREEN
DECOY = arcade.color.ANTIQUE_RUBY
GAME_OVER = arcade.color.RED
EXCELLENT = arcade.color.GREEN

START_MARGIN = 6

CELL_CODE_TO_COLOR_MAP = {0: EMPTY, 1: SNAKE, 2: DECOY, 3: GAME_OVER, 4: EXCELLENT}


def create_cell_list() -> list:
    """
    Generate random 2-dim list with alive or dead cells
    :return: list
    """

    list_representation = []

    for _ in range(ROW_COUNT):
        column_repr = []
        for _ in range(COLUMN_COUNT):
            column_repr.append(0)  # label for empty cell
        list_representation.append(column_repr)

    return list_representation


class RandomCellGenerator:
    """
    Random cell generator for create new decoy
    """

    def __call__(self) -> Tuple[int, int]:
        x_coord, y_coord = random.randint(START_MARGIN, COLUMN_COUNT - START_MARGIN), random.randint(
            START_MARGIN, ROW_COUNT - START_MARGIN
        )
        return x_coord, y_coord


def create_grid(list_representation: list) -> arcade.SpriteList:
    """
    Create grid with generated above 2-dim list
    """

    grid = arcade.SpriteList()

    for row_index, row in enumerate(list_representation):
        for value_index, value in enumerate(row):
            x_coord = (MARGIN + WIDTH) * value_index + MARGIN + WIDTH // 2
            y_coord = (MARGIN + HEIGHT) * row_index + MARGIN + HEIGHT // 2

            color = CELL_CODE_TO_COLOR_MAP[value]

            circle = arcade.SpriteCircle(WIDTH // 2, color)
            circle.center_x = x_coord
            circle.center_y = y_coord

            grid.append(circle)

    return grid
