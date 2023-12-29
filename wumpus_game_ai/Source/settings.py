import pygame

# Speed
SPEED = 150  # Change the speed of the game here.

# Window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
CAPTION = 'AI Game Wumpus World !!!' 

# Cell
IMAGE_INITIAL_CELL = '../Images/initial_cell.png'
IMAGE_DISCOVERED_CELL = '../Images/discovered_cell.png'

# Object
IMAGE_PIT = '../Images/pit.jpg'
IMAGE_WUMPUS = '../Images/wumpus.png'
IMAGE_GOLD = '../Images/gold.jpg'

# Hunter
IMAGE_AGENT_RIGHT = '../Images/agent_right.png'

IMAGE_ARROW_RIGHT = '../Images/arrow_right.png'

# Map
MAP_LIST = ['../Input/map1.txt',
            '../Input/map2.txt',
            '../Input/map3.txt',
            '../Input/map4.txt',
            '../Input/map5.txt']
MAP_NUM = len(MAP_LIST)

# Output
OUTPUT_LIST = ['../Output/result_1.txt',
                '../Output/result_2.txt',
                '../Output/result_3.txt',
                '../Output/result_4.txt',
                '../Output/result_5.txt']

# FONTS = '../Fonts/mrsmonster.ttf'
# FONTS = '../Fonts/ChrustyRock-ORLA.ttf'
FONTS = '../Fonts/YeastyFlavorsRegular-yweyd.ttf'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (170, 170, 170)
DARK_GREY = (75, 75, 75)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# state
RUNNING = 'running'
GAMEOVER = 'gameover'
WIN = 'win'
TRYBEST = 'trybest'
MAP = 'map'
ALGORITHM = 'algorithm'

LEVEL_1_POS = pygame.Rect(235, 120, 500, 50)
LEVEL_2_POS = pygame.Rect(235, 200, 500, 50)
LEVEL_3_POS = pygame.Rect(235, 280, 500, 50)
LEVEL_4_POS = pygame.Rect(235, 360, 500, 50)
LEVEL_5_POS = pygame.Rect(235, 440, 500, 50)
EXIT_POS = pygame.Rect(235, 520, 500, 50)
