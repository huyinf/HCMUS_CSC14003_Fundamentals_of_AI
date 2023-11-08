import pygame
import os
from main import *
from AI_Search_Level_1 import *
from AI_Search_Level_2 import *
from AI_Search_Level_3 import *
from AI_Search_Level_4 import *
from setting import *

# Set algorithm for level 1, 2
'''
    1. BFS:  best first search implemnetation
    2. BFS2: breadth-first search implementation
    3.ASTAR (Default)
    4. UCS
'''

class Interface_Graphic:
    def __init__(self):
        # Init Game
        pygame.init()

        self._setting = Setting()
        
        # Set level map
        self._level_map = self._setting.level_map # Default = 1

        # Set up Screen
        self.screen_width, self.screen_height = 1000, 562
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac - man AI Search")

        # Load image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image = pygame.image.load(os.path.join(current_dir,"images/bg.jpg"))
        self.bg_width, self.bg_height = self.background_image.get_size()

        self.scale_factor = min(self.screen_width / self.bg_width, self.screen_height / self.bg_height)
        self.new_width = int(self.bg_width * self.scale_factor)
        self.new_height = int(self.bg_height * self.scale_factor)

        self.background_image = pygame.transform.scale(self.background_image, (self.new_width, self.new_height))

        # Define font
        self.font = pygame.font.Font(None, 50)

        # Set button color
        self.button_color = (255, 255, 255)
        self.change_button_color = (0, 255, 0)
        self.RED = (255, 0 ,0)
        self.YELLOW = (255, 255, 0)

        # Create button 'start'
        self.start_button = self.font.render("START GAME", True, self.button_color)
        self.start_button_rect = self.start_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

        # Create button "CHOOSE MAP"
        self.map_button = self.font.render("CHOOSE MAP", True, self.button_color)
        self.map_button_rect = self.map_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))

        # Create button "QUIT"
        self.quit_button = self.font.render("QUIT", True, self.button_color)
        self.quit_button_rect = self.quit_button.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 150))

        # Create BACK button
        self.back_button = self.font.render("BACK", True, self.button_color)
        self.back_button_rect = self.back_button.get_rect(center=(self.screen_width // 2 - 300, self.screen_height // 2 + 225))

        # Create button Level
        self.level1_buttons = self.font.render("LEVEL 1", True, self.button_color)
        self.level2_buttons = self.font.render("LEVEL 2", True, self.button_color)
        self.level3_buttons = self.font.render("LEVEL 3", True, self.button_color)
        self.level4_buttons = self.font.render("LEVEL 4", True, self.button_color)

        self.level1_buttons_rects = self.level1_buttons.get_rect(center=(self.screen_width // 2 -300, self.screen_height // 2 - 150))
        self.level2_buttons_rects = self.level2_buttons.get_rect(center=(self.screen_width // 2 -300, self.screen_height // 2 - 75))
        self.level3_buttons_rects = self.level3_buttons.get_rect(center=(self.screen_width // 2 -300, self.screen_height // 2 ))
        self.level4_buttons_rects = self.level4_buttons.get_rect(center=(self.screen_width // 2 -300, self.screen_height // 2 + 75))
        
        # Create button map
        self.map1_buttons = self.font.render("MAP 1", True, self.button_color)
        self.map2_buttons = self.font.render("MAP 2", True, self.button_color)
        self.map3_buttons = self.font.render("MAP 3", True, self.button_color)
        self.map4_buttons = self.font.render("MAP 4", True, self.button_color)
        self.map5_buttons = self.font.render("MAP 5", True, self.button_color)

        self.map1_buttons_rects = self.map1_buttons.get_rect(center=(self.screen_width // 2 - 300, self.screen_height // 2 - 200))
        self.map2_buttons_rects = self.map2_buttons.get_rect(center=(self.screen_width // 2 - 300, self.screen_height // 2 - 125))
        self.map3_buttons_rects = self.map3_buttons.get_rect(center=(self.screen_width // 2 - 300, self.screen_height // 2 - 50))
        self.map4_buttons_rects = self.map4_buttons.get_rect(center=(self.screen_width // 2 - 300, self.screen_height // 2 + 25))
        self.map5_buttons_rects = self.map5_buttons.get_rect(center=(self.screen_width // 2 - 300, self.screen_height // 2 + 100))
        
        # Create button Algorithm
        self.BFS_buttons = self.font.render("BFS (Best-First Search)", True, self.YELLOW)
        self.BFS2_buttons = self.font.render("BFS (Breadth-First Search)", True, self.YELLOW)
        self.ASTAR_buttons = self.font.render("ASTAR", True, self.YELLOW)
        self.DFS_buttons = self.font.render("DFS", True, self.YELLOW)

        self.BFS_buttons_rects = self.BFS_buttons.get_rect(left=self.screen_width // 2 + 10, top = self.screen_height // 2 - 175)
        self.DFS_buttons_rects = self.DFS_buttons.get_rect(left=self.screen_width // 2  + 10, top = self.screen_height // 2 - 100)
        self.ASTAR_buttons_rects = self.ASTAR_buttons.get_rect(left=self.screen_width // 2  + 10, top = self.screen_height // 2 -25)
        self.BFS2_buttons_rects = self.BFS2_buttons.get_rect(left=self.screen_width // 2  + 10, top =self.screen_height // 2 + 50)
        
        # State current screen
        self.current_screen = "start"  # Màn hình "Start" ban đầu

        # Save image background
        self.original_background = self.background_image.copy()

        # Check button level press
        '''
            1. Press Level 1
            2. Press Level 2
            3. Press Level 3
            4. Press Level 4

        '''
        self._check_button_press = 0
        self._pacman_bg = pygame.image.load(os.path.join(current_dir,"images/bg1.jpg"))
        self._pacman_bg =  pygame.transform.scale(self._pacman_bg, (self.new_width//2, self.new_height//2))
        self._pacman_bg_rect = self._pacman_bg.get_rect(center=(self.bg_width//2, self.bg_height//2 - 150))
        
        self.check_show_pacman_bg = True
    '''
        RUN GAME MAIN
    '''
    def run_game(self):
        running = True
        while running:
            # Draw background on the screen         
            if self.check_show_pacman_bg:         
                self.screen.blit(self._pacman_bg, self._pacman_bg_rect)
            else:
                self.screen.fill((0, 0, 0))

            # Check event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check mouse in button rect to change color buton rect
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos

                    # Check mouse in 'start' button to change color
                    if self.start_button_rect.collidepoint(mouse_x, mouse_y):
                        self.start_button = self.font.render("START GAME", True, self.change_button_color)
                    else:
                        self.start_button = self.font.render("START GAME", True, self.button_color)
                    
                    # Check mouse in 'quit' button to change color
                    if self.quit_button_rect.collidepoint(mouse_x, mouse_y):
                        self.quit_button = self.font.render("QUIT", True, self.change_button_color)
                    else:
                        self.quit_button = self.font.render("QUIT", True, self.button_color)

                    # Check mouse in 'quit' button to change color
                    if self.back_button_rect.collidepoint(mouse_x, mouse_y):
                        self.back_button = self.font.render("BACK", True, self.change_button_color)
                    else:
                        self.back_button = self.font.render("BACK", True, self.button_color)

                    # Check mouse in 'map' button to change color
                    if self.map_button_rect.collidepoint(mouse_x, mouse_y):
                        self.map_button = self.font.render("CHOOSE MAP", True, self.change_button_color)
                    else:
                        self.map_button = self.font.render("CHOOSE MAP", True, self.button_color)

                    # Check mouse in 'level1' button to change color
                    if self.level1_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.level1_buttons = self.font.render("LEVEL 1", True, self.change_button_color)
                    else:
                        self.level1_buttons = self.font.render("LEVEL 1", True, self.button_color)

                    # Check mouse in 'level2' button to change color
                    if self.level2_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.level2_buttons = self.font.render("LEVEL 2", True, self.change_button_color)
                    else:
                        self.level2_buttons = self.font.render("LEVEL 2", True, self.button_color)

                    # Check mouse in 'level3' button to change color
                    if self.level3_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.level3_buttons = self.font.render("LEVEL 3", True, self.change_button_color)
                    else:
                        self.level3_buttons = self.font.render("LEVEL 3", True, self.button_color)

                    # Check mouse in 'level4' button to change color
                    if self.level4_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.level4_buttons = self.font.render("LEVEL 4", True, self.change_button_color)
                    else:
                        self.level4_buttons = self.font.render("LEVEL 4", True, self.button_color)

                    # Check mouse in map
                    if self.map1_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.map1_buttons = self.font.render("MAP 1", True, self.change_button_color)
                    else:
                        self.map1_buttons = self.font.render("MAP 1", True, self.button_color)

                    if self.map2_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.map2_buttons = self.font.render("MAP 2", True, self.change_button_color)
                    else:
                        self.map2_buttons = self.font.render("MAP 2", True, self.button_color)

                    if self.map3_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.map3_buttons = self.font.render("MAP 3", True, self.change_button_color)
                    else:
                        self.map3_buttons = self.font.render("MAP 3", True, self.button_color)

                    if self.map4_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.map4_buttons = self.font.render("MAP 4", True, self.change_button_color)
                    else:
                        self.map4_buttons = self.font.render("MAP 4", True, self.button_color)
                    
                    if self.map5_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.map5_buttons = self.font.render("MAP 5", True, self.change_button_color)
                    else:
                        self.map5_buttons = self.font.render("MAP 5", True, self.button_color)

                    # Check mouse in Algorithm
                    if self.BFS_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.BFS_buttons = self.font.render("BFS (Best-First Search)", True, self.change_button_color)
                    else:
                        self.BFS_buttons = self.font.render("BFS (Best-First Search)", True, self.YELLOW)

                    if self.DFS_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.DFS_buttons = self.font.render("DFS", True, self.change_button_color)
                    else:
                        self.DFS_buttons = self.font.render("DFS", True, self.YELLOW)

                    if self.ASTAR_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.ASTAR_buttons = self.font.render("ASTAR", True, self.change_button_color)
                    else:
                        self.ASTAR_buttons = self.font.render("ASTAR", True, self.YELLOW)

                    if self.BFS2_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.BFS2_buttons = self.font.render("BFS(Breadth-First Search)", True, self.change_button_color)
                    else:
                        self.BFS2_buttons = self.font.render("BFS(Breadth-First Search)", True, self.YELLOW)
                

                # Check mouse button down and check press left mouse
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check current screen "start"
                    if self.start_button_rect.collidepoint(event.pos):
                        self.current_screen = "level_select"
                        self.check_show_pacman_bg = False
                    elif self.quit_button_rect.collidepoint(event.pos):
                        running = False
                    elif self.map_button_rect.collidepoint(event.pos):
                        self.current_screen = "choose_map"
                        self.check_show_pacman_bg = False

                    # Check current screen "level_select" in "start"
                    # Search Level 1 Pacman
                    elif self.level1_buttons_rects.collidepoint(event.pos):
                        self.current_screen = "show_algorithm"
                        self._setting.level_map = 1
                        self._check_button_press = 1
                
                    # Search Level 2 Pacman
                    elif self.level2_buttons_rects.collidepoint(event.pos):
                        self.current_screen = "show_algorithm"
                        self._setting.level_map = 2
                        self._check_button_press = 2
                    
                    # Search level 3 Pacman
                    elif self.level3_buttons_rects.collidepoint(event.pos):
                        self.current_screen = "level_select"
                        self._setting.level_map = 3
                        self._check_button_press = 3
                        # self._choose_level_map_rungame()

                    # Search level 4 Pacman
                    elif self.level4_buttons_rects.collidepoint(event.pos):
                        self.current_screen = "level_select"
                        self._setting.level_map = 4
                        # self.current_screen = "level_select"
                        self._check_button_press = 4
                        self._choose_level_map_rungame()

                    # Check Algorithm using for level 1, 2
                    elif self.BFS_buttons_rects.collidepoint(event.pos):
                        self._setting.choose_algorithm = 1
                        self._choose_level_map_rungame()
                    elif self.BFS2_buttons_rects.collidepoint(event.pos):
                        self._setting.choose_algorithm = 2
                        self._choose_level_map_rungame()
                    elif self.ASTAR_buttons_rects.collidepoint(event.pos):
                        self._setting.choose_algorithm = 3
                        self._choose_level_map_rungame()
                    elif self.DFS_buttons_rects.collidepoint(event.pos):
                        self._setting.choose_algorithm = 4
                        self._choose_level_map_rungame()

                    # Return main interface, BACK
                    elif self.back_button_rect.collidepoint(event.pos):
                        self.current_screen = "start"

                    # Check mouse button map txt
                    if self.current_screen == "choose_map":

                        if self.map1_buttons_rects.collidepoint(event.pos):
                            print('a')

                        elif self.map2_buttons_rects.collidepoint(event.pos):
                            print('a')

                        elif self.map3_buttons_rects.collidepoint(event.pos):
                            print('a')

                        elif self.map4_buttons_rects.collidepoint(event.pos):
                            print('a')

                        elif self.map5_buttons_rects.collidepoint(event.pos):
                            print('a')

                    print(self.current_screen)
            # Draw change color button if press 
            self._check_button_level_press()

            
            
            ''' ==================================================== '''

            # Check condition state screen
            if self.current_screen == "start":
                # Draw button "START GAME" and button "QUIT" when state screen = "Start"
                self.screen.blit(self.quit_button, self.quit_button_rect)
                self.screen.blit(self.start_button,self.start_button_rect)
                self.screen.blit(self.map_button,self.map_button_rect)

            elif self.current_screen == "level_select":
                # Draw button level on the screen
                self.screen.blit(self.level1_buttons, self.level1_buttons_rects)
                self.screen.blit(self.level2_buttons, self.level2_buttons_rects)
                self.screen.blit(self.level3_buttons, self.level3_buttons_rects)
                self.screen.blit(self.level4_buttons, self.level4_buttons_rects)

                # Draw back button
                self.screen.blit(self.back_button, self.back_button_rect)
            
            # Show algorithm
            elif self.current_screen == "show_algorithm":
                # Draw button level on the screen
                self.screen.blit(self.level1_buttons, self.level1_buttons_rects)
                self.screen.blit(self.level2_buttons, self.level2_buttons_rects)
                self.screen.blit(self.level3_buttons, self.level3_buttons_rects)
                self.screen.blit(self.level4_buttons, self.level4_buttons_rects)
                
                # Draw back button
                self.screen.blit(self.back_button, self.back_button_rect)

                # Draw button level on the screen
                self.screen.blit(self.BFS_buttons, self.BFS_buttons_rects)
                self.screen.blit(self.BFS2_buttons, self.BFS2_buttons_rects)
                self.screen.blit(self.ASTAR_buttons, self.ASTAR_buttons_rects)
                self.screen.blit(self.DFS_buttons, self.DFS_buttons_rects)
                
            # Check current screen "choose_map"
            elif self.current_screen == "choose_map":
                # Delete button "START GAME" and button "QUIT" 
                # self.screen.blit(self.original_background, (0, 0))
                self.screen.blit(self.map1_buttons, self.map1_buttons_rects)
                self.screen.blit(self.map2_buttons, self.map2_buttons_rects)
                self.screen.blit(self.map3_buttons, self.map3_buttons_rects)
                self.screen.blit(self.map4_buttons, self.map4_buttons_rects)
                self.screen.blit(self.map5_buttons, self.map5_buttons_rects)
                
                # Draw back button
                self.screen.blit(self.back_button, self.back_button_rect)
            

            pygame.display.update()
            
    ''' ==================================================== '''
    
    # Chọn level map để chạy
    def _choose_level_map_rungame(self):
        if self._setting.level_map == 1:
            self.ai_search_pacman = AI_Search_PacMan_Level_1()
            self.ai_search_pacman.run_game()
        elif self._setting.level_map == 2:
            self.ai_search_pacman = AI_Search_PacMan_Level_2()
            self.ai_search_pacman.run_game()
        elif self._setting.level_map == 3:
            self.ai_search_pacman = AI_Search_PacMan_Level_3()
            self.ai_search_pacman.run_game()
        elif self._setting.level_map == 4:
            self.ai_search_pacman = AI_Search_PacMan_Level_4()
            self.ai_search_pacman.run_game()
        
    ''' ==================================================== '''
    # Check button press level 
    def _check_button_level_press(self):
        if self._check_button_press == 1:
            # Check mouse in 'level1' button to change color
            self.level1_buttons = self.font.render("LEVEL 1", True, self.RED)
        elif self._check_button_press == 2:
            # Check mouse in 'level1' button to change color
            self.level2_buttons = self.font.render("LEVEL 2", True, self.RED)
        elif self._check_button_press == 3:
            # Check mouse in 'level1' button to change color
            self.level3_buttons = self.font.render("LEVEL 3", True, self.RED)
        elif self._check_button_press == 4:
            # Check mouse in 'level1' button to change color
            self.level4_buttons = self.font.render("LEVEL 4", True, self.RED)

                    

if __name__ == '__main__':
    interface_graphic = Interface_Graphic()
    interface_graphic.run_game()