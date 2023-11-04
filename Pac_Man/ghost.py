import pygame
from pygame.sprite import Sprite
from Astar import *

BLOCK_SIZE = 25
WIDTH, HEIGHT = 800, 450

class Ghost(Sprite):
    def __init__(self, ai_game, tup_pos_ghost):
        super().__init__()

        self.screen = ai_game.screen
        self.world = ai_game.world
        self.pos_ghost = tup_pos_ghost
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (25, 25))

    # Draw ghost on the screen
    def draw_ghost(self):
        map_width = len(self.world[0]) * BLOCK_SIZE
        map_height = len(self.world) * BLOCK_SIZE

        map_x = (WIDTH - map_width) // 2
        map_y = (HEIGHT - map_height) // 2

        for pos in self.pos_ghost:
            self.screen.blit(self.image, (map_x + pos[1] * BLOCK_SIZE, map_y + pos[0] * BLOCK_SIZE))

    # 
    def move_ghosts_to_pacman(self, pacman_pos):
        for i in range(len(self.pos_ghost)):
            # Tìm đường đi từ vị trí hiện tại của con ma đến vị trí của pacman bằng A*
            path = Astar(self.world, self.pos_ghost[i], pacman_pos)

            if path:
                # Nếu có đường đi, thì di chuyển con ma tới vị trí tiếp theo trong đường đi
                next_pos = path[1] if len(path) > 1 else path[0]
                self.pos_ghost[i] = next_pos
