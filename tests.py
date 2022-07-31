from main import Snake, SnakeMoveDirection
from utils import RandomCellGenerator, create_cell_list


def test_decoy_catch() -> None:
    """
    Check if new deoy was created after catch original one
    """

    board = create_cell_list()

    snake_start = (5, 7)
    decoy_coords = (5, 6)
    snake = Snake(board, RandomCellGenerator, snake_start, decoy_coords)
    snake.direction = SnakeMoveDirection.LEFT.value

    snake.move()

    assert isinstance(snake.decoy_cell_coordinates, tuple)
    assert snake.decoy_cell_coordinates != decoy_coords
