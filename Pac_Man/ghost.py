import pygame
from pygame.sprite import Sprite
from Astar import *
import random
import copy

BLOCK_SIZE = 25
WIDTH, HEIGHT = 1000, 562

class Ghost(Sprite):
    def __init__(self, ai_game, tup_pos_ghost):
        super().__init__()

        self.screen = ai_game.screen
        self.world = ai_game.world
        self.pos_ghost = tup_pos_ghost
        # them tuple chua vi tri moi cua ghost
        self.new_pos_ghost = copy.deepcopy(tup_pos_ghost)
        self.image = pygame.transform.scale(pygame.image.load(f'images/ghost.png'), (25, 25))

        self.possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]


    # Draw ghost on the screen
    def draw_ghost(self):
        map_width = len(self.world[0]) * BLOCK_SIZE
        map_height = len(self.world) * BLOCK_SIZE

        map_x = (WIDTH - map_width) // 2
        map_y = (HEIGHT - map_height) // 2

        for pos in self.pos_ghost:
            self.screen.blit(self.image, (map_x + pos[1] * BLOCK_SIZE, map_y + pos[0] * BLOCK_SIZE))
    
    # Draw ghost on the screen
    def draw_ghost_level3(self):
        map_width = len(self.world[0]) * BLOCK_SIZE
        map_height = len(self.world) * BLOCK_SIZE

        map_x = (WIDTH - map_width) // 2
        map_y = (HEIGHT - map_height) // 2

        # print("in draw: ",self.new_pos_ghost)
        for pos in self.new_pos_ghost:
            self.screen.blit(self.image, (map_x + pos[1] * BLOCK_SIZE, map_y + pos[0] * BLOCK_SIZE))
    # 
    def move_ghosts_to_pacman(self, pacman_pos):
        for i in range(len(self.pos_ghost)):
            # Tìm đường đi từ vị trí hiện tại của con ma đến vị trí của pacman bằng A*
            path = Astar(self.world, self.pos_ghost[i], pacman_pos)

            if path:
                # Nếu có đường đi, thì di chuyển con ma tới vị trí tiếp theo trong đường đi
                next_pos = path[1] if len(path) > 1 else path[0]
                self.pos_ghost[i] = next_pos
    
    def _random_pos_ghost(self):

        # kiểm tra xem ghost có ra khỏi vùng ban đầu không
        '''
            input: vị trí khởi tạo (initial_pos), vị trí hiện tại (curr_pos)
            output: True (trong vùng) or False (ngoài vùng)
        '''
        def inBoundary(initial_pos,curr_pos):
            return abs(curr_pos[0]-initial_pos[0]) <= 1 and abs(curr_pos[1]-initial_pos[1]) <= 1
        
        for i in range(len(self.pos_ghost)):
            move = self.possible_moves[random.randint(0, 3)]
            run = True
            while run:
                # chọn bước đi tiếp theo dựa trên vị trí cũ, không phải vị trí khởi tạo
                new_x = self.new_pos_ghost[i][0] + move[0]
                new_y = self.new_pos_ghost[i][1] + move[1]
                newPos = (new_x,new_y)
                # Kiểm tra xem có nằm trong biên của thế giới không
                # print("in random")
                # print("init: ",self.pos_ghost[i])
                # print("new: ",newPos)
                if 0 <= new_x < len(self.world) and 0 <= new_y < len(self.world[0]) and inBoundary(self.pos_ghost[i],newPos) == True:
                    # Kiểm tra xem ô đó có là tường không
                    if self.world[new_x][new_y] != 1:
                        # cập nhật vị trí mới cho ghost
                        self.new_pos_ghost[i] = (new_x, new_y)
                        run = False
                move = self.possible_moves[random.randint(0, 3)]


