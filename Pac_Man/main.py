import pygame
from pacman import *
from Map import *
from Astar import *

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
        
        # Read map at folder level-1, map1.txt
        self.world, pacman_pos = self.map.load_level(1,1)

        # Get position food
        self.food = tuple(self.map.pos_food())

        # Create pacman
        self.pacman = Pacman(self, pacman_pos[0], pacman_pos[1])

        # Path level 1 - Astar
        self.path_level_1_Astar = Astar(self.world, pacman_pos, self.food)

    # Function Run Game
    def run_game(self):
        self.fps = 5
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
            
            # Astar algorithm - level 1
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

            # Check key down
            if event.type == pygame.KEYDOWN:
                self.pacman.turns_allowed = [False, False, False, False]
                if event.key == pygame.K_RIGHT:
                    self.pacman.turns_allowed[0] = True
                    self.pacman.direction = 0
                if event.key == pygame.K_LEFT:
                    self.pacman.turns_allowed[1] = True
                    self.pacman.direction = 1
                if event.key == pygame.K_UP:
                    self.pacman.turns_allowed[2] = True
                    self.pacman.direction = 2
                if event.key == pygame.K_DOWN:
                    self.pacman.turns_allowed[3] = True
                    self.pacman.direction = 3

            # Check key up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.pacman.turns_allowed[0] = False
                if event.key == pygame.K_LEFT:
                    self.pacman.turns_allowed[1] = False
                if event.key == pygame.K_UP:
                    self.pacman.turns_allowed[2] = False
                if event.key == pygame.K_DOWN:
                    self.pacman.turns_allowed[3] = False

    def _update_screen(self):
        self.screen.fill((0, 0, 0))

        # Draw map
        self.map.draw_map()

        # Draw Pacman
        self.pacman.draw()

        pygame.display.flip()
    
if __name__ == '__main__':
    ai_search_pacman = AI_Search_PacMan()
    ai_search_pacman.run_game()
