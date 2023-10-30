import pygame
import sys

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 40
PACMAN_COLOR = (255, 255, 0)
WALL_COLOR = (0, 0, 255)
DOT_COLOR = (255, 255, 255)

# Map layout
map_data = [
    "####################",
    "#............#.....#",
    "#.####.#####.#.####.#",
    "#.#  #.#   #.#  #.#",
    "#.#  #.#   #.#  #.#",
    "#.####.#####.#.####.#",
    "#.................#",
    "####################"
]

def draw_map(screen):
    for row, line in enumerate(map_data):
        for col, char in enumerate(line):
            x = col * GRID_SIZE
            y = row * GRID_SIZE

            if char == '#':
                pygame.draw.rect(screen, WALL_COLOR, (x, y, GRID_SIZE, GRID_SIZE))
            elif char == '.':
                pygame.draw.circle(screen, DOT_COLOR, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
            elif char == 'P':
                pygame.draw.circle(screen, PACMAN_COLOR, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 2)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Map")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_map(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()