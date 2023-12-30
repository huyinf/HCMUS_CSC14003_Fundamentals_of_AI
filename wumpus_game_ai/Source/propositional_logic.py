from enum import Enum
import copy
import cell
import knowledgeBase
from settings import *

class Action(Enum):
    """ Hướng di chuyển của Agent"""
    TURN_LEFT = 1
    TURN_RIGHT = 2
    TURN_UP = 3
    TURN_DOWN = 4

    """ Đi thẳng """
    MOVE_FORWARD = 5

    """ Lấy vàng """
    GRAB_GOLD = 6

    """ Cảm nhận gió """
    PERCEIVE_BREEZE = 7
    
    """ Cảm nhận mùi hôi """
    PERCEIVE_STENCH = 8

    """ Bắn """
    SHOOT = 9

    """ Giết và không Wumpus """
    KILL_WUMPUS = 10
    KILL_NO_WUMPUS = 11

    """ Bị Wumpus ăn """
    BE_EATEN_BY_WUMPUS = 12

    """ Rơi vào hố """
    FALL_INTO_PIT = 13

    """ Giết tất cả Wumpus và lấy tất cả thức ăn """
    KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD = 14

    """ Leo ra khỏi hang """
    CLIMB_OUT_OF_THE_CAVE = 15

    """ Phát hiện hố """
    DECTECT_PIT = 16

    """ Phát hiện Wumpus"""
    DETECT_WUMPUS = 17

    """ Không phát hiện hố và wumpus """
    DETECT_NO_PIT = 18
    DETECT_NO_WUMPUS = 19

    """ Suy luận có hố và wumpus ||  không có hố và wumpus """
    INFER_PIT = 20
    INFER_NOT_PIT = 21
    INFER_WUMPUS = 22
    INFER_NOT_WUMPUS = 23

    """ Phát hiện an toàn """
    DETECT_SAFE = 24

    """ Suy luận an toàn """
    INFER_SAFE = 25


