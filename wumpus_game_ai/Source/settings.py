import pygame

# Speed
SPEED = 10  # Change the speed of the game here.

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
OUTPUT_LIST1 = ['../Output_Pro/result1.txt',
                '../Output_Pro/result2.txt',
                '../Output_Pro/result3.txt',
                '../Output_Pro/result4.txt',
                '../Output_Pro/result5.txt']

OUTPUT_LIST2 = ['../Output_FOL/result1.txt',
                '../Output_FOL/result2.txt',
                '../Output_FOL/result3.txt',
                '../Output_FOL/result4.txt',
                '../Output_FOL/result5.txt']

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
