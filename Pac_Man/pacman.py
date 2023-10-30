import pygame
from pygame.sprite import Sprite

BLOCK_SIZE = 32

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
            self.pacman_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (22, 22)))
        
        # self.image = pygame.transform.scale(pygame.image.load(f'assets/player_images/1.png'),(22,22))
        
        self.rect = self.pacman_images[0].get_rect()
        self.rect.x = pacmanx
        self.rect.y = pacmany

        # R, L, U, D
        self.turns_allowed = [False, False, False, False]

    # Update position pacman
    def move_pacman(self):
        # Check move Right
        if self.turns_allowed[0] and self.rect.right < self.screen.get_rect().right:
            self.rect.x += 1

        # Check move Left
        if self.turns_allowed[1] and self.rect.left >= 0:
            self.rect.x -= 1

        # Check move Up
        if self.turns_allowed[2] and self.rect.top >= 0:
            self.rect.y -= 1
        
        # Check move Down
        if self.turns_allowed[3] and self.rect.bottom < self.screen.get_rect().bottom:
            self.rect.y += 1

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

    # Check block (wall) ahead of pacman
    # def block_ahead_of_pacman(self):
    #     # Position where pacman wants to move
    #     x = self.rect.x
    #     y = self.rect.y

    #     # Calculate the next position based on the direction
    #     if self.direction == 0:
    #         x += BLOCK_SIZE
    #     elif self.direction == 1:
    #         x -= BLOCK_SIZE
    #     elif self.direction == 2:
    #         y -= BLOCK_SIZE
    #     elif self.direction == 3:
    #         y += BLOCK_SIZE

    #     # Find wall position
    #     ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)

    #     # Remainder lets us check adjacent blocks
    #     rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE

    #     blocks = [self.world[iy][ix]]

    #     if self.direction == 0:
    #         if rx: blocks.append(self.world[iy][ix + 1])
    #     elif self.direction == 1:
    #         if rx: blocks.append(self.world[iy][ix - 1])
    #     elif self.direction == 2:
    #         if ry: blocks.append(self.world[iy - 1][ix])
    #     elif self.direction == 3:
    #         if ry: blocks.append(self.world[iy + 1][ix])

    #     return blocks

        
