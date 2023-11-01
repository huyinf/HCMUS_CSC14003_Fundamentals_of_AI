import pygame
from Pacman import *
from Map import *
from Astar import *
from Ghost import *

class AI_Search_PacMan():
    def __init__(self):
        pygame.init()

        # Initialize
        self.BLOCK_SIZE_SC = 25
        self.WORLD_SIZE_SC = 25
        self.WIDTH = self.HEIGHT = self.WORLD_SIZE_SC * self.BLOCK_SIZE_SC
        self.TITLE = 'Pac - man AI Search'

        # Set up environment: size, caption, ... for game app
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.TITLE)
        self.timer = pygame.time.Clock()
        
        # Read map
        self.map = Map(self)

        # Read map at folder level-{number1}, map{number2}.txt
        self.world = self.map.load_level(2,1)
        

        # Get position ghost
        ghost_pos = self.map._pos_ghost()
        # Create ghost
        self.ghost = Ghost(self, ghost_pos)

        # Get position food
        self.food = tuple(self.map._pos_food())

        # Get position pacman
        pacman_pos = self.map._pos_pacman()
        # Create pacman
        self.pacman = Pacman(self, pacman_pos[0], pacman_pos[1])

        # Path level 1 - Astar
        self.path_level_1_Astar = Astar(self.world, pacman_pos, self.food)

    # Function Run Game
    def run_game(self):
        self.fps = 4
        self.running = True
        self.path_index = 0  # Initialize the index to the first coordinate in the path

        # Check event
        while self.running:
            # animation pacman image
            if self.pacman.counter < 19:
                self.pacman.counter += 1
            else:
                self.pacman.counter = 0

            # Check events
            self._check_events()
            
            # Astar algorithm - level 1, move Pacman follow Astar
            if self.path_level_1_Astar:
                tup = self.path_level_1_Astar[self.path_index]
                
                # Update position Pacman and move
                self.pacman.move_pacman(tup)            
                self.path_index += 1  # Move to the next coordinate

                # If we have reached the end of the path, stop moving
                if self.path_index >= len(self.path_level_1_Astar):
                    self.path_level_1_Astar = None  # Clear the path or add logic to handle this case

            # update screen
            self._update_screen()

            pygame.display.flip()
            self.timer.tick(self.fps)


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

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
