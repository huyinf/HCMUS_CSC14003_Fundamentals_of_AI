import pygame

BLOCK_SIZE = 25

class Map:  
    def __init__(self, ai_game):
        # Store level
        self.world = []
        self.screen = ai_game.screen
        self.food = []

        # Convert char to image
        self.char_to_image = {
            1: pygame.transform.scale(pygame.image.load(f'images/wall.png'), (25,25)),
            2: pygame.transform.scale(pygame.image.load(f'images/power.png'), (25,25)),
        }

    # Read map level return map and position pacman
    def load_level(self, number):
        file = f"level/level-{number}.txt"  # Use proper string formatting
        with open(file, 'r') as f:
            lines = f.readlines()

            rows, cols = map(int, lines[0].split())
            self.world = [[int(cell) for cell in line.strip()] for line in lines[1:rows + 1]]

            pacman_pos = tuple(map(int, lines[rows + 1].split()))

            return self.world, pacman_pos
    
    # Draw map
    def draw_map(self):
        for y, row in enumerate(self.world):
            for x, block in enumerate(row):
                image = self.char_to_image.get(block, None)
                if self.world[y][x] == 2:
                    self.food.append(x)
                    self.food.append(y)
                if image:
                    self.screen.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    # Position Food
    def pos_food(self):
        for y, row in enumerate(self.world):
            for x, block in enumerate(row):
                image = self.char_to_image.get(block, None)
                if self.world[y][x] == 2:
                    self.food.append(x)
                    self.food.append(y)
        return self.food
