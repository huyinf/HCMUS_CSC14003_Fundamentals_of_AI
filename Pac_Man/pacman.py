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
    def move_pacman(self):
        if not self.check_collision_wall():
            # Update Pac-Man's position based on the direction
            if self.turns_allowed[0] and self.rect.right < self.screen.get_rect().right:
                self.rect.x += 1
            elif self.turns_allowed[1] and self.rect.left >= 0:
                self.rect.x -= 1
            elif self.turns_allowed[2] and self.rect.top >= 0:
                self.rect.y -= 1
            elif self.turns_allowed[3] and self.rect.bottom < self.screen.get_rect().bottom:
                self.rect.y += 1

    # Check collision wall
    def check_collision_wall(self):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        x = self.rect.x
        y = self.rect.y
        
        if self.direction == 0:
            x += 1
        elif self.direction == 1:
            x -= 1
        elif self.direction == 2:
            y -= 1
        elif self.direction == 3:
            y += 1

        # Find integer block position, using floor
        ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)

        # Check if Pac-Man collides with walls in the current and adjacent blocks
        if self.world[iy][ix] == 1:
            return True  # Collision with a wall
        elif self.direction == 0:
            if (x % BLOCK_SIZE) + 1 > BLOCK_SIZE // 2:
                if self.world[iy][ix + 1] == 1:
                    return True
        elif self.direction == 1:
            if (x % BLOCK_SIZE) < BLOCK_SIZE // 2:
                if self.world[iy][ix - 1] == 1:
                    return True
        elif self.direction == 2:
            if (y % BLOCK_SIZE) < BLOCK_SIZE // 2:
                if self.world[iy - 1][ix] == 1:
                    return True
        elif self.direction == 3:
            if (y % BLOCK_SIZE) + 1 > BLOCK_SIZE // 2:
                if self.world[iy + 1][ix] == 1:
                    return True

        return False  # No collision

