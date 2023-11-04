import pygame
import os


BLOCK_SIZE = 25
WIDTH, HEIGHT = 800, 450
current_dir = os.path.dirname(os.path.abspath(__file__))


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

        wall_path = os.path.join(current_dir,'images','wall.png')
        power_path = os.path.join(current_dir,'images','power.png')
        # Convert char to image
        # 1: wall
        # 2: Goal (Large Food)
        self.char_to_image = {
            1: pygame.transform.scale(pygame.image.load(wall_path), (25,25)),
            2: pygame.transform.scale(pygame.image.load(power_path), (25,25)),
        }

    # Read map level return map and position pacman
    def load_level(self, number1, number2):
        file = os.path.join(current_dir, f"map/level-{number1}/map{number2}.txt")
        # file = f"map/level-{number1}/map{number2}.txt"  # Use proper string formatting
        with open(file, 'r') as f:
            lines = f.readlines()

            rows, cols = map(int, lines[0].split())
            self.world = [[int(cell) for cell in line.strip()] for line in lines[1:rows + 1]]

            self.pos_pacman = tuple(map(int, lines[rows + 1].split()))

            return self.world
    
    # Draw map
    def draw_map(self):
        map_width = len(self.world[0]) * BLOCK_SIZE
        map_height = len(self.world) * BLOCK_SIZE

        map_x = (WIDTH - map_width) // 2
        map_y = (HEIGHT - map_height) // 2

        for y, row in enumerate(self.world):
            for x, block in enumerate(row):
                image = self.char_to_image.get(block, None)
                if image:
                    block_x = map_x + x * BLOCK_SIZE
                    block_y = map_y + y * BLOCK_SIZE
                    self.screen.blit(image, (block_x, block_y))

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
    # function get cell
    def init_cells(self):
      
        cells = []
        for y in range(len(self.world)):
            row = []
            for x in range(len(self.world[y])):
                if self.world[y][x] != 1:
                    if self.world[y][x] == 0:
                        row.append(Cell((x, y), []))
                    else:
                        row.append(Cell((x, y), [CState(self[y][x])]))
                else:
                    row.append(None)
            cells.append(row)

        return cells
