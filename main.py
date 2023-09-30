"""
Simple Snake game
"""

import random
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Type

import arcade

from constants import (
    COLUMN_COUNT,
    GAME_VIEW_UPDATE_RATE,
    ROW_COUNT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
)
from utils import RandomCellGenerator, create_cell_list, create_grid

EMPTY = arcade.color.WHITE
FILLED = arcade.color.RED


class SnakeMoveDirection(Enum):
    """Enum for mode direction"""

    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    DOWN = "DOWN"


@dataclass
class CellType:
    EMPTY = 0
    SNAKE = 1
    DECOY = 2
    GAME_OVER = 3
    EXCELLENT = 4


class Snake:
    """
    Snake movement and decoy creation logic
    """

    def __init__(
        self,
        board: list[list[int]],
        random_cell_generator: Type[RandomCellGenerator],
        snake_head_coord: Optional[Tuple[int, int]] = None,
        decoy_coords: Optional[Tuple[int, int]] = None,
    ):
        self.random_cell_generator = random_cell_generator()

        self.snake_cells_coordinates = (
            deque([snake_head_coord]) if snake_head_coord else deque([self.random_cell_generator()])
        )
        self.decoy_cell_coordinates = decoy_coords or self.random_cell_generator()
        self.direction = random.choice([s.value for s in SnakeMoveDirection])

        self.board = board
        self.set_up_coordinates_for_cell_type(self.snake_cells_coordinates[0], CellType.SNAKE)
        self.set_up_coordinates_for_cell_type(self.decoy_cell_coordinates, CellType.DECOY)

    def set_up_coordinates_for_cell_type(self, coordinates: Tuple[int, int], color: int) -> None:
        coord_x, coord_y = coordinates
        self.board[coord_x][coord_y] = color

    def __len__(self) -> int:
        return len(self.snake_cells_coordinates)

    def change_direction(self, symbol: int) -> None:
        if symbol == arcade.key.W and self.direction != SnakeMoveDirection.DOWN.value:
            self.direction = SnakeMoveDirection.UP.value
        elif symbol == arcade.key.S and self.direction != SnakeMoveDirection.UP.value:
            self.direction = SnakeMoveDirection.DOWN.value
        elif symbol == arcade.key.A and self.direction != SnakeMoveDirection.RIGHT.value:
            self.direction = SnakeMoveDirection.LEFT.value
        elif symbol == arcade.key.D and self.direction != SnakeMoveDirection.LEFT.value:
            self.direction = SnakeMoveDirection.RIGHT.value

    def check_snake_on_borders(self, head_coordinates: Tuple[int, int]) -> bool:
        head_x, head_y = head_coordinates
        inside_borders = True

        if head_y == 0 and self.direction == SnakeMoveDirection.LEFT.value:
            inside_borders = False
        elif head_y >= ROW_COUNT and self.direction == SnakeMoveDirection.RIGHT.value:
            inside_borders = False
        elif head_x == 0 and self.direction == SnakeMoveDirection.UP.value:
            inside_borders = False
        elif head_x >= COLUMN_COUNT and self.direction == SnakeMoveDirection.DOWN.value:
            inside_borders = False

        if not inside_borders:
            raise ValueError
        return inside_borders

    def check_self_eat(self, head_coordinates: Tuple[int, int]) -> None:
        if head_coordinates in self.snake_cells_coordinates:
            raise ValueError

    def create_new_decoy(self) -> None:
        if len(self) >= (ROW_COUNT * COLUMN_COUNT) - 1:
            raise ArithmeticError

        while True:
            new_decoy = self.random_cell_generator()
            if new_decoy not in self.snake_cells_coordinates:
                break

        self.decoy_cell_coordinates = new_decoy
        self.set_up_coordinates_for_cell_type(self.decoy_cell_coordinates, CellType.DECOY)

    def create_new_head_element(self, current_head: Tuple[int, int]) -> Tuple[int, int]:
        """
        Using tuple to prevent list deepcopy
        """

        if self.direction == SnakeMoveDirection.LEFT.value:
            current_head = (current_head[0], current_head[1] - 1)
        elif self.direction == SnakeMoveDirection.RIGHT.value:
            current_head = (current_head[0], current_head[1] + 1)
        elif self.direction == SnakeMoveDirection.UP.value:
            current_head = (current_head[0] + 1, current_head[1])
        elif self.direction == SnakeMoveDirection.DOWN.value:
            current_head = (current_head[0] - 1, current_head[1])

        return current_head

    def move(self) -> None:
        head_coordinates = self.snake_cells_coordinates[0]
        self.check_snake_on_borders(head_coordinates)

        head_coordinates = self.create_new_head_element(head_coordinates)
        self.check_self_eat(head_coordinates)

        self.set_up_coordinates_for_cell_type(head_coordinates, 1)
        self.snake_cells_coordinates.appendleft(head_coordinates)

        if head_coordinates != self.decoy_cell_coordinates:
            last = self.snake_cells_coordinates.pop()
            self.set_up_coordinates_for_cell_type(last, CellType.EMPTY)
        else:
            self.create_new_decoy()

    def game_over(self, status_code: int = CellType.GAME_OVER) -> None:
        for index_x, row in enumerate(self.board):
            for index_y, _ in enumerate(row):
                if index_y == 0 or index_x == 0 or index_x >= ROW_COUNT - 1 or index_y >= COLUMN_COUNT - 1:
                    self.board[index_x][index_y] = status_code


class SnakeGame(arcade.Window):
    """Game launcher"""

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.shape_grid = arcade.SpriteList()
        self.snake = Snake(create_cell_list(), RandomCellGenerator)
        self.update_grid()

        self.set_update_rate(GAME_VIEW_UPDATE_RATE)

    def on_draw(self) -> None:
        arcade.start_render()
        self.shape_grid.draw()

    def update_grid(self) -> None:
        self.shape_grid = create_grid(self.snake.board)

    def on_update(self, delta_time: float) -> None:
        try:
            self.snake.move()
        except IndexError:
            self.snake.game_over()
            self.set_update_rate(10**9)
        except ValueError:
            self.snake.game_over()
            self.set_update_rate(10**9)
        except ArithmeticError:
            self.snake.game_over(CellType.EXCELLENT)
            self.set_update_rate(10**9)

        self.update_grid()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.snake.change_direction(symbol)


if __name__ == "__main__":
    SnakeGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    arcade.run()
