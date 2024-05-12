import random


class Snake:
    def __init__(self, board_width, board_height):
        self.speed = 2  # Squares per second
        self.direction = 'right'  # Initial direction
        self.body = [
            (board_width // 2, board_height // 2),  # Head
            (board_width // 2 - 1, board_height // 2),
            (board_width // 2 - 2, board_height // 2)
        ]

    def get_head(self):
        return self.body[0]  # Head is always the first segment

    def move(self):
        # Calculate new head position based on the current direction
        head_x, head_y = self.body[0]
        if self.direction == 'right':
            head_x += 1
        elif self.direction == 'left':
            head_x -= 1
        elif self.direction == 'up':
            head_y -= 1
        elif self.direction == 'down':
            head_y += 1

        # Insert the new head at the beginning of the list
        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        # Remove the last element to simulate movement unless growing
        self.body.pop()

    def calculate_new_head(self):
        head_x, head_y = self.get_head()
        new_head_x = head_x  # Initialize with current head position
        new_head_y = head_y  # Initialize with current head position

        if self.direction == 'right':
            new_head_x = head_x + 1
        elif self.direction == 'left':
            new_head_x = head_x - 1
        elif self.direction == 'up':
            new_head_y = head_y - 1
        elif self.direction == 'down':
            new_head_y = head_y + 1

        return new_head_x, new_head_y

    def grow(self):
        # Add a new segment at the previous tail position
        self.body.append(self.body[-1])

    def get_body(self):
        return self.body

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        opposite_directions = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction


# Game state management
class Game:
    def __init__(self, width, height):
        self.board_width = width
        self.board_height = height
        self.snake = Snake(width, height)
        self.food = self.place_food()
        self.walls = self.place_walls()
        self.game_over = False

    def place_food(self):
        while True:
            food_position = (random.randint(0, self.board_width - 1), random.randint(0, self.board_height - 1))
            if food_position not in self.snake.body:
                return food_position

    def place_walls(self):
        walls = set()
        wall_count = int((self.board_width * self.board_height) / 25)
        while len(walls) < wall_count:
            wall = (random.randint(0, self.board_width - 1), random.randint(0, self.board_height - 1))
            if wall not in self.snake.body and wall != self.food:
                walls.add(wall)
        return walls

    def move_snake(self):
        if self.check_collision(self.snake.calculate_new_head()):
            self.game_over = True
        else:
            self.snake.move()
            if self.snake.get_head() == self.food:
                self.snake.grow()
                self.food = self.place_food()

    def check_collision(self, position):
        x, y = position
        return (
                x < 0 or x >= self.board_width or
                y < 0 or y >= self.board_height or
                position in self.snake.body or
                position in self.walls
        )



    def get_score(self):
        return len(self.snake.body) - 3  # Assuming initial snake length is 3

# Example to initiate and manage game
game_instance = None


def init_game(width, height, name):
    global game_instance
    if width < 5 or width > 25 or height < 5 or height > 25:
        raise ValueError("Width and height must be between 5 and 25.")
    game_instance = Game(width, height)


def move_snake():
    global game_instance
    if not game_instance.game_over:
        game_instance.move_snake()


def change_direction(new_direction):
    global game_instance
    if game_instance and not game_instance.game_over:
        game_instance.snake.change_direction(new_direction)


def get_snake():
    return game_instance.snake.body if game_instance else []


def get_food():
    return game_instance.food if game_instance else (0, 0)


def get_walls():
    return game_instance.walls if game_instance else set()


def get_board():
    return (game_instance.board_width, game_instance.board_height) if game_instance else (0, 0)


def is_game_over():
    return game_instance.game_over if game_instance else False


def calculate_area(width, height):
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive numbers.")
    return width * height