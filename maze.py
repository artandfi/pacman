import numpy as np


from random import randint
from pygame import Rect
from PIL import Image
from constants import BLOCK_SIZE, UP, RIGHT, FLOOR, WALL
from colors import BLACK, GREEN, RED, WHITE


opposite = lambda d: d - 1 if d % 2 else d + 1


class Maze:
    """Empty maze. To generate walls and corridors, call generate() method."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = width * height
        self.layout = []

    def generate(self):
        self._generate_nodes()
        self._generate_layout()
        return self.layout

    def _generate_nodes(self):
        stack = []
        visited = 0
        position = randint(0, self.size-1)

        self.nodes = [MazeCell(i // self.width, i % self.width) for i in range(self.size)]
        self.nodes[position].visited = True

        while visited < self.size - 1:
            nxt = self._neighbor_positions(position)
            directions = [x[0] for x in list(filter(lambda p: p[1] != -1 and not self.nodes[p[1]].visited, enumerate(nxt)))]

            if directions:
                visited += 1
                dir_count = len(directions)
                
                if dir_count > 1:
                    stack.append(position)
                
                direction = directions[randint(0, len(directions)-1)]

                # Update current position
                self.nodes[position].available_directions[direction] = False
                # Set new position
                position = nxt[direction]

                # Update next position
                self.nodes[position].available_directions[opposite(direction)] = False
                self.nodes[position].visited = True
            else:
                if not stack:
                    break

                position = stack.pop()
    
    def _generate_layout(self):
        row1, row2 = [], []

        if len(self.nodes) != self.size:
            return
        
        for i in range(self.size):
            if not row1:
                row1.append(WALL)
            if not row2:
                row2.append(WALL)

            if self.nodes[i].available_directions[UP]:
                row1.extend([WALL, WALL])
                if self.nodes[i].available_directions[RIGHT]:
                    row2.extend([FLOOR, WALL])
                else:
                    row2.extend([FLOOR, FLOOR])
            else:
                rng = range(len(self.nodes))
                has_above = i - self.width in rng
                above = has_above and self.nodes[i-self.width].available_directions[RIGHT]
                has_next = i + 1 in rng
                nxt = has_next and self.nodes[i+1].available_directions[UP]

                if self.nodes[i].available_directions[RIGHT]:
                    row1.extend([FLOOR, WALL])
                    row2.extend([FLOOR, WALL])
                elif nxt or above:
                    row1.extend([FLOOR, WALL])
                    row2.extend([FLOOR, FLOOR])
                else:
                    row1.extend([FLOOR, FLOOR])
                    row2.extend([FLOOR, FLOOR])
            
            if (i + 1) % self.width == 0:
                self.layout.append(row1)
                self.layout.append(row2)
                row1, row2 = [], []
        
        self.layout.append([WALL] * (self.width*2+1))

    def _neighbor_positions(self, pos):
        return [
            pos - self.width if pos - self.width >= 0 else -1,
            pos + self.width if self.size > pos + self.width else -1,
            pos - 1 if pos > 0 and pos % self.width != 0 else -1,
            pos + 1 if (pos + 1) % self.width != 0 else -1
        ]
    
    def layout_rgb(self):
        width, height = len(self.layout), len(self.layout[0])
        layout = np.zeros((width, height, 3), dtype=np.uint8)

        for i, row in enumerate(self.layout):
            for j, cell in enumerate(row):
                if self.layout[i][j] == WALL:
                    layout[i][j] = BLACK
                else:
                    layout[i][j] = WHITE
        
        layout[1][1] = GREEN
        layout[width-2][height-2] = RED
        return layout

    def save_maze(self, file_name="./media/maze.png", scale=3):
        """Save maze as image file in subdirectory."""
        Image.fromarray(self.scale_layout(scale), "RGB").save(file_name, "png")
    
    def scale_layout(self, scale):
        """Scale maze."""
        layout = self.layout_rgb()
        return layout.repeat(scale, axis=0).repeat(scale, axis=1)


class MazeWall:
    """A single block of the maze's wall."""
    def __init__(self, pos):
        self.rect = Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)


class MazeCell:
    """Cell in a maze's grid prior to layout generation."""
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visited = False
        self.available_directions = [True] * 4
