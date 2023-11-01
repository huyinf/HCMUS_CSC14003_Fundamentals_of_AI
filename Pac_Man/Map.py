import pygame

BLOCK_SIZE = 25
WIDTH, HEIGHT = 800, 750

class Map:  
    def __init__(self, ai_game):
        # Store map
        self.world = []
        self.screen = ai_game.screen

        # Identify position food
        self.pos_food = []

        # Identify position pacman
        self.pos_pacman = []

        # Identify position ghost
        self.pos_ghost = []

        # Convert char to image
        # 1: wall
        # 2: Goal (Large Food)
        self.char_to_image = {
            1: pygame.transform.scale(pygame.image.load(f'images/wall.png'), (25,25)),
            2: pygame.transform.scale(pygame.image.load(f'images/power.png'), (25,25)),
        }

    # Read map level return map and position pacman
    def load_level(self, number1, number2):
        file = f"level/level-{number1}/map{number2}.txt"  # Use proper string formatting
        with open(file, 'r') as f:
            lines = f.readlines()

            rows, cols = map(int, lines[0].split())
            self.world = [[int(cell) for cell in line.strip()] for line in lines[1:rows + 1]]

            self.pos_pacman = tuple(map(int, lines[rows + 1].split()))

            return self.world
    
    # Draw map
    def draw_map(self):
        for y, row in enumerate(self.world):
            for x, block in enumerate(row):
                image = self.char_to_image.get(block, None)
                if image:
                    self.screen.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    # Position Food
    def _pos_food(self):
        for y, row in enumerate(self.world):
            for x, block in enumerate(row):
                if self.world[y][x] == 2:
                    self.pos_food.append(y)
                    self.pos_food.append(x)
        return self.pos_food
    
    # Position Ghost
    def _pos_ghost(self):
        for y, row in enumerate(self.world):
            for x, block in enumerate(row):
                if self.world[y][x] == 3:
                    pos = (y, x)
                    self.pos_ghost.append(pos)
        return self.pos_ghost

    # Position Pacman 
    def _pos_pacman(self):
        return self.pos_pacman