import pygame
from pygame.sprite import Sprite

BLOCK_SIZE = 25

class Ghost(Sprite):
    def __init__(self, ai_game, tup_pos_ghost):
        super().__init__()

        self.screen = ai_game.screen
        self.world = ai_game.world
        self.pos_ghost = tup_pos_ghost
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (25, 25))

    def draw_ghost(self):
        for pos in self.pos_ghost:
            self.screen.blit(self.image, (pos[1] * BLOCK_SIZE, pos[0] * BLOCK_SIZE))