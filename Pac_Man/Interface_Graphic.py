import pygame
from main import *
from AI_Search_Level_1 import *
from AI_Search_Level_2 import *

class Interface_Graphic:
    def __init__(self):
        # Init Game
        pygame.init()

        # Set up Screen
        self.screen_width, self.screen_height = 800, 450
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac - man AI Search")

        # Load image
        self.background_image = pygame.image.load("images/bg2.jpg")
        self.bg_width, self.bg_height = self.background_image.get_size()

        self.scale_factor = min(self.screen_width / self.bg_width, self.screen_height / self.bg_height)
        self.new_width = int(self.bg_width * self.scale_factor)
        self.new_height = int(self.bg_height * self.scale_factor)

        self.background_image = pygame.transform.scale(self.background_image, (self.new_width, self.new_height))

        # Define font
        self.font = pygame.font.Font(None, 50)

        # Set button color
        self.button_color = (0, 0, 0)
        self.change_button_color = (0, 255, 0)

        # Create button 'start'
        self.start_button = self.font.render("Start game", True, self.button_color)
        self.start_button_rect = self.start_button.get_rect(center=(self.screen_width // 2 - 200, self.screen_height // 2 - 25))

        # Create button "Quit"
        self.quit_button = self.font.render("Quit", True, self.button_color)
        self.quit_button_rect = self.quit_button.get_rect(center=(self.screen_width // 2 - 200, self.screen_height // 2 + 25))

        # Create button Level
        self.level1_buttons = self.font.render("Level 1", True, self.button_color)
        self.level2_buttons = self.font.render("Level 2", True, self.button_color)
        self.level3_buttons = self.font.render("Level 3", True, self.button_color)
        self.level4_buttons = self.font.render("Level 4", True, self.button_color)

        self.level1_buttons_rects = self.level1_buttons.get_rect(center=(self.screen_width // 2 -200, self.screen_height // 2 - 100))
        self.level2_buttons_rects = self.level2_buttons.get_rect(center=(self.screen_width // 2 -200, self.screen_height // 2 - 50))
        self.level3_buttons_rects = self.level3_buttons.get_rect(center=(self.screen_width // 2 -200, self.screen_height // 2))
        self.level4_buttons_rects = self.level4_buttons.get_rect(center=(self.screen_width // 2 -200, self.screen_height // 2 + 50))

        # State current screen
        self.current_screen = "start"  # Màn hình "Start" ban đầu

        # Save image bạcground
        self.original_background = self.background_image.copy()
        

        '''
            RUN GAME MAIN
        '''
    def run_game(self):
        running = True
        while running:
            # Check event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check mouse in button rect to change color buton rect
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos

                    # Check mouse in 'start' button to change color
                    if self.start_button_rect.collidepoint(mouse_x, mouse_y):
                        self.start_button = self.font.render("Start game", True, self.change_button_color)
                    else:
                        self.start_button = self.font.render("Start game", True, self.button_color)
                    
                    # Check mouse in 'quit' button to change color
                    if self.quit_button_rect.collidepoint(mouse_x, mouse_y):
                        self.quit_button = self.font.render("Quit", True, self.change_button_color)
                    else:
                        self.quit_button = self.font.render("Quit", True, self.button_color)

                    # Check mouse in 'level1' button to change color
                    if self.level1_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.level1_buttons = self.font.render("Level 1", True, self.change_button_color)
                    else:
                        self.level1_buttons = self.font.render("Level 1", True, self.button_color)

                    # Check mouse in 'level2' button to change color
                    if self.level2_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.level2_buttons = self.font.render("Level 2", True, self.change_button_color)
                    else:
                        self.level2_buttons = self.font.render("Level 2", True, self.button_color)

                    # Check mouse in 'level3' button to change color
                    if self.level3_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.level3_buttons = self.font.render("Level 3", True, self.change_button_color)
                    else:
                        self.level3_buttons = self.font.render("Level 3", True, self.button_color)

                    # Check mouse in 'level4' button to change color
                    if self.level4_buttons_rects.collidepoint(mouse_x, mouse_y):
                        self.level4_buttons = self.font.render("Level 4", True, self.change_button_color)
                    else:
                        self.level4_buttons = self.font.render("Level 4", True, self.button_color)

                # Check mouse button down and check press left mouse
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check current screen "start"
                    if self.current_screen == "start":
                        if self.start_button_rect.collidepoint(event.pos):
                            self.current_screen = "level_select"
                        elif self.quit_button_rect.collidepoint(event.pos):
                            running = False

                    # Check current screen "level_select" in "start"
                    elif self.current_screen == "level_select":
                        # Search Level 1 Pacman
                        if self.level1_buttons_rects.collidepoint(event.pos):
                                self.ai_search_pacman1 = AI_Search_PacMan_Level_1()
                                self.ai_search_pacman1.run_game()
                        # Search Level 2 Pacman
                        if self.level2_buttons_rects.collidepoint(event.pos):
                                self.ai_search_pacman2 = AI_Search_PacMan_Level_2()
                                self.ai_search_pacman2.run_game()
                
            # Draw background on the screen                    
            self.screen.blit(self.background_image, (0, 0))
            
            # Check condition state screen
            if self.current_screen == "start":
                # Draw button "Start game" and button "Quit" when state screen = "Start"
                self.screen.blit(self.quit_button, self.quit_button_rect)
                self.screen.blit(self.start_button,self.start_button_rect)
            elif self.current_screen == "level_select":
                # Delete button "Start game" and button "Quit" 
                self.screen.blit(self.original_background, (0, 0))

                # Draw button level on the screen
                self.screen.blit(self.level1_buttons, self.level1_buttons_rects)
                self.screen.blit(self.level2_buttons, self.level2_buttons_rects)
                self.screen.blit(self.level3_buttons, self.level3_buttons_rects)
                self.screen.blit(self.level4_buttons, self.level4_buttons_rects)

            pygame.display.flip()

        # Kết thúc Pygame
        pygame.quit()

if __name__ == '__main__':
    interface_graphic = Interface_Graphic()
    interface_graphic.run_game()