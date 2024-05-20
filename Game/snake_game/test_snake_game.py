import pytest
from flask import Flask

from Game.snake_game import game
from Game.snake_game.game import Game, Snake, get_food


# Basic Snake Tests
def test_snake_init():
    game_width = 10
    game_height = 10
    snake = Snake(game_width, game_height)

    assert snake.speed == 1
    assert snake.direction == 'right'
    assert snake.body == [(5, 5), (4, 5), (3, 5)]


def test_game_move_snake():
    game = Game(10, 10)
    start_head = game.snake.get_head()

    game.move_snake()

    assert game.snake.get_head() != start_head  # Snake has moved


# Tests for board validation and creation
def test_board_size_validation():
    with pytest.raises(ValueError):
        game.init_game(4, 4, 'Invalid')


def test_board_creation():
    game = Game(10, 10)
    assert game.board_width == 10
    assert game.board_height == 10


def test_board_size_below_minimum():
    with pytest.raises(ValueError):
        game.init_game(4, 24, 'Invalid Low Width')
        game.init_game(24, 4, 'Invalid Low Height')


def test_board_size_above_maximum():
    with pytest.raises(ValueError):
        game.init_game(26, 24, 'Invalid High Width')
        game.init_game(24, 26, 'Invalid High Height')


# Movement tests
def test_move_up():
    game = Game(10, 10)  # Directly create an instance of Game in each test
    game.snake.change_direction('up')
    game.move_snake()
    assert game.snake.get_head() == (5, 4)  # Assumes initial position is (5, 5)


def test_move_down():
    game = Game(10, 10)
    game.snake.change_direction('down')
    game.move_snake()
    assert game.snake.get_head() == (5, 6)


def test_move_right():
    game = Game(10, 10)
    game.snake.change_direction('right')
    game.move_snake()
    assert game.snake.get_head() == (6, 5)


def test_prevent_move_backwards_from_right():
    game = Game(10, 10)
    game.snake.direction = 'right'
    game.snake.change_direction('left')  # Attempt to change to the opposite direction
    game.move_snake()
    assert game.snake.direction == 'right'  # Expect no change in direction


def test_prevent_move_backwards_from_left():
    snake = Snake(10, 10)
    snake.direction = 'left'
    snake.change_direction('right')
    assert snake.direction == 'left'


def test_prevent_move_backwards_from_up():
    snake = Snake(10, 10)
    snake.direction = 'up'
    snake.change_direction('down')
    assert snake.direction == 'up'


def test_prevent_move_backwards_from_down():
    snake = Snake(10, 10)
    snake.direction = 'down'
    snake.change_direction('up')
    assert snake.direction == 'down'


# Tests for collisions and growth
def test_collision_left_wall():
    game = Game(5, 5)
    game.snake.body = [(0, 2)]  # Place snake head near left wall
    game.snake.direction = 'left'
    game.move_snake()
    assert game.game_over


def test_collision_right_wall():
    game = Game(5, 5)
    game.snake.body = [(4, 2)]  # Place snake head near right wall
    game.snake.direction = 'right'
    game.move_snake()
    assert game.game_over


def test_collision_top_wall():
    game = Game(5, 5)
    game.snake.body = [(2, 0)]  # Place snake head near top wall
    game.snake.direction = 'up'
    game.move_snake()
    assert game.game_over


def test_collision_bottom_wall():
    game = Game(5, 5)
    game.snake.body = [(2, 4)]  # Place snake head near bottom wall
    game.snake.direction = 'down'
    game.move_snake()
    assert game.game_over


def test_snake_growth_over_multiple_moves():
    game = Game(10, 10)
    start_length = len(game.snake.body)

    # Move multiple times, placing food directly in the snake's path each time
    for _ in range(3):  # Let's simulate eating 3 times
        game.food = game.snake.calculate_new_head()  # Place food ahead
        game.move_snake()

    assert len(game.snake.body) == start_length + 3


def test_snake_reaches_specific_length():
    game = Game(10, 10)
    target_length = 6  # Adjust this target length

    while len(game.snake.body) < target_length:
        game.food = game.snake.calculate_new_head()
        game.move_snake()

    assert len(game.snake.body) == target_length


def test_collision_with_self():
    game = Game(10, 10)

    # Force a scenario where the snake collides with its own tail
    game.snake.body = [(2, 2), (3, 2), (4, 2), (4, 3), (3, 3), (2, 3)]  # Head overlaps the tail
    game.snake.direction = 'right'  # Move the head back towards the body

    game.move_snake()
    assert game.game_over


def test_new_food_not_on_snake():
    game = Game(10, 10)
    game.snake.head = get_food()  # Force eating
    game.move_snake()
    assert game.snake.head not in get_food()


def test_new_food_not_on_walls():
    game = Game(10, 10)
    game.food = game.snake.get_head()  # Force eating
    game.move_snake()
    assert game.food not in game.walls


def test_snake_initial_length():
    snake = Snake(10, 10)
    assert len(snake.body) == 3  # Initial length


def test_snake_grow():
    snake = Snake(10, 10)
    initial_length = len(snake.body)
    snake.grow()
    assert len(snake.body) == initial_length + 1  # After growing, length should increase by 1


def test_snake_move_without_growing():
    snake = Snake(10, 10)
    initial_length = len(snake.body)
    snake.move()
    assert len(snake.body) == initial_length  # Length should remain the same if not growing


def test_snake_move_with_growing():
    snake = Snake(10, 10)
    initial_length = len(snake.body)
    snake.grow()
    snake.move()
    assert len(snake.body) == initial_length + 1  # Length should increase after moving and growing


def test_snake_move_multiple_times():
    snake = Snake(10, 10)
    initial_length = len(snake.body)
    for _ in range(5):
        snake.move()
    assert len(snake.body) == initial_length  # Length should remain the same without growing


def test_snake_grow_multiple_times():
    snake = Snake(10, 10)
    initial_length = len(snake.body)
    for _ in range(5):
        snake.grow()
    assert len(snake.body) == initial_length + 5  # Length should increase after growing multiple times


def test_snake_move_with_custom_speed():
    snake = Snake(10, 10)
    snake.speed = 2  # Increase speed
    initial_head = snake.get_head()
    snake.move()
    assert snake.get_head() != initial_head  # Snake should move faster


def test_snake_grow_max_length():
    snake = Snake(5, 5)
    max_length = 5 * 5  # Maximum possible length for this board size
    for _ in range(max_length):
        snake.grow()
        if len(snake.body) >= max_length:
            break
    assert len(snake.body) == max_length  # Snake should reach maximum length


def test_snake_avoid_obstacles():
    snake = Snake(10, 10)
    snake.body = [(5, 5), (5, 4), (5, 3)]  # Place snake near an obstacle
    snake.direction = 'left'
    obstacle_position = (4, 4)
    game = Game(10, 10)
    game.walls.add(obstacle_position)
    game.move_snake()
    assert snake.get_head() != (4, 5)  # Snake should avoid the obstacle


def test_snake_move_bigger_steps():
    snake = Snake(10, 10)
    initial_head = snake.get_head()
    snake.speed = 2  # Increase speed
    for _ in range(2):
        snake.move()  # Snake should move two steps
    assert snake.get_head() == (initial_head[0] + 2, initial_head[1])


def test_incorrect_route():
    app = Flask(__name__)

    with app.test_client() as client:
        response = client.get('/some_incorrect_route')
        assert response.status_code == 404

