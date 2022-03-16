import os
import sys
import pygame
import colors
import easygui


from maze import Maze, MazeWall
from player import Player
from constants import BLOCK_SIZE, ROWS, COLUMNS, SCREEN_HEIGHT, SCREEN_WIDTH, SPEED, WALL, A_STAR, GREEDY, BY_HAND
from solver import MazeSolverAStar


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


def draw_path(path, start_cell, end_cell, screen):
    cell = path[start_cell]
    while cell != end_cell:
        rect = pygame.Rect(cell.y*BLOCK_SIZE, cell.x*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, colors.BLUE, rect)
        cell = path[cell]


def run():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    maze = Maze(COLUMNS, ROWS)
    layout = maze.generate()
    solver = MazeSolverAStar(maze)
    start_cell, end_cell, path = solver.solve()
    walls = fill_walls(layout)
    player = Player(walls)
    end_rect = pygame.Rect(SCREEN_WIDTH-2*BLOCK_SIZE, SCREEN_HEIGHT-2*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    running = True
    draw = False
    chosen = False
    
    while running:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

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

        screen.fill(colors.WHITE)
        for wall in walls.values():
            pygame.draw.rect(screen, colors.BLACK, wall.rect)
        
        if draw:
            draw_path(path, start_cell, end_cell, screen)
        
        pygame.draw.rect(screen, colors.RED, end_rect)
        pygame.draw.rect(screen, colors.GREEN, player.rect)
        pygame.display.flip()

        if not chosen:
            choice = prompt()
            chosen = True
            if choice == A_STAR:
                draw = True
        
        clock.tick(360)
    
    maze.save_maze()


def main():
    init()
    run()
    pygame.quit()


if __name__ == "__main__":
    main()
