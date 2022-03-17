import os
import sys
import pygame
import colors
import easygui


from maze import Maze, MazeWall
from player import Player
from constants import BLOCK_SIZE, ROWS, COLUMNS, SCREEN_HEIGHT, SCREEN_WIDTH, SPEED, WALL, A_STAR, GREEDY, BY_HAND
from solver import MazeSolverAStar, MazeSolverGreedy


def init():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_caption("Maze generator & solver by artandfi")


def prompt():
    choices = ["A* (automatic)", "Greedy (automatic)", "On my own!"]
    choice = easygui.buttonbox("How do you wanna solve the generated maze?", choices=choices)
    return choices.index(choice)


def fill_walls(layout):
    walls = {}
    x = y = 0

    for row in layout:
        for cell in row:
            if cell == WALL:
                walls[(x, y)] = MazeWall((x, y))
            x += BLOCK_SIZE
        
        y += BLOCK_SIZE
        x = 0
    
    return walls


def move(player, end_rect):
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-SPEED, 0)
    if key[pygame.K_RIGHT]:
        player.move(SPEED, 0)
    if key[pygame.K_UP]:
        player.move(0, -SPEED)
    if key[pygame.K_DOWN]:
        player.move(0, SPEED)

    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()


def draw_maze(screen, walls):
    screen.fill(colors.WHITE)
    for wall in walls.values():
        pygame.draw.rect(screen, colors.BLACK, wall.rect)


def draw_endpoints(screen, player_rect, end_rect):
    pygame.draw.rect(screen, colors.RED, end_rect)
    pygame.draw.rect(screen, colors.GREEN, player_rect)


def draw_path(path, start_cell, end_cell, screen):
    cell = path[start_cell]

    while cell != end_cell:
        rect = pygame.Rect(cell.y*BLOCK_SIZE, cell.x*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, colors.ORANGE, rect)
        
        cell = path[cell]


def traverse_path(path, start_cell, end_cell, player):
    cell = path[start_cell]

    while cell != end_cell:
        player.rect.x, player.rect.y = cell.y * BLOCK_SIZE, cell.x * BLOCK_SIZE
        cell = path[cell]

def traverse_path_step(path, current_cell, player):
    cell = path[current_cell]
    player.rect.x, player.rect.y = cell.y * BLOCK_SIZE, cell.x * BLOCK_SIZE
    
    return cell


def run():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    maze = Maze(COLUMNS, ROWS)
    layout = maze.generate()
    start_cell, end_cell, path = None, None, None
    walls = fill_walls(layout)
    player = Player(walls)
    end_rect = pygame.Rect(SCREEN_WIDTH-2*BLOCK_SIZE, SCREEN_HEIGHT-2*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    path_cell = None

    running = True
    auto_draw = False
    chosen = False
    
    while running:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        if not auto_draw:
            move(player, end_rect)
        
        draw_maze(screen, walls)
        
        if auto_draw:
            draw_path(path, start_cell, end_cell, screen)
            if path_cell != end_cell:
                path_cell = traverse_path_step(path, path_cell, player)
            else:
                auto_draw = False

        draw_endpoints(screen, player.rect, end_rect)
        pygame.display.flip()

        if not chosen:
            solvers = [MazeSolverAStar, MazeSolverGreedy]
            choices = ["A* (automatic)", "Greedy (automatic)", "On my own!"]
            choice = choices.index(easygui.buttonbox("How do you wanna solve the generated maze?", choices=choices))
            chosen = True

            if choice != BY_HAND:
                auto_draw = True
                start_cell, end_cell, path = solvers[choice](maze).solve()
                path_cell = start_cell
        
        clock.tick(360)
    
    maze.save_maze(path=path)


def main():
    init()
    run()
    pygame.quit()


if __name__ == "__main__":
    main()
