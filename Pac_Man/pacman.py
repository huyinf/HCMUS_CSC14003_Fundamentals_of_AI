import pygame
from pygame.sprite import Sprite

BLOCK_SIZE = 25
WIDTH, HEIGHT = 800, 450

# Create pacman
class Pacman(Sprite):
    def __init__(self, ai_game, pacmanx, pacmany):
        super().__init__()

        self.screen = ai_game.screen

        self.world = ai_game.world
        self.counter = 0
        self.direction = 0
        
        self.pacman_images = pygame.transform.scale(pygame.image.load(f'assets/player_images/1.png'), (25, 25))
        
        self.rect = self.pacman_images.get_rect()
        self.rect.x = pacmanx * BLOCK_SIZE
        self.rect.y = pacmany * BLOCK_SIZE

        # R, L, U, D
        self.turns_allowed = [False, False, False, False]

    # Draw pacman in screen
    def draw(self):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        self.screen.blit(self.pacman_images, self.rect)

    def move_pacman(self, tup):
        map_width = len(self.world[0]) * BLOCK_SIZE
        map_height = len(self.world) * BLOCK_SIZE

        map_x = (WIDTH - map_width) // 2
        map_y = (HEIGHT - map_height) // 2

        self.rect.x = map_x + tup[1] * BLOCK_SIZE
        self.rect.y = map_y + tup[0] * BLOCK_SIZE