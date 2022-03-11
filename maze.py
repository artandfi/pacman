import numpy as np
import collections
import random

from pygame import Rect
from PIL import Image
from constants import BLOCK_SIZE


VISITED = [255, 255, 255]


class Maze:
    """Maze class with layout for the game."""
    def __init__(self):
        self.layout = None
        self.solution = None

        self._dir1 = [
            lambda x, y: (x + 1, y),
            lambda x, y: (x - 1, y),
            lambda x, y: (x, y - 1),
            lambda x, y: (x, y + 1)
        ]
        self._dir2 = [
            lambda x, y: (x + 2, y),
            lambda x, y: (x - 2, y),
            lambda x, y: (x, y - 2),
            lambda x, y: (x, y + 2)
        ]
        self._direction_range = list(range(4))

    @property
    def _random_directions(self):
        """Returns a random direction range to iterate over."""
        random.shuffle(self._direction_range)
        return self._direction_range
    
    @property
    def row_count_with_walls(self):
        return self.layout.shape[0]

    @property
    def col_count_with_walls(self):
        return self.layout.shape[1]

    @property
    def row_count(self):
        return self.row_count_with_walls // 2

    @property
    def col_count(self):
        return self.col_count_with_walls // 2

    def generate(self, row_count, col_count):
        """Generate a maze for a given row and column count."""
        if (row_count or col_count) <= 0:
            raise MazeError("Row or column count cannot be less than zero.")

        self.layout = np.zeros((row_count, col_count, 3), dtype=np.uint8)
        self._backtrack()

        return self.layout

    def _backtrack(self):
        """Creates a maze using the recursive backtracking algorithm."""
        stack = collections.deque()

        x = 2 * random.randint(0, self.row_count - 1) + 1
        y = 2 * random.randint(0, self.col_count - 1) + 1
        self.layout[x, y] = VISITED[:]

        while x and y:
            while x and y:
                stack.append((x, y))
                x, y = self._generate_walk(x, y)
            x, y = self._generate_backtrack(stack)

    def _generate_walk(self, x, y):
        """Randomly walk from one cell within the maze to another one."""
        for idx in self._random_directions:
            tx, ty = self._dir2[idx](x, y)
            if not self._out_of_bounds(tx, ty) and self.layout[tx, ty, 0] == 0:
                self.layout[tx, ty] = self.layout[self._dir1[idx](x, y)] = VISITED[:]
                return tx, ty

        return None, None

    def _generate_backtrack(self, stack):
        """Backtrack the stack until walking is possible again."""
        while stack:
            x, y = stack.pop()
            for direction in self._dir2:
                tx, ty = direction(x, y)
                if not self._out_of_bounds(tx, ty) and self.layout[tx, ty, 0] == 0:
                    return x, y

        return None, None

    def _out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.row_count_with_walls or y >= self.col_count_with_walls
    
    def save_maze(self, file_name="./media/maze.png", scale=3):
        """Save maze to file in subdirectory."""
        if self.layout is None:
            raise MazeError(
                "Cannot save maze because it is not assigned.\n"
                "Use the \"create\" or \"load_maze\" method to create or load a maze."
            )

        Image.fromarray(self.scale_layout(scale), "RGB").save(file_name, "png")
    
    def scale_layout(self, scale):
        """Scale maze."""
        if not isinstance(self.layout, np.ndarray):
            self.layout = np.array(self.layout)
        
        return self.layout.repeat(scale, axis=0).repeat(scale, axis=1)


class Wall:
    """Maze's wall class. Represents a single block of the wall."""
    def __init__(self, pos):
        self.rect = Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)


class MazeError(Exception):
    def __init__(self, e):
        super(MazeError, self).__init__(e)