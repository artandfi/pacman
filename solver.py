from math import inf
from queue import PriorityQueue
from constants import FLOOR

def h_score(cell1, cell2):
    return abs(cell1.x-cell2.x) + abs(cell1.y-cell2.y)


class MazeSolverBase:
    def __init__(self, maze):
        self.maze = maze
        self.height = len(self.cells)
        self.width = len(self.cells[0])
    
    def neighbor_cells(self, cell):
        up_index = cell.x - 1
        down_index = cell.x + 1
        left_index = cell.y - 1
        right_index = cell.y + 1

        return list(filter(None, [
            self.cells[up_index][cell.y] if up_index >= 0 and self.cells[up_index][cell.y].is_floor else None,
            self.cells[down_index][cell.y] if down_index < self.height and self.cells[down_index][cell.y].is_floor else None,
            self.cells[cell.x][left_index] if left_index >= 0 and self.cells[cell.x][left_index].is_floor else None,
            self.cells[cell.x][right_index] if right_index < self.width and self.cells[cell.x][right_index].is_floor else None
        ]))


class MazeSolverAStar(MazeSolverBase):
    def __init__(self, maze):
        self.cells = [[MazeAStarCell(x, y, maze.layout[x][y]==FLOOR) for y, _ in enumerate(row)] for x, row in enumerate(maze.layout)]
        super(MazeSolverAStar, self).__init__(maze)

    def solve(self, start=None, end=None):
        if start is None:
            start = (1, 1)
        if end is None:
            end = (self.height-2, self.width-2)
        
        start_cell, end_cell = self.cells[start[0]][start[1]], self.cells[end[0]][end[1]]
        start_cell.g = 0
        start_cell.h = h_score(start_cell, end_cell)

        queue = PriorityQueue()
        queue.put((start_cell.h, start_cell.h, start_cell))
        path = {}

        while not queue.empty():
            cell = queue.get()[-1]

            if cell == end_cell:
                break
            
            neighbors = self.neighbor_cells(cell)

            for new_cell in neighbors:
                g = cell.g + 1
                h = h_score(new_cell, end_cell)
                f = g + h

                if f < new_cell.f:
                    new_cell.g, new_cell.h = g, h
                    queue.put((f, h, new_cell))

                    path[new_cell] = cell
        
        fwd_path = {}
        cell = end_cell
        
        while cell != start_cell:
            fwd_path[path[cell]] = cell
            cell = path[cell]
        
        return start_cell, end_cell, fwd_path


class MazeAStarCell:
    """Cell in a maze's grid for A* pathfinding."""
    def __init__(self, x, y, is_floor):
        self.x = x
        self.y = y
        self.g = inf
        self.h = inf
        self.is_floor = is_floor
    
    @property
    def f(self):
        return self.g + self.h

    def __hash__(self):
        return (self.x, self.y).__hash__()
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    
    def __repr__(self):
        return f"({self.x},{self.y}) G={self.g} H={self.h} F={self.f} {'W' if not self.is_floor else ''}"
