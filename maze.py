import os
import numpy as np

from random import randint
from pygame import Rect
from PIL import Image
from constants import BLOCK_SIZE, UP, RIGHT, FLOOR, WALL
from colors import BLACK, BLUE, GREEN, RED, WHITE
from solver import MazeAStarCell

opposite = lambda d: d - 1 if d % 2 else d + 1


class Maze:
    """Empty maze. To generate walls and corridors, call generate() method."""
    def __init__(self, rows, columns):
        self.height = rows
        self.width = columns
        self.size = rows * columns
        self.layout = []

    def generate(self):
        self._generate_nodes()
        self._generate_layout()
        return self.layout

    def _generate_nodes(self):
        stack = []
        visited = 0
        position = randint(0, self.size-1)

        self.cells = [MazeGenerationCell() for i in range(self.size)]
        self.cells[position].visited = True

        while visited < self.size - 1:
            nxt = self._neighbor_positions(position)
            directions = [x[0] for x in list(filter(lambda p: p[1] != -1 and not self.cells[p[1]].visited, enumerate(nxt)))]

            if directions:
                visited += 1
                dir_count = len(directions)
                
                if dir_count > 1:
                    stack.append(position)
                
                direction = directions[randint(0, len(directions)-1)]

                # Update current position
                self.cells[position].available_directions[direction] = False
                # Set new position
                position = nxt[direction]

                # Update next position
                self.cells[position].available_directions[opposite(direction)] = False
                self.cells[position].visited = True
            else:
                if not stack:
                    break

                position = stack.pop()
    
    def _generate_layout(self):
        row1, row2 = [], []

        if len(self.cells) != self.size:
            return
        
        for i in range(self.size):
            if not row1:
                row1.append(WALL)
            if not row2:
                row2.append(WALL)

            if self.cells[i].available_directions[UP]:
                row1.extend([WALL, WALL])
                if self.cells[i].available_directions[RIGHT]:
                    row2.extend([FLOOR, WALL])
                else:
                    row2.extend([FLOOR, FLOOR])
            else:
                rng = range(len(self.cells))
                has_above = i - self.height in rng
                above = has_above and self.cells[i-self.height].available_directions[RIGHT]
                has_next = i + 1 in rng
                nxt = has_next and self.cells[i+1].available_directions[UP]

                if self.cells[i].available_directions[RIGHT]:
                    row1.extend([FLOOR, WALL])
                    row2.extend([FLOOR, WALL])
                elif nxt or above:
                    row1.extend([FLOOR, WALL])
                    row2.extend([FLOOR, FLOOR])
                else:
                    row1.extend([FLOOR, FLOOR])
                    row2.extend([FLOOR, FLOOR])
            
            if (i + 1) % self.height == 0:
                self.layout.append(row1)
                self.layout.append(row2)
                row1, row2 = [], []
        
        self.layout.append([WALL] * (self.height*2+1))

    def _neighbor_positions(self, pos):
        return [
            pos - self.height if pos - self.height >= 0 else -1,
            pos + self.height if self.size > pos + self.height else -1,
            pos - 1 if pos > 0 and pos % self.height != 0 else -1,
            pos + 1 if (pos + 1) % self.height != 0 else -1
        ]
    
    def layout_rgb(self, start_cell, end_cell, path=None):
        height, width = len(self.layout), len(self.layout[0])
        layout = np.zeros((height, width, 3), dtype=np.uint8)

        for i, row in enumerate(self.layout):
            for j, _ in enumerate(row):
                if self.layout[i][j] == WALL:
                    layout[i][j] = BLACK
                else:
                    cell = MazeAStarCell(i, j, True)
                    layout[i][j] = BLUE if path and cell in path else WHITE
        
        layout[start_cell.x][start_cell.y] = GREEN
        layout[end_cell.x][end_cell.y] = RED
        return layout

    def save_maze(self, start_cell, end_cell, file_name="./media/maze.png", scale=3, path=None):
        """Save maze as image file in subdirectory."""
        os.makedirs('media', exist_ok=True)
        Image.fromarray(self.scale_layout(start_cell, end_cell, scale, path), "RGB").save(file_name, "png")
    
    def scale_layout(self, start_cell, end_cell, scale, path=None):
        """Scale maze's layout."""
        layout = self.layout_rgb(start_cell, end_cell, path)
        return layout.repeat(scale, axis=0).repeat(scale, axis=1)


class MazeWall:
    """A single block of the maze's wall."""
    def __init__(self, pos):
        self.rect = Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)


class MazeGenerationCell:
    """Cell in a maze's grid prior to layout generation."""
    def __init__(self):
        self.visited = False
        self.available_directions = [True] * 4
