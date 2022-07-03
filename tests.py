from main import Snake, SnakeMoveDirection
from utils import create_cell_list, generate_start_coordinates


def test_decoy_catch():
    board = create_cell_list()

    snake_start = (5, 7)
    decoy_coords = (5, 6)
    snake = Snake(board, generate_start_coordinates, snake_start, decoy_coords)
    snake.direction = SnakeMoveDirection.LEFT.value

    snake.move()

    assert snake.decoy_cell_coordinates != decoy_coords
