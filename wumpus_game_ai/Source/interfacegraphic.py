import pygame
from map import Map
from settings import *
import os
import sys
from agent import Agent
from arrow import Arrow
from gold import Gold
from pit import Pit
from wumpus import Wumpus
import propositional_logic as PropositionalLogic
import fol_logic as FirstOrderLogic
import time


class InterfaceGraphic:
    def __init__(self):
        """Khởi tạo giao diện và các thuộc tính của game."""
        self.initialize_interface()
        self.initialize_game_attributes()
        self.initialize_fonts()
        self.initialize_buttons()

    """ ---------------------------------------- """
    """ ---------------------------------------- """

    """ Khởi tạo giao diện Pygame"""
    def initialize_interface(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.bg = pygame.image.load('../Images/win.jpg').convert()
        # self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.bg = pygame.transform.scale(self.bg, (605, 507))


    """ Khởi tạo các thuộc tính của game"""
    def initialize_game_attributes(self):
        self.map = None
        self.agent = None
        self.gold = None
        self.wumpus = None
        self.pit = None
        self.arrow = None
        self.state = MAP
        self.map_i = 1
        
        self.output_file = OUTPUT_LIST1
        # print(OUTPUT_LIST1)

        ''' 
        Chọn thuật toán để chạy game 
        1. Proposional Logic
        2. First Order Logic
        '''
        self.choose_algorithm = 1

        '''
        0: up
        1: down
        2: left
        3: right
        '''
        self.direct = 3

    """Khởi tạo các font cho giao diện."""
    def initialize_fonts(self):
        """ Set fonts"""
        self.font = pygame.font.Font(FONTS, 30) 
        self.noti = pygame.font.Font(FONTS, 15)
        self.victory = pygame.font.Font(FONTS, 50)
    
    """Khởi tạo các nút bấm trên giao diện."""
    def initialize_buttons(self):
        # create button
        self.button_map1 = pygame.font.Font.render(self.font, "Map 1", True, BLACK)
        self.button_map2 = pygame.font.Font.render(self.font, "Map 2", True, BLACK)
        self.button_map3 = pygame.font.Font.render(self.font, "Map 3", True, BLACK)
        self.button_map4 = pygame.font.Font.render(self.font, "Map 4", True, BLACK)
        self.button_map5 = pygame.font.Font.render(self.font, "Map 5", True, BLACK)
        self.button_exit = pygame.font.Font.render(self.font, "Exit", True, BLACK)
        self.button_alg = pygame.font.Font.render(self.font, "Algorithm", True, BLACK)

        # get rect button
        self.button_alg_rect = self.button_alg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT //2 - 240))
        self.button_map1_rect = self.button_map1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT //2 - 160))
        self.button_map2_rect = self.button_map2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT //2 - 80))
        self.button_map3_rect = self.button_map3.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT //2))
        self.button_map4_rect = self.button_map4.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT //2 + 80))
        self.button_map5_rect = self.button_map5.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT //2 + 160))
        self.button_exit_rect = self.button_exit.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT //2 + 240))

    """ ---------------------------------------- """
    """ ---------------------------------------- """

    """ Hiển thị giao diện người dùng """
    def running_draw(self):
        self.screen.fill(WHITE)
        self.map.draw(self.screen)

        ''' Vẽ điểm số '''
        text = self.font.render('Your score: ', True, RED)
        textRect = text.get_rect()
        textRect.topleft = (750, 28)
        self.screen.blit(text, textRect)        

        score = self.agent.get_score()
        text = self.font.render(str(score), True, BLACK)
        textRect = text.get_rect()
        textRect.topleft = (1000, 28)
        self.screen.blit(text, textRect)   

        ''' Vẽ count gold và kill wumpus '''
        text = self.font.render('Count gold: ', True, BLUE)
        textRect = text.get_rect()
        textRect.topleft = (720, 70)
        self.screen.blit(text, textRect)

        text = self.font.render(str(self.count_G), True, BLACK)
        textRect = text.get_rect()
        textRect.topleft = (1020, 70)
        self.screen.blit(text, textRect)

        text = self.font.render('Count wumpus: ', True, BLUE)
        textRect = text.get_rect()
        textRect.topleft = (720, 110)
        self.screen.blit(text, textRect)

        text = self.font.render(str(self.count_W), True, BLACK)
        textRect = text.get_rect()
        textRect.topleft = (1020, 110)
        self.screen.blit(text, textRect)
    # run game
    def run_game(self):
        running = True
        while running:
            self.clock.tick(60)
            self.screen.fill(WHITE)

            if self.state == MAP:
                self.check_event()
            elif self.state == ALGORITHM:  
                # self.screen.fill(WHITE)
                text = self.font.render('Choose algorithm:', True, BLACK)
                textRect = text.get_rect()
                textRect.center = (600, 50)
                self.screen.blit(text, textRect)

                text1 = self.font.render('1. Proposional Logic', True, BLACK)
                textRect1 = text.get_rect()
                textRect1.center = (500, 300)

                text2 = self.font.render('2. First Order Logic', True, BLACK)
                textRect2 = text.get_rect()
                textRect2.center = (500, 400)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # check mouse in button and change blue color
                    if event.type == pygame.MOUSEMOTION:
                        if textRect1.collidepoint(event.pos):
                            text1 = pygame.font.Font.render(self.font, "1. Proposional Logic", True, BLUE)
                        else:
                            text1 = pygame.font.Font.render(self.font, "1. Proposional Logic", True, BLACK)

                        if textRect2.collidepoint(event.pos):
                            text2 = pygame.font.Font.render(self.font, "2. First Order Logic", True, BLUE)
                        else:
                            text2 = pygame.font.Font.render(self.font, "2. First Order Logic", True, BLACK)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if textRect1.collidepoint(event.pos):
                            self.choose_algorithm = 1
                            print(1)
                            self.state = MAP
                            self.output_file = OUTPUT_LIST1
                        if textRect2.collidepoint(event.pos):
                            self.choose_algorithm = 2
                            print(2)
                            self.state = MAP
                            self.output_file = OUTPUT_LIST2

                    self.screen.blit(text1, textRect1)
                    self.screen.blit(text2, textRect2)
                    pygame.display.flip()

            elif self.state == RUNNING:
                self.state = TRYBEST
                action_list, cave_cell, cell_matrix = None, None, None
                self.count_G = 0
                self.count_W = 0
                ''' Chọn thuật toán '''
                if self.choose_algorithm == 1:
                    start_time = time.time()
                    action_list, cave_cell, cell_matrix, self.count_G, self.count_W = PropositionalLogic.AgentBrain(MAP_LIST[self.map_i - 1], self.output_file[self.map_i - 1]).solve_wumpus_world()
                    # print(action_list)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print('Time: ', elapsed_time)
                    
                    # write time to output file
                    with open (self.output_file[self.map_i - 1], 'a') as f:
                        f.write('Time: ' + str(elapsed_time) + '\n')
                else:
                    os.chdir(os.path.dirname(os.path.abspath(__file__)))
                    inputFile = MAP_LIST[self.map_i - 1]
                    # print(inputFile)
                    outputFile = self.output_file[self.map_i - 1]
                    # action_list, cave_cell, cell_matrix, self.count_G, self.count_W = PropositionalLogic.AgentBrain(inputFile,outputFile).solve_wumpus_world()
                    cave_cell = PropositionalLogic.AgentBrain(inputFile,outputFile).get_cave_cell()
                    cell_matrix = PropositionalLogic.AgentBrain(inputFile,outputFile).get_cell_matrix()
                    
                    fol = FirstOrderLogic.FOL(inputFile, outputFile)
                    start_time = time.time()
                    fol.FOLmodel()

                    # action_list, cave_cell, cell_matrix = None, None, None
                    action_list = fol.results()[-1]
                    self.count_G = fol.results()[1]
                    self.count_W = fol.results()[2]

                    end_time = time.time()
                    
                    elapsed_time = end_time - start_time
                    print('Time: ', elapsed_time)
                    fol.write_ouput()
                    # write time to output file
                    with open (outputFile, 'a') as f:
                        f.write('Time: ' + str(elapsed_time) + '\n')
                    
                    # print(fol.results()[0])
                    # print(action_list)
                
                map_pos = cave_cell.map_pos

                # print("cave cell:", cave_cell.map_pos)
                # print("cell matrix:", cell_matrix)

                self.map = Map((len(cell_matrix) - map_pos[1] + 1, map_pos[0]))
                self.arrow = Arrow()
                self.gold = Gold()
                self.agent = Agent(len(cell_matrix) - map_pos[1] + 1, map_pos[0])
                self.agent.save_image_to_lst()
                self.all_sprites = pygame.sprite.Group()
                self.all_sprites.add(self.agent)

                x = []
                y = []
                for ir in range(len(cell_matrix)):
                    for ic in range(len(cell_matrix)):
                        if cell_matrix[ir][ic].exist_pit():
                            x.append(ir)
                            y.append(ic)
                self.pit = Pit(x, y)
                self.pit.pit_notification()

                x = []
                y = []
                for ir in range(len(cell_matrix)):
                    for ic in range(len(cell_matrix)):
                        if cell_matrix[ir][ic].exist_wumpus():
                            x.append(ir)
                            y.append(ic)
                self.wumpus = Wumpus(x, y)
                self.wumpus.wumpus_notification()

                self.running_draw()

                for action in action_list:
                    pygame.time.delay(SPEED)
                    self.display_action(action)
                    # print(action)

                    if action == PropositionalLogic.Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD or action == 'win':
                        self.state = WIN

                    if action == PropositionalLogic.Action.FALL_INTO_PIT or action == PropositionalLogic.Action.BE_EATEN_BY_WUMPUS or action == 'Wumpus' or action == 'Pit':
                        self.state = GAMEOVER
                        break

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
            elif self.state == WIN or self.state == TRYBEST:
                self.win_draw()
                self.win_event()

    # check event
    def check_event(self):
        # check su kien
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # check mouse in button and change blue color
            if event.type == pygame.MOUSEMOTION:
                if self.button_map1_rect.collidepoint(event.pos):
                    self.button_map1 = pygame.font.Font.render(self.font, "Map 1", True, BLUE)
                else:
                    self.button_map1 = pygame.font.Font.render(self.font, "Map 1", True, BLACK)
                if self.button_map2_rect.collidepoint(event.pos):
                    self.button_map2 = pygame.font.Font.render(self.font, "Map 2", True, BLUE)
                else:
                    self.button_map2 = pygame.font.Font.render(self.font, "Map 2", True, BLACK)
                if self.button_map3_rect.collidepoint(event.pos):
                    self.button_map3 = pygame.font.Font.render(self.font, "Map 3", True, BLUE)
                else:
                    self.button_map3 = pygame.font.Font.render(self.font, "Map 3", True, BLACK)
                if self.button_map4_rect.collidepoint(event.pos):
                    self.button_map4 = pygame.font.Font.render(self.font, "Map 4", True, BLUE)
                else:
                    self.button_map4 = pygame.font.Font.render(self.font, "Map 4", True, BLACK)
                if self.button_map5_rect.collidepoint(event.pos):
                    self.button_map5 = pygame.font.Font.render(self.font, "Map 5", True, BLUE)
                else:
                    self.button_map5 = pygame.font.Font.render(self.font, "Map 5", True, BLACK)
                if self.button_exit_rect.collidepoint(event.pos):
                    self.button_exit = pygame.font.Font.render(self.font, "Exit", True, BLUE)
                else:
                    self.button_exit = pygame.font.Font.render(self.font, "Exit", True, BLACK)
                if self.button_alg_rect.collidepoint(event.pos):
                    self.button_alg = pygame.font.Font.render(self.font, "Algorithm", True, BLUE)
                else:
                    self.button_alg = pygame.font.Font.render(self.font, "Algorithm", True, BLACK)
            # check click button 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_map1_rect.collidepoint(event.pos):
                    # print("Map 1")
                    self.state = RUNNING
                    self.map_i = 1
                if self.button_map2_rect.collidepoint(event.pos):
                    # print("Map 2")
                    self.state = RUNNING
                    self.map_i = 2
                if self.button_map3_rect.collidepoint(event.pos):
                    # print("Map 3")
                    self.state = RUNNING
                    self.map_i = 3
                if self.button_map4_rect.collidepoint(event.pos):
                    # print("Map 4")
                    self.state = RUNNING
                    self.map_i = 4
                if self.button_map5_rect.collidepoint(event.pos):
                    # print("Map 5")
                    self.state = RUNNING
                    self.map_i = 5
                if self.button_alg_rect.collidepoint(event.pos):
                    self.state = ALGORITHM
                if self.button_exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            # draw button
            self.draw_button()

            pygame.display.flip()
    # draw button
    def draw_button(self):
        self.screen.blit(self.button_map1, self.button_map1_rect)
        self.screen.blit(self.button_map2, self.button_map2_rect)
        self.screen.blit(self.button_map3, self.button_map3_rect)
        self.screen.blit(self.button_map4, self.button_map4_rect)
        self.screen.blit(self.button_map5, self.button_map5_rect)
        self.screen.blit(self.button_exit, self.button_exit_rect)
        self.screen.blit(self.button_alg, self.button_alg_rect)

    # draw win game
    def win_draw(self):
        # set background
        self.screen.fill(WHITE)
        self.screen.blit(self.bg, (300, 110))

        # check state == 'win'
        if self.state == WIN:
            text = self.victory.render('You win !!!', True, BLACK)
        elif self.state == TRYBEST:
            text = self.victory.render('Try more effort !!!', True, BLACK)
        
        textRect = text.get_rect()
        textRect.center = (600, 50)
        self.screen.blit(text, textRect)

        """ In ra điểm cao nhất """
        score = self.agent.get_score()
        text = self.victory.render('Max score: ' + str(score), True, BLACK)
        textRect.center = (550, 120)
        self.screen.blit(text, textRect)

    # draw win event
    def win_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        pygame.time.delay(1500)
        self.state = MAP

    # display action
    def display_action(self, action: PropositionalLogic.Action):
        
        """ Cập nhật lại màn hình"""
        def update_elements():
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            pygame.display.update()
            

        if action == PropositionalLogic.Action.TURN_LEFT or action == "L":
            self.direct = self.agent.turn_left()
            update_elements()
        elif action == PropositionalLogic.Action.TURN_RIGHT or action == "R":
            self.direct = self.agent.turn_right()
            update_elements()
        elif action == PropositionalLogic.Action.TURN_UP or action == "U":
            self.direct = self.agent.turn_up()
            update_elements()
        elif action == PropositionalLogic.Action.TURN_DOWN or action == "D":
            self.direct = self.agent.turn_down()
            update_elements()
        elif action == PropositionalLogic.Action.MOVE_FORWARD or action == "F":
            self.agent.move_forward(self.direct)
            i, j = self.agent.get_pos()
            self.map.discover_cell_i_j(i, j)
            update_elements()
        elif action == PropositionalLogic.Action.GRAB_GOLD or action == 'G':
            self.agent.grab_gold()
            update_elements()
            self.gold.grab_gold(self.screen, self.font)
            self.count_G -= 1
            pygame.time.delay(1500)
        elif action == PropositionalLogic.Action.PERCEIVE_BREEZE:
            pass
        elif action == PropositionalLogic.Action.PERCEIVE_STENCH:
            pass
        elif action == PropositionalLogic.Action.SHOOT or action == 'S':
            self.agent.shoot()
            update_elements()
            i, j = self.agent.get_pos()
            self.arrow.shoot(self.direct, self.screen, i, j)
        elif action == PropositionalLogic.Action.KILL_WUMPUS or action == 'K':
            i, j = self.agent.get_pos()
            if self.direct == 0:
                i -= 1
            elif self.direct == 1:
                i += 1
            elif self.direct == 2:
                j -= 1
            elif self.direct == 3:
                j += 1
                
            self.wumpus.wumpus_killed(i, j)
            self.wumpus.wumpus_notification()
            i, j = self.agent.get_pos()
            if not self.wumpus.stench_i_j(i, j):
                self.wumpus.wumpus_kill(self.screen, self.font)
            temp = self.map.discovered()

            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)

            self.count_W -= 1
            pygame.display.update()
            pygame.time.delay(1500)
        elif action == PropositionalLogic.Action.KILL_NO_WUMPUS:
            pass
        elif action == PropositionalLogic.Action.BE_EATEN_BY_WUMPUS or action == 'Wumpus':
            self.agent.wumpus_or_pit_collision()
            update_elements()
            self.state = GAMEOVER
        elif action == PropositionalLogic.Action.FALL_INTO_PIT or action == 'Pit':
            self.agent.wumpus_or_pit_collision()
            update_elements()
            self.state = GAMEOVER
        elif action == PropositionalLogic.Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD or action == 'win':
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            self.map.agent_grab_all_gold_and_kill_wumpus(self.screen, self.font)
            self.state = WIN
            pygame.display.update()
            pygame.time.delay(1500)
        elif action == PropositionalLogic.Action.DECTECT_PIT:
            i, j = self.agent.get_pos()
            if self.direct == 0:
                i -= 1
            elif self.direct == 1:
                i += 1
            elif self.direct == 2:
                j -= 1
            elif self.direct == 3:
                j += 1
            self.map.pit_detect(i, j)
            update_elements()
            pygame.time.delay(1500)
        elif action == PropositionalLogic.Action.CLIMB_OUT_OF_THE_CAVE or action == 'out':
            self.agent.climb()
            self.all_sprites.update()
            self.running_draw()
            self.all_sprites.draw(self.screen)
            self.map.agent_climb(self.screen, self.font)
            pygame.display.update()
            pygame.time.delay(1500)
        elif action == None:
            pass
        elif action == PropositionalLogic.Action.DETECT_WUMPUS:
            pass
        elif action == PropositionalLogic.Action.DETECT_NO_PIT:
            pass
        elif action == PropositionalLogic.Action.DETECT_NO_WUMPUS:
            pass
        elif action == PropositionalLogic.Action.INFER_PIT:
            pass
        elif action == PropositionalLogic.Action.INFER_NOT_PIT:
            pass
        elif action == PropositionalLogic.Action.INFER_WUMPUS:
            pass
        elif action == PropositionalLogic.Action.INFER_NOT_WUMPUS:
            pass
        elif action == PropositionalLogic.Action.DETECT_SAFE:
            pass
        elif action == PropositionalLogic.Action.INFER_SAFE:
            pass
        else:
            raise TypeError("Error: " + self.display_action.__name__)