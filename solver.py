from math import inf
from queue import PriorityQueue
from constants import FLOOR


def h_score(cell1, cell2):
    return abs(cell1.x-cell2.x) + abs(cell1.y-cell2.y)


class MazeSolverBase:
    """Base maze solver."""
    def __init__(self, maze):
        self.maze = maze
        self.height = len(self.cells)
        self.width = len(self.cells[0])
    
    def _start_end_cells(self, start, end):
        if start is None:
            start = (1, 1)
        if end is None:
            end = (self.height-2, self.width-2)
        
        return self.cells[start[0]][start[1]], self.cells[end[0]][end[1]]

    def _neighbor_cells(self, cell):
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
    
    def _reverse_path(self, path, start_cell, end_cell):
        fwd_path = {}
        cell = end_cell
        
        while cell != start_cell:
            fwd_path[path[cell]] = cell
            cell = path[cell]
        
        return fwd_path


class MazeSolverAStar(MazeSolverBase):
    """Solves a maze via A* algorithm."""
    def __init__(self, maze):
        self.cells = [[MazeAStarCell(x, y, maze.layout[x][y]==FLOOR) for y, _ in enumerate(row)] for x, row in enumerate(maze.layout)]
        super().__init__(maze)

    def solve(self, start=None, end=None):
        start_cell, end_cell = self._start_end_cells(start, end)
        start_cell.g = 0
        start_cell.h = h_score(start_cell, end_cell)

        queue = PriorityQueue()
        queue.put((start_cell.h, start_cell.h, start_cell))
        path = {}

        while not queue.empty():
            cell = queue.get()[-1]

            if cell == end_cell:
                break
            
            neighbors = self._neighbor_cells(cell)

            for new_cell in neighbors:
                g = cell.g + 1
                h = h_score(new_cell, end_cell)
                f = g + h

                if f < new_cell.f:
                    new_cell.g, new_cell.h = g, h
                    queue.put((f, h, new_cell))

                    path[new_cell] = cell
        
        return start_cell, end_cell, self._reverse_path(path, start_cell, end_cell)


class MazeSolverGreedy(MazeSolverBase):
    """Solves a maze via greedy (best-first) algorithm."""
    def __init__(self, maze):
        self.cells = [[MazeGreedyCell(x, y, maze.layout[x][y]==FLOOR) for y, _ in enumerate(row)] for x, row in enumerate(maze.layout)]
        super().__init__(maze)
    
    def solve(self, start=None, end=None):
        start_cell, end_cell = self._start_end_cells(start, end)
        path = {}
        visited = set()
        queue = PriorityQueue()

        visited.add(start_cell)
        queue.put((start_cell.h, start_cell))

        while not queue.empty():
            cell = queue.get()[-1]
            neighbors = list(filter(lambda c: c not in visited, self._neighbor_cells(cell)))

            if cell == end_cell:
                break

            for new_cell in neighbors:
                visited.add(new_cell)
                queue.put((new_cell.h, new_cell))
                path[new_cell] = cell
        
        return start_cell, end_cell, self._reverse_path(path, start_cell, end_cell)


class MazePathfindingCellBase:
    """Cell in a maze's grid for pathfinding."""
    def __init__(self, x, y, is_floor):
        self.x = x
        self.y = y
        self.is_floor = is_floor

    def __hash__(self):
        return (self.x, self.y).__hash__()
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


class MazeAStarCell(MazePathfindingCellBase):
    """Cell in a maze's grid for A* pathfinding."""
    def __init__(self, x, y, is_floor):
        super().__init__(x, y, is_floor)
        self.g = inf
        self.h = inf
    
    @property
    def f(self):
        return self.g + self.h
    

class MazeGreedyCell(MazePathfindingCellBase):
    """Cell in a maze's grid for greedy (best-first) pathfinding."""
    def __init__(self, x, y, is_floor):
        super().__init__(x, y, is_floor)
        self.h = 0
