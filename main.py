import random
from enum import Enum

import arcade

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, ROW_COUNT, COLUMN_COUNT, GAME_VIEW_UPDATE_RATE
from utils import create_grid, create_cell_list, generate_start_coordinates

EMPTY = arcade.color.WHITE
FILLED = arcade.color.RED


class SnakeMoveDirection(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    DOWN = "DOWN"


# would be nice to move to container
cell_type_to_color_code = {"EMPTY": 0, "SNAKE": 1, "DECOY": 2, "GAME_OVER": 3, "EXCELLENT": 4}


class Snake:
    def __init__(self, board: list, random_cell_generator, snake_head_coord=None, decoy_coords=None):
        self.random_cell_generator = random_cell_generator

        self.snake_cells_coordinates = [snake_head_coord] if snake_head_coord else [self.random_cell_generator()]
        self.decoy_cell_coordinates = decoy_coords or self.random_cell_generator()
        self.direction = random.choice([s.value for s in SnakeMoveDirection])

        self.board = board
        self.set_up_coordinates_for_cell_type(self.snake_cells_coordinates[0], cell_type_to_color_code["SNAKE"])
        self.set_up_coordinates_for_cell_type(self.decoy_cell_coordinates, cell_type_to_color_code["DECOY"])

    def set_up_coordinates_for_cell_type(self, coordinates, color):
        coord_x, coord_y = coordinates
        self.board[coord_x][coord_y] = color

    def __len__(self):
        return len(self.snake_cells_coordinates)

    def change_direction(self, symbol: int):
        if symbol == arcade.key.W and self.direction != SnakeMoveDirection.DOWN.value:
            self.direction = SnakeMoveDirection.UP.value
        elif symbol == arcade.key.S and self.direction != SnakeMoveDirection.UP.value:
            self.direction = SnakeMoveDirection.DOWN.value
        elif symbol == arcade.key.A and self.direction != SnakeMoveDirection.RIGHT.value:
            self.direction = SnakeMoveDirection.LEFT.value
        elif symbol == arcade.key.D and self.direction != SnakeMoveDirection.LEFT.value:
            self.direction = SnakeMoveDirection.RIGHT.value

    def check_snake_on_borders(self, head_coordinates):
        head_x, head_y = head_coordinates

        if head_y == 0 and self.direction == SnakeMoveDirection.LEFT.value:
            raise ValueError
        elif head_y >= ROW_COUNT and self.direction == SnakeMoveDirection.RIGHT.value:
            raise ValueError
        elif head_x == 0 and self.direction == SnakeMoveDirection.UP.value:
            raise ValueError
        elif head_x >= COLUMN_COUNT and self.direction == SnakeMoveDirection.DOWN.value:
            raise ValueError

        return True

    def check_self_eat(self, head_coordinates):
        if head_coordinates in self.snake_cells_coordinates:
            raise ValueError

    def create_new_decoy(self):
        if len(self) >= (ROW_COUNT * COLUMN_COUNT) - 1:
            raise ArithmeticError

        while True:
            new_decoy = self.random_cell_generator()
            if new_decoy in self.snake_cells_coordinates:
                continue
            else:
                break

        self.decoy_cell_coordinates = new_decoy
        self.set_up_coordinates_for_cell_type(self.decoy_cell_coordinates, cell_type_to_color_code["DECOY"])

    def create_new_head_element(self, current_head: tuple) -> tuple:
        """
        Using tuple to prevent list deepcopy

        :param current_head:
        :return:
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

    def move(self):
        head_coordinates = self.snake_cells_coordinates[0]

        self.check_snake_on_borders(head_coordinates)
        head_coordinates = self.create_new_head_element(head_coordinates)
        self.check_self_eat(head_coordinates)

        self.set_up_coordinates_for_cell_type(head_coordinates, 1)
        self.snake_cells_coordinates.insert(0, head_coordinates)

        if head_coordinates != self.decoy_cell_coordinates:
            last = self.snake_cells_coordinates.pop()
            self.set_up_coordinates_for_cell_type(last, cell_type_to_color_code["EMPTY"])
        else:
            self.create_new_decoy()

    def game_over(self, status_code=cell_type_to_color_code["GAME_OVER"]):
        for index_x, row in enumerate(self.board):
            for index_y, col in enumerate(row):
                if index_y == 0 or index_x == 0 or index_x >= ROW_COUNT - 1 or index_y >= COLUMN_COUNT - 1:
                    self.board[index_x][index_y] = status_code


class SnakeGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.shape_grid = None
        self.snake = Snake(create_cell_list(), generate_start_coordinates)
        self.update_grid()

        self.set_update_rate(GAME_VIEW_UPDATE_RATE)

    def increase_update_rate(self):
        if self.update_rate > 1:
            self.update_rate -= 1

    def on_draw(self):
        arcade.start_render()
        self.shape_grid.draw()

    def update_grid(self):
        self.shape_grid = create_grid(self.snake.board)

    def on_update(self, delta_time: float):
        try:
            self.snake.move()
        except IndexError:
            self.snake.game_over()
            self.set_update_rate(10**9)
        except ValueError:
            self.snake.game_over()
            self.set_update_rate(10**9)
        except ArithmeticError:
            self.snake.game_over(cell_type_to_color_code["EXCELLENT"])
            self.set_update_rate(10**9)

        self.update_grid()

    def on_key_press(self, symbol: int, modifiers: int):
        self.snake.change_direction(symbol)


if __name__ == "__main__":
    SnakeGame(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    arcade.run()
