import pygame
from settings import *
import os

class Map:
    def __init__(self, init_agent_pos):
        self.space = 10
        self.size = 10 # size map
        self.cell_size = 60 # size cell

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_parent_dir = os.path.dirname(self.current_dir)     
        

        # load image
        self.cell = pygame.image.load(IMAGE_INITIAL_CELL).convert()
        self.pit = pygame.image.load(IMAGE_PIT).convert()

        # set state pit and cell 
        # False: not discover
        # True: discover
        self.pit_discover = [[False for i in range(self.size)] for j in range(self.size)]
        self.discover_cell = pygame.image.load(IMAGE_DISCOVERED_CELL).convert()
        self.is_discover = [[False for i in range(self.size)] for j in range(self.size)]
        self.is_discover[init_agent_pos[0] - 1][init_agent_pos[1] - 1] = True

    def draw(self, screen):
        x = self.space
        y = self.space

        for i in range(0, self.size):
            for j in range(0, self.size):
                # Check if cell is discover
                if(self.is_discover[i][j]):
                    screen.blit(self.discover_cell, (x, y))
                    x += self.space + self.cell_size
                # Check if cell is not discover
                elif not self.is_discover[i][j]:
                    # Check if cell is pit
                    if self.pit_discover[i][j]:
                        screen.blit(self.pit, (x, y))
                        x += self.space + self.cell_size
                    # Check if cell is not pit
                    else:
                        screen.blit(self.cell, (x, y))
                        x += self.space + self.cell_size
            y += self.space + self.cell_size
            x = self.space

    # updated cell discover at position x, y -> True
    def discover_cell_i_j(self, x, y):
        self.is_discover[x][y] = True
    
    # return list cell discover
    def discovered(self):
        return self.is_discover
    
    # updated pit discover at position x, y -> set True
    def discover_pit(self, x, y):
        self.pit_discover[x][y] = True

    # show result
    def agent_climb(self, screen, font):
        text = font.render('Climbed out !!!', True, RED)
        textRect = text.get_rect()
        textRect.center = (900, 100)
        screen.blit(text, textRect)
        text = font.render('Score + 10', True, RED)
        textRect.center = (920, 150)
        screen.blit(text, textRect)
    
    def agent_grab_all_gold_and_kill_wumpus(self, screen, font):
        text = font.render('Grab all Gold and ', True, RED)
        textRect = text.get_rect()
        textRect.center = (900, 200)
        screen.blit(text, textRect)
        text = font.render('Kill all Wumpus !!!', True, RED)
        textRect = text.get_rect()
        textRect.center = (900, 250)
        screen.blit(text, textRect)
    def pit_detect(self, i, j):
        self.pit_discover[i][j] = True