class AgentBrain:
    def __init__(self, map_filename, output_filename):
        self.output_filename = output_filename

        self.map_size = None
        self.cell_matrix = None
        self.init_cell_matrix = None

        self.cave_cell = cell.Cell((-1, -1), 10, cell.Object.EMPTY.value)
        self.agent_cell = None
        self.init_agent_cell = None
        self.KB = knowledgeBase.KnowledgeBase()
        self.path = []
        self.action_list = []
        self.len_path = 0
        self.score = 0
        
        ''' Đếm số gold và wumpus ban đầu có trong map '''
        self.count_G_init = 0  
        self.count_W_init = 0

        ''' Dùng để kiểm tra xem đã ăn hết gold và giết hết wumpus chưa'''
        self.count_W = 0
        self.count_G = 0
        self.read_map(map_filename)

    def read_map(self, map_filename):
        file = open(map_filename, 'r')

        self.map_size = int(file.readline())
        raw_map = [line.split('.') for line in file.read().splitlines()]

        self.cell_matrix = [[None for _ in range(self.map_size)] for _ in range(self.map_size)]
        for ir in range(self.map_size):
            for ic in range(self.map_size):
                # Count Wumpus and Gold
                if raw_map[ir][ic] == 'W':
                    self.count_W += 1   
                if 'G' in raw_map[ir][ic]:
                    self.count_G += 1
                
                # Create cell
                self.cell_matrix[ir][ic] = cell.Cell((ir, ic), self.map_size, raw_map[ir][ic])
                if cell.Object.AGENT.value in raw_map[ir][ic]:
                    self.agent_cell = self.cell_matrix[ir][ic]
                    self.agent_cell.update_parent(self.cave_cell)
                    self.init_agent_cell = copy.deepcopy(self.agent_cell)
        file.close()
        self.count_G_init = self.count_G
        self.count_W_init = self.count_W   
        
        self.init_cell_matrix = copy.deepcopy(self.cell_matrix)
    #     result, pos = self.is_valid_map()
    #     if not result:
    #         if pos is None:
    #             raise TypeError('Input Error: The map is invalid! There is no Agent!')
    #         raise TypeError('Input Error: The map is invalid! Please check at row ' + str(pos[0]) + ' and column ' + str(pos[1]) + '.')


    # def is_valid_map(self):
    #     for cell_row in self.cell_matrix:
    #         for cell in cell_row:
    #             adj_cell_list = cell.get_adj_cell_list(self.cell_matrix)
    #             if cell.exist_pit():
    #                 for adj_cell in adj_cell_list:
    #                     if not adj_cell.exist_breeze():
    #                         return False, cell.matrix_pos
    #             if cell.exist_wumpus():
    #                 for adj_cell in adj_cell_list:
    #                     if not adj_cell.exist_stench():
    #                         return False, cell.matrix_pos
    #     if self.agent_cell is None:
    #         return False, None
    #     return True, None


    def append_event_to_output_file(self, text: str):
        if self.output_filename == OUTPUT_LIST1:
            out_file = open(self.output_filename, 'a')
            out_file.write(text + '\n')
            out_file.close()


    def add_action(self, action):
        self.action_list.append(action)
        # print(action)
        # self.append_event_to_output_file(action.name)

        if action == Action.TURN_LEFT:
            pass
        elif action == Action.TURN_RIGHT:
            pass
        elif action == Action.TURN_UP:
            pass
        elif action == Action.TURN_DOWN:
            pass
        elif action == Action.MOVE_FORWARD:
            self.score -= 10
            # print('Score: ' + str(self.score))
            # self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.GRAB_GOLD:
            self.score += 100
            # print('Score: ' + str(self.score))
            # self.append_event_to_output_file('Score: ' + str(self.score))
            self.count_G -= 1
        elif action == Action.PERCEIVE_BREEZE:
            pass
        elif action == Action.PERCEIVE_STENCH:
            pass
        elif action == Action.SHOOT:
            self.score -= 100
            # print('Score: ' + str(self.score))
            # self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.KILL_WUMPUS:
            self.count_W -= 1
            pass
        elif action == Action.KILL_NO_WUMPUS:
            pass
        elif action == Action.BE_EATEN_BY_WUMPUS:
            self.score -= 10000
            # print('Score: ' + str(self.score))
            # self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.FALL_INTO_PIT:
            self.score -= 10000
            # print('Score: ' + str(self.score))
            # self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD:
            pass
        elif action == Action.CLIMB_OUT_OF_THE_CAVE:
            self.score += 10
            # print('Score: ' + str(self.score))
            # self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.DECTECT_PIT:
            pass
        elif action == Action.DETECT_WUMPUS:
            pass
        elif action == Action.DETECT_NO_PIT:
            pass
        elif action == Action.DETECT_NO_WUMPUS:
            pass
        elif action == Action.INFER_PIT:
            pass
        elif action == Action.INFER_NOT_PIT:
            pass
        elif action == Action.INFER_WUMPUS:
            pass
        elif action == Action.INFER_NOT_WUMPUS:
            pass
        elif action == Action.DETECT_SAFE:
            pass
        elif action == Action.INFER_SAFE:
            pass
        else:
            raise TypeError("Error: " + self.add_action.__name__)
        
    def add_new_percepts_to_KB(self, cell1):
        adj_cell_list = cell1.get_adj_cell_list(self.cell_matrix)

        # Note: Pit and Wumpus can not appear at the same cell.
        # Hence: * If a cell has Pit, then it can not have Wumpus.
        #        * If a cell has Wumpus, then it can not have Pit.

        # PL: Pit?
        # sign = '-'
        # # if cell1.exist_pit():
        # #     sign = '+'
        # #     self.KB.add_clause([cell1.get_literal(cell.Object.WUMPUS, '-')])
        # # self.KB.add_clause([cell1.get_literal(cell.Object.PIT, sign)])
        # sign_pit = sign

        # # PL: Wumpus?
        # sign = '-'
        # if cell1.exist_wumpus():
        #     sign = '+'
        #     self.KB.add_clause([cell1.get_literal(cell.Object.PIT, '-')])
        # self.KB.add_clause([cell1.get_literal(cell.Object.WUMPUS, sign)])
        # sign_wumpus = sign

        # Check the above constraint.
        # if sign_pit == sign_wumpus == '+':
        #     raise TypeError('Logic Error: Pit and Wumpus can not appear at the same cell.')

        # PL: Breeze?
        sign = '-'
        if cell1.exist_breeze():
            sign = '+'
        self.KB.add_clause([cell1.get_literal(cell.Object.BREEZE, sign)])

        # PL: Stench?
        sign = '-'
        if cell1.exist_stench():
            sign = '+'
        self.KB.add_clause([cell1.get_literal(cell.Object.STENCH, sign)])

        # PL: This cell has Breeze iff At least one of all of adjacent cells has a Pit.
        # B <=> Pa v Pb v Pc v Pd
        if cell1.exist_breeze():
            # B => Pa v Pb v Pc v Pd
            clause = [cell1.get_literal(cell.Object.BREEZE, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(cell.Object.PIT, '+'))
            self.KB.add_clause(clause)

            # Pa v Pb v Pc v Pd => B
            # for adj_cell in adj_cell_list:
            #     clause = [cell1.get_literal(cell.Object.BREEZE, '+'),
            #             adj_cell.get_literal(cell.Object.PIT, '-')]
            #     self.KB.add_clause(clause)

        # PL: This cell has no Breeze then all of adjacent cells has no Pit.
        # -Pa ^ -Pb ^ -Pc ^ -Pd
        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(cell.Object.PIT, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has Stench iff At least one of all of adjacent cells has a Wumpus.
        if cell1.exist_stench():
            # S => Wa v Wb v Wc v Wd
            clause = [cell1.get_literal(cell.Object.STENCH, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(cell.Object.WUMPUS, '+'))
            self.KB.add_clause(clause)

            # # Wa v Wb v Wc v Wd => S
            # for adj_cell in adj_cell_list:
            #     clause = [cell1.get_literal(cell.Object.STENCH, '+'),
            #             adj_cell.get_literal(cell.Object.WUMPUS, '-')]
            #     self.KB.add_clause(clause)

        # PL: This cell has no Stench then all of adjacent cells has no Wumpus.
        # -Wa ^ -Wb ^ -Wc ^ -Wd
        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(cell.Object.WUMPUS, '-')]
                self.KB.add_clause(clause)

        # print(self.KB.KB)
        # self.append_event_to_output_file(str(self.KB.KB))

    def turn_to(self, next_cell):
        if next_cell.map_pos[0] == self.agent_cell.map_pos[0]:
            if next_cell.map_pos[1] - self.agent_cell.map_pos[1] == 1:
                self.add_action(Action.TURN_UP)
            else:
                self.add_action(Action.TURN_DOWN)
        elif next_cell.map_pos[1] == self.agent_cell.map_pos[1]:
            if next_cell.map_pos[0] - self.agent_cell.map_pos[0] == 1:
                self.add_action(Action.TURN_RIGHT)
            else:
                self.add_action(Action.TURN_LEFT)
        else:
            raise TypeError('Error: ' + self.turn_to.__name__)


    def move_to(self, next_cell):
        self.turn_to(next_cell)
        self.add_action(Action.MOVE_FORWARD)
        self.agent_cell = next_cell


    def backtracking_search(self):
        # Check agent grab all of gold and kill all of wumpus.
        if self.count_G == 0 and self.count_W == 0:
            self.add_action(Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD)
            return 
        
        # If there is a Pit, Agent dies.
        if self.agent_cell.exist_pit():
            self.add_action(Action.FALL_INTO_PIT)
            return False

        # If there is a Wumpus, Agent dies.
        if self.agent_cell.exist_wumpus():
            self.add_action(Action.BE_EATEN_BY_WUMPUS)
            return False

        # If there is Gold, Agent grabs Gold.
        if self.agent_cell.exist_gold():
            self.add_action(Action.GRAB_GOLD)
            self.agent_cell.grab_gold()

        # If there is Breeze, Agent perceives Breeze.
        if self.agent_cell.exist_breeze():
            self.add_action(Action.PERCEIVE_BREEZE)

        # If there is Stench, Agent perceives Stench.
        if self.agent_cell.exist_stench():
            self.add_action(Action.PERCEIVE_STENCH)

        # If this cell is not explored, mark this cell as explored then add new percepts to the KB.
        if not self.agent_cell.is_explored():
            self.agent_cell.explore()
            self.add_new_percepts_to_KB(self.agent_cell)

        # Initialize valid_adj_cell_list.
        valid_adj_cell_list = self.agent_cell.get_adj_cell_list(self.cell_matrix)

        # Discard the parent_cell from the valid_adj_cell_list.
        temp_adj_cell_list = []
        if self.agent_cell.parent in valid_adj_cell_list:
            valid_adj_cell_list.remove(self.agent_cell.parent)

        # Store previos agent's cell.
        pre_agent_cell = self.agent_cell

        # If the current cell is OK (there is no Breeze or Stench), Agent move to all of valid adjacent cells.
        # If the current cell has Breeze or/and Stench, Agent infers base on the KB to make a decision.
        if not self.agent_cell.is_OK():
            # Discard all of explored cells having Pit from the valid_adj_cell_list.
            temp_adj_cell_list = []
            for valid_adj_cell in valid_adj_cell_list:
                if valid_adj_cell.is_explored() and valid_adj_cell.exist_pit():
                    temp_adj_cell_list.append(valid_adj_cell)
            for adj_cell in temp_adj_cell_list:
                valid_adj_cell_list.remove(adj_cell)

            temp_adj_cell_list = []

            # If the current cell has Stench, Agent infers whether the valid adjacent cells have Wumpus.
            if self.agent_cell.exist_stench():
                valid_adj_cell: cell.Cell
                for valid_adj_cell in valid_adj_cell_list:
                    # print("Infer: ", end='')
                    # print(valid_adj_cell.map_pos)
                    # self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))
                    self.turn_to(valid_adj_cell)

                    # Infer Wumpus.
                    self.add_action(Action.INFER_WUMPUS)
                    not_alpha = [[valid_adj_cell.get_literal(cell.Object.WUMPUS, '-')]]
                    have_wumpus = self.KB.infer(not_alpha)

                    # If we can infer Wumpus.
                    if have_wumpus:
                        # Dectect Wumpus.
                        self.add_action(Action.DETECT_WUMPUS)

                        # Shoot this Wumpus.
                        self.add_action(Action.SHOOT)
                        self.add_action(Action.KILL_WUMPUS)
                        valid_adj_cell.kill_wumpus(self.cell_matrix, self.KB)
                        # self.append_event_to_output_file('KB: ' + str(self.KB.KB))

                    # If we can not infer Wumpus.
                    else:
                        # Infer not Wumpus.
                        self.add_action(Action.INFER_NOT_WUMPUS)
                        not_alpha = [[valid_adj_cell.get_literal(cell.Object.WUMPUS, '+')]]
                        have_no_wumpus = self.KB.infer(not_alpha)

                        # If we can infer not Wumpus.
                        if have_no_wumpus:
                            # Detect no Wumpus.
                            self.add_action(Action.DETECT_NO_WUMPUS)

                        # If we can not infer not Wumpus.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            if valid_adj_cell not in temp_adj_cell_list:
                                temp_adj_cell_list.append(valid_adj_cell)

            if self.agent_cell.exist_breeze():
                valid_adj_cell: cell.Cell
                for valid_adj_cell in valid_adj_cell_list:
                    # print("Infer: ", end='')
                    # print(valid_adj_cell.map_pos)
                    # self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))
                    self.turn_to(valid_adj_cell)

                    # Infer Pit.
                    self.add_action(Action.INFER_PIT)
                    not_alpha = [[valid_adj_cell.get_literal(cell.Object.PIT, '-')]]
                    have_pit = self.KB.infer(not_alpha)

                    # If we can infer Pit.
                    if have_pit:
                        # Detect Pit.
                        self.add_action(Action.DECTECT_PIT)

                        # Mark these cells as explored.
                        valid_adj_cell.explore()

                        # Add new percepts of these cells to the KB.
                        self.add_new_percepts_to_KB(valid_adj_cell)

                        # Update parent for this cell.
                        valid_adj_cell.update_parent(valid_adj_cell)

                        # Discard these cells from the valid_adj_cell_list.
                        temp_adj_cell_list.append(valid_adj_cell)

                    # If we can not infer Pit.
                    else:
                        # Infer not Pit.
                        self.add_action(Action.INFER_NOT_PIT)
                        not_alpha = [[valid_adj_cell.get_literal(cell.Object.PIT, '+')]]
                        have_no_pit = self.KB.infer(not_alpha)

                        # If we can infer not Pit.
                        if have_no_pit:
                            # Detect no Pit.
                            self.add_action(Action.DETECT_NO_PIT)

                        # If we can not infer not Pit.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            temp_adj_cell_list.append(valid_adj_cell)

            # If this cell still has Stench after trying to infer,
            # the Agent will try to shoot all of valid directions till Stench disappear.
            if self.agent_cell.exist_stench():
                adj_cell_list = self.agent_cell.get_adj_cell_list(self.cell_matrix)
                if self.agent_cell.parent in adj_cell_list:
                    adj_cell_list.remove(self.agent_cell.parent)

                explored_cell_list = []
                for adj_cell in adj_cell_list:
                    if adj_cell.is_explored():
                        explored_cell_list.append(adj_cell)
                for explored_cell in explored_cell_list:
                    adj_cell_list.remove(explored_cell)

                for adj_cell in adj_cell_list:
                    # print("Try: ", end='')
                    # print(adj_cell.map_pos)
                    # self.append_event_to_output_file('Try: ' + str(adj_cell.map_pos))
                    self.turn_to(adj_cell)

                    self.add_action(Action.SHOOT)
                    if adj_cell.exist_wumpus():
                        self.add_action(Action.KILL_WUMPUS)
                        adj_cell.kill_wumpus(self.cell_matrix, self.KB)
                        # self.append_event_to_output_file('KB: ' + str(self.KB.KB))

                    if not self.agent_cell.exist_stench():
                        self.agent_cell.update_child_list([adj_cell])
                        break

            # If the current cell has Breeze, Agent infers whether the adjacent cells have Pit.

        temp_adj_cell_list = list(set(temp_adj_cell_list))

        # Select all of the valid nexts cell from the current cell.
        for adj_cell in temp_adj_cell_list:
            valid_adj_cell_list.remove(adj_cell)
        self.agent_cell.update_child_list(valid_adj_cell_list)
        

        # Move to all of the valid next cells sequentially.
        for next_cell in self.agent_cell.child_list:
            self.move_to(next_cell)
            # print("Move to: ", end='')
            # print(self.agent_cell.map_pos)
            self.append_event_to_output_file('Move to: ' + str(self.agent_cell.map_pos))

            if not self.backtracking_search():
                return False

            self.move_to(pre_agent_cell)
            # print("Backtrack: ", end='')
            # print(pre_agent_cell.map_pos)
            self.append_event_to_output_file('Backtrack: ' + str(pre_agent_cell.map_pos))

        return True

    def solve_wumpus_world(self):
        # Reset file output
        out_file = open(self.output_filename, 'w')
        out_file.close()

        self.append_event_to_output_file('start: (1, 1)')
        self.backtracking_search()

        if self.agent_cell.parent == self.cave_cell:
            self.add_action(Action.CLIMB_OUT_OF_THE_CAVE)
    
        for action in self.action_list:
            if action == Action.MOVE_FORWARD:
                self.len_path += 1
        
        print('Length path propositional logic: ',self.len_path)
        self.append_event_to_output_file('SCORE: ' + str(self.score))
        self.append_event_to_output_file('Length path propositional logic: ' + str(self.len_path))
        
        return self.action_list, self.init_agent_cell, self.init_cell_matrix, self.count_G_init, self.count_W_init
