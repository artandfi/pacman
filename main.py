import os
import sys
import pygame
import colors


from maze import Maze, MazeWall
from player import Player
from constants import BLOCK_SIZE, M, N, SCREEN_WIDTH, SCREEN_HEIGHT


def init():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_caption("Maze generator by artandfi")


def fill_walls():
    x = y = 0
    for row in layout:
        for cell in row:
            if cell == 1:
                walls.append(MazeWall((x, y)))
            x += BLOCK_SIZE
        
        y += BLOCK_SIZE
        x = 0


def run():
    running = True
    while running:
        clock.tick(60)
    
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-2, 0)
        if key[pygame.K_RIGHT]:
            player.move(2, 0)
        if key[pygame.K_UP]:
            player.move(0, -2)
        if key[pygame.K_DOWN]:
            player.move(0, 2)

        if player.rect.colliderect(end_rect):
            pygame.quit()
            sys.exit()

        screen.fill(colors.WHITE)
        for wall in walls:
            pygame.draw.rect(screen, colors.BLACK, wall.rect)
    
        pygame.draw.rect(screen, colors.RED, end_rect)
        pygame.draw.rect(screen, colors.GREEN, player.rect)
        pygame.display.flip()
        clock.tick(360)


def save():
    maze.save_maze()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
walls = []
maze = Maze(M, N)
player = Player(walls)
end_rect = pygame.Rect(SCREEN_WIDTH-2*BLOCK_SIZE, SCREEN_HEIGHT-2*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
layout = maze.generate()


def main():
    init()
    fill_walls()
    run()
    save()
    pygame.quit()


if __name__ == "__main__":
    main()
