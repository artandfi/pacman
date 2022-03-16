from pygame import Rect
from constants import BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(object):
    def __init__(self, maze_walls):
        self.rect = Rect(BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        self.maze_walls = maze_walls

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        old_pos = self.rect.x, self.rect.y
        x_mod, y_mod = self.rect.x % BLOCK_SIZE, self.rect.y % BLOCK_SIZE
        closest_x = self.rect.x - x_mod if x_mod < BLOCK_SIZE // 2 else self.rect.x + BLOCK_SIZE - x_mod
        closest_y = self.rect.y - y_mod if y_mod < BLOCK_SIZE // 2 else self.rect.y + BLOCK_SIZE - y_mod

        neighbors = self.neighbor_cells_pos(closest_x, closest_y)
        walls = list(filter(None, [self.maze_walls[n] if n in self.maze_walls else None for n in neighbors]))
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x, self.rect.y = old_pos
    
    def neighbor_cells_pos(self, x, y):
        x_plus, y_plus = x + BLOCK_SIZE, y + BLOCK_SIZE
        x_minus, y_minus = x - BLOCK_SIZE, y - BLOCK_SIZE
        x_plus_fits, y_plus_fits = x_plus < SCREEN_WIDTH, y_plus < SCREEN_HEIGHT
        x_minus_fits, y_minus_fits = x_minus >= 0, y_minus >= 0

        return list(filter(None, [
            (x_plus, y) if x_plus_fits else None,
            (x_minus, y) if x_minus_fits else None,
            (x, y_plus) if y_plus_fits < SCREEN_HEIGHT else None,
            (x, y_minus) if y_minus_fits >= 0 else None,
            (x_minus, y_minus) if x_minus_fits and y_minus_fits else None,
            (x_minus, y_plus) if x_minus_fits and y_plus_fits else None,
            (x_plus, y_minus) if x_plus_fits and y_minus_fits else None,
            (x_plus, y_plus) if x_plus_fits and y_plus_fits else None
        ]))
