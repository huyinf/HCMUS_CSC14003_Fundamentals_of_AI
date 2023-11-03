import pygame
from Pacman import *
from Map import *
from Astar import *
from Ghost import *
from BFS import *

'''
    Thay đổi linh hoạt viết hàm hoạt động level 3 vào có đồ họa sẵn rồi
'''
class AI_Search_PacMan_Level_3():
    def __init__(self):
        pygame.init()

        # Initialize
        self.WIDTH, self.HEIGHT = 800, 450
        self.TITLE = 'Pac - man AI Search'

        # Set up environment: size, caption, ... for game app
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.TITLE)
        self.timer = pygame.time.Clock()

        # Initialize time and score
        self.time_elapsed = 0
        self.score = 0     

        ''' Initialize reached goal:
            False --> Not reached goal
            True  --> reached goal
        '''
        self.reached_goal = False

        # Set up path Astar
        # self.path_level_2_Astar = None

        # Set up path BFS
        # self.path_level_2_BFS = None

        # Check index path in algorithm to pacman move to goal
        # self.path_index = 0

        '''
            Set number to choose algorithm search:
            1: Astar Search (default)
            2: BFS Search
        '''
        # self.index_alg = 1
    
    ''' ######################### RUN GAME #########################- '''
    def run_game(self):
        self.fps = 5
        self.running = True
        self.path_index = 0  # Initialize the index to the first coordinate in the path

        # Start the timer
        start_time = pygame.time.get_ticks()
            
        # Check event
        while self.running:
            # Check events
            self._check_events()
            
            # Check reached goal
            if not self.reached_goal:
                # Calculate the time elapsed
                current_time = pygame.time.get_ticks()
                self.time_elapsed = (current_time - start_time) // 1000 # Convert to seconds
                
                # Main Function level 3
                self._state_curr_level_3()
                
                # update screen
                self._update_screen()

            pygame.display.flip()
            self.timer.tick(self.fps)

    ''' ######################### READ MAP ############################### '''
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
        self.food_pos = tuple(self.map._pos_food())

        # Get position pacman
        self.pacman_pos = self.map._pos_pacman()
        # Create pacman
        self.pacman = Pacman(self, self.pacman_pos[0], self.pacman_pos[1])

    ''' ######################### FUNCTION LEVEL 2 ############################### '''


    ''' ------ Function Main to executive ------ '''
    '''
        Trong level có hàm gì xử lý viết vào đây để chạy main chính
    '''
    def _state_curr_level_3(self):
        pass
    
    ''' ########################### EVENT ############################### '''
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

        '''
            Check reached goal:
                if True: 
                    Stop count time and score
                else: 
                    Continue count time and score
        '''
        # Draw time and score
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"TIME: {self.time_elapsed}", True, (255, 255, 255))
        score_text = font.render(f"SCORE: {self.score}", True, (255, 255, 255))

        # Position the text on the screen
        self.screen.blit(time_text, (10, 10))
        self.screen.blit(score_text, (10, 50))

        # Display "YOU WIN" in the center of the screen
        if self.reached_goal:
            # Set font and display "YOU WIN"
            font = pygame.font.Font(None, 72)
            font.set_bold(True)
            win_text = font.render("YOU WIN !!!", True, (255, 0, 0))
            text_rect = win_text.get_rect()
            text_rect.center = (self.WIDTH // 2, 40)  # Center the text
            self.screen.blit(win_text, text_rect)

if __name__ == '__main__':
    ai = AI_Search_PacMan_Level_3()
    ai.run_game()