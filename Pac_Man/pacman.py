import pygame
from pygame.sprite import Sprite

BLOCK_SIZE = 25

# Create pacman
class Pacman(Sprite):
    def __init__(self, ai_game, pacmanx, pacmany):
        super().__init__()

        self.screen = ai_game.screen

        self.world = ai_game.world
        self.counter = 0
        self.direction = 0
        self.pacman_images = []
        
        for i in range(1, 5):
            self.pacman_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (20, 20)))
        
        # self.image = pygame.transform.scale(pygame.image.load(f'assets/player_images/1.png'),(22,22))
        
        self.rect = self.pacman_images[0].get_rect()
        self.rect.x = pacmanx
        self.rect.y = pacmany

        # R, L, U, D
        self.turns_allowed = [False, False, False, False]

    # Draw pacman in screen
    def draw(self):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if self.direction == 0:
            self.screen.blit(self.pacman_images[self.counter // 5], self.rect)
        elif self.direction == 1:
            self.screen.blit(pygame.transform.flip(self.pacman_images[self.counter // 5], True, False), self.rect)
        elif self.direction == 2:
            self.screen.blit(pygame.transform.rotate(self.pacman_images[self.counter // 5], 90), self.rect)
        elif self.direction == 3:
            self.screen.blit(pygame.transform.rotate(self.pacman_images[self.counter // 5], 270), self.rect)

    # Move Pacman
    # def check_collision_wall(self, new_rect):
    #     # Determine Pac-Man's new grid position
    #     ix = new_rect.centerx // BLOCK_SIZE
    #     iy = new_rect.centery // BLOCK_SIZE

    #     # Check bounds to avoid out-of-range index errors
    #     if ix < 0 or ix >= len(self.world[0]) or iy < 0 or iy >= len(self.world):
    #         return True  # Pac-Man is out of bounds

    #     # Check for wall collisions in the new position
    #     if self.direction == 0:  # Right
    #         if new_rect.right > (ix + 1) * BLOCK_SIZE:
    #             return True
    #     elif self.direction == 1:  # Left
    #         if new_rect.left < ix * BLOCK_SIZE:
    #             return True
    #     elif self.direction == 2:  # Up
    #         if new_rect.top < iy * BLOCK_SIZE:
    #             return True
    #     elif self.direction == 3:  # Down
    #         if new_rect.bottom > (iy + 1) * BLOCK_SIZE:
    #             return True

    #     return False  # No collision

    def move_pacman(self):
        # Copy the current position to a new rect
        new_rect = self.rect.copy()

        # Update Pac-Man's position based on the direction
        if self.direction == 0 and self.rect.right < self.screen.get_rect().right \
            and self.turns_allowed[0]:  # Right
            new_rect.x += 5
        elif self.direction == 1 and self.rect.left > 0 and self.turns_allowed[1]:  # Left
            new_rect.x -= 5
        elif self.direction == 2 and self.rect.top > 0 and self.turns_allowed[2]:  # Up
            new_rect.y -= 5
        elif self.direction == 3 and self.rect.bottom < self.screen.get_rect().bottom \
            and self.turns_allowed[3]:  # Down
            new_rect.y += 5

        self.rect = new_rect
