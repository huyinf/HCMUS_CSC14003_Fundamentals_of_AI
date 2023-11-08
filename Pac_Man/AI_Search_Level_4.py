import pygame
from Pacman import *
from Map34 import *
from Astar import *
from Ghost import *
from BFS import *
from Minimax_Alg import *
import copy

'''
    Thay đổi linh hoạt viết hàm hoạt động level 3 vào có đồ họa sẵn rồi
'''
class AI_Search_PacMan_Level_4():
    def __init__(self):
        pygame.init()

        # Initialize
        self.WIDTH, self.HEIGHT = 1000, 562
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
        self.path_level_4_minimax = None

        # Set up path BFS
        # self.path_level_2_BFS = None

        # Check index path in algorithm to pacman move to goal
        self.path_index = 0

        '''
            Set number to choose algorithm search:
            1: Astar Search (default)
            2: BFS Search
        '''
        self.index_alg = 1

        self.deep = 0

        self._check_read_map = False

        # Check ghost
        self._check_ghost = False
        self._check_pacman = False

        # Check lose
        self._check_lose = False

    ''' ######################### RUN GAME #########################- '''
    def run_game(self):
        self.fps = 8
        self.running = True
        self.path_index = 0  # Initialize the index to the first coordinate in the path

        # Start the timer
        start_time = pygame.time.get_ticks()
        
        # Load map at folder map/level{..}/map{}.txt
        self._read_map_level(4, 3)

        # Check event
        while self.running:
            # Check events
            self._check_events()
            # Check reached goal
            if not self.reached_goal:
                # Calculate the time elapsed
                current_time = pygame.time.get_ticks()
                self.time_elapsed = (current_time - start_time) // 1000 # Convert to seconds
                
                # Main Function level 4
                self._state_curr_level_4()
                
                # update screen
                self._update_screen()

            pygame.display.flip()
            self.timer.tick(self.fps)

    ''' ######################### READ MAP ############################### '''
    # Read map level at folder level-{number1}, map{number2}..
    def _read_map_level(self, number1, number2):
        # Read map
        self.map = Map(self)

        # Read map at folder level/level-{number1}/map{number2}.txt
        self.world = self.map.load_level(number1, number2)
        
        # Get position ghost
        self.ghost_pos = self.map._pos_ghost()
        
        # Create ghost
        self.ghost = Ghost(self, self.ghost_pos)

        # Get position food
        self.food_pos = self.map._pos_food()
        '''
            Kiem tra pac man da di an thuc an tai vi tri (x,y) chua:
                False: Chua an
                True: An roi
        '''
        self._check_pass_food = {} 
        for pos in self.food_pos:
            self._check_pass_food[pos] = False


        # Get position pacman
        self.pacman_pos = self.map._pos_pacman()
        # Create pacman
        self.pacman = Pacman(self, self.pacman_pos[0], self.pacman_pos[1])

    ''' ######################### FUNCTION LEVEL 4 ############################### '''

    # Using Minimax Search algorithm
    def _MiniMax_Search_alg(self):
        if not self._check_lose:
            # Copy map
            map = copy.deepcopy(self.world)

            # Kiem tra an het thuc an chua
            if self.food_pos:
                # Copy position food
                food_check = copy.deepcopy(self.food_pos)

                # Find best move pacman
                best_move_pacman = best_move(map, self.pacman.get_possition_pacman(), copy.deepcopy(self.ghost_pos),food_check)
                
                # Cap nhat lai ban do sau khi pac an thuc an
                if self.world[best_move_pacman[0]][best_move_pacman[1]] == 2:
                    self.score += 19
                    self.world[best_move_pacman[0]][best_move_pacman[1]] = 0
                    self.food_pos = [item for item in self.food_pos if item != (best_move_pacman[0],best_move_pacman[1])]
                else:
                    self.score -= 1
                
                # Di chuyen pacman
                self.pacman.move_pacman(best_move_pacman)

                # Check vi tri ban dau cua ghost
                if self._check_ghost == False:
                    for y, row in enumerate(self.world):
                        for x, block in enumerate(row):
                            if self.world[y][x] == 3:
                                self.world[y][x] = 0

                    self._check_ghost = True

                # Di chuyen ghost toi pacman
                self.ghost.move_ghosts_to_pacman(best_move_pacman)

                if best_move_pacman in self.ghost.pos_ghost:
                    self._check_lose = True
                    self.score -= 20
            else:
                self.reached_goal = True            

    ''' ------ Function Main to executive ------ '''
    '''
        Trong level có hàm gì xử lý viết vào đây để chạy main chính
    '''
    def _state_curr_level_4(self):
        self._MiniMax_Search_alg()
        
    
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

        # Draw time and score
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"TIME: {self.time_elapsed}", True, (255, 255, 255))
        score_text = font.render(f"SCORE: {self.score}", True, (255, 255, 255))

        # Position the text on the screen
        self.screen.blit(time_text, (10, 10))

        '''
            Check reached goal:
                if True: 
                    Stop count time and score
                else: 
                    Continue count time and score
        '''
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

        # Display "YOU LOSE in the center of the screen
        if self._check_lose:
            # Set font and display "YOU LOSE"
            font = pygame.font.Font(None, 72)
            font.set_bold(True)
            win_text = font.render("YOU LOSE !!!", True, (255, 0, 0))
            text_rect = win_text.get_rect()
            text_rect.center = (self.WIDTH // 2, 40)  # Center the text
            self.screen.blit(win_text, text_rect)

if __name__ == '__main__':
    ai = AI_Search_PacMan_Level_4()
    ai.run_game()