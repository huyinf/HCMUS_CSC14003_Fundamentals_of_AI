import pygame
from Pacman import *
from Map import *
from Astar import *
from Ghost import *
from BFS import *

class AI_Search_PacMan():
    def __init__(self):
        pygame.init()

        # Initialize
        self.WIDTH, self.HEIGHT = 800, 450
        self.TITLE = 'Pac - man AI Search'

        # Set up environment: size, caption, ... for game app
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.TITLE)
        self.timer = pygame.time.Clock()

        # set current map level
        self.current_map_level = 1
        self.path_level_1_Astar = None
        self.path_index = 0

        # BFS for level 1 2
        self.path_level_1_BFS = None

    # Function Run Game
    def run_game(self):
        self.fps = 5
        self.running = True
        self.path_index = 0  # Initialize the index to the first coordinate in the path

        # Check event
        while self.running:
            # Check events
            self._check_events()
            
            ''' Check current map level '''
            # Current map level 1
            if self.current_map_level == 1:
                self._state_curr_level_1()

            # Current map level 2
            elif self.current_map_level == 2:
                self._state_curr_level_2()

            # Current map level 3
            elif self.current_map_level == 3:
                self._state_curr_level_3()

            # Current map level 4
            elif self.current_map_level == 4:
                self._state_curr_level_4()
            
            # update screen
            self._update_screen()

            pygame.display.flip()
            self.timer.tick(self.fps)

    ''' ######################### Read Map ############################### '''

    # Read map level at folder level-{number1}, map{number2}.txt
    def _read_map_level(self, number1, number2):
        # Read map
        self.map = Map(self)

        # Read map at folder level/level-{number1}/map{number2}.txt
        self.world = self.map.load_level(number1, number2)
        
        # Get position ghost
        ghost_pos = self.map._pos_ghost()
        # Create ghost
        self.ghost = Ghost(self, ghost_pos)

        # Get position food
        self.food = tuple(self.map._pos_food())

        # Get position pacman
        self.pacman_pos = self.map._pos_pacman()
        # Create pacman
        self.pacman = Pacman(self, self.pacman_pos[0], self.pacman_pos[1])

    ''' ######################### Level 1 ############################### '''
    # def _state_curr_level_1(self):
    #     if self.path_level_1_Astar is None:
    #         # Load map at folder level/level-1/map2.txt
    #         self._read_map_level(2, 1)
    #         self.path_level_1_Astar = Astar(self.world, self.pacman_pos, self.food)

    #     # Astar algorithm - level 1, move Pacman follow Astar
    #     if self.path_level_1_Astar:
    #         if self.path_index < len(self.path_level_1_Astar):
    #             tup = self.path_level_1_Astar[self.path_index]

    #             # Update position Pacman and move
    #             self.pacman.move_pacman(tup)
    #             self.path_index += 1  # Move to the next coordinate
    
    ''' ------------------------- BFS level 1 + 2 ------------------------- '''
    def _state_curr_level_1(self):
        if self.path_level_1_Astar is None:
            # Load map at folder level/level-1/map2.txt
            self._read_map_level(2, 1)
            # self.path_level_1_Astar = Astar(self.world, self.pacman_pos, self.food)
            self.path_level_1_BFS = bfs(self.world, self.pacman_pos, self.food)

        # Astar algorithm - level 1, move Pacman follow Astar
        if self.path_level_1_BFS:
            if self.path_index < len(self.path_level_1_BFS):
                tup = self.path_level_1_BFS[self.path_index]

                # Update position Pacman and move
                self.pacman.move_pacman(tup)
                self.path_index += 1  # Move to the next coordinate
    
    ''' ######################### Level 2 ############################### '''

    # State current map level 2
    def _state_curr_level_2(self):
        if self.path_level_1_Astar is None:

            # Load map at folder level/level-2/map1.txt
            self._read_map_level(2, 1)
            self.path_level_1_Astar = Astar(self.world, self.pacman_pos, self.food)
        
        # Astar algorithm - level 1, move Pacman follow Astar
        if self.path_level_1_Astar:
            if self.path_index < len(self.path_level_1_Astar):
                tup = self.path_level_1_Astar[self.path_index]

                # Update position Pacman and move
                self.pacman.move_pacman(tup)
                self.path_index += 1  # Move to the next coordinate
    
    ''' ######################### Level 3 ############################### '''
    def _state_curr_level_3(self):
        pass


    ''' ######################### Level 4 ############################### '''
    def _state_curr_level_4(self):
            pass
    
    ''' ######################### Event ############################### '''
    # Check event
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    # Update screen
    def _update_screen(self):
        self.screen.fill((0, 0, 0))

        # Draw map
        self.map.draw_map()

        # Draw Pacman
        self.pacman.draw()

        # Draw Ghost
        self.ghost.draw_ghost()

        pygame.display.flip()
    
if __name__ == '__main__':
    ai_search_pacman = AI_Search_PacMan()
    ai_search_pacman.run_game()
