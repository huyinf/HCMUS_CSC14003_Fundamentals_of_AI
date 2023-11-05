import pygame
from pygame.sprite import Sprite
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


BLOCK_SIZE = 25
WIDTH, HEIGHT = 800, 450

# Create pacman
class Pacman(Sprite):
    def __init__(self, ai_game, pacmanx, pacmany,cell=None):
        super().__init__()

        self.screen = ai_game.screen
        self.world = ai_game.world
        self.counter = 0
        self.direction = 0
        
        player_1_path = os.path.join(current_dir,'assets/player_images/1.png')
        self.pacman_images = pygame.transform.scale(pygame.image.load(player_1_path), (25, 25))
        
        self.rect = self.pacman_images.get_rect()
        self.rect.x = pacmanx * BLOCK_SIZE
        self.rect.y = pacmany * BLOCK_SIZE

        # R, L, U, D
        self.turns_allowed = [False, False, False, False]
        #pacman's memory
        self.food_memory= []
        self.path_food_memory=[]

        #pacman's sight
        self.food_sight=[]
        self.monter_sight=[]

        self.cell=cell

    # Draw pacman in screen
    def draw(self):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        self.screen.blit(self.pacman_images, self.rect)

    def move_pacman(self, tup):
        map_width = len(self.world[0]) * BLOCK_SIZE
        map_height = len(self.world) * BLOCK_SIZE

        map_x = (WIDTH - map_width) // 2
        map_y = (HEIGHT - map_height) // 2

        self.rect.x = map_x + tup[1] * BLOCK_SIZE
        self.rect.y = map_y + tup[0] * BLOCK_SIZE

    #custom for lv3
    # def emty_memory(self):
    #     return len(self.food_memory)==0
    # def monter_in_sight(self):
    #     return len(self.monter_sight)!=0
    # def food_in_sight(self):
    #     return len(self.food_sight)!=0    
    
    # def food_spread(self,pacman_pos_old):
    #     for path_food in self.path_food_memory:
    #         path_food.append(pacman_pos_old)
    # def temp(self,matrix):
    #     temp=self.path_food_memory[-1][-1]
    #     for path_food in self.path_food_memory:
    #         path_food.pop(-1)
    #     return temp
    # def remove_path(self):
    #    return self.remove(self.path_food_memory)
    # def near_monster(self,food):
    #     for monster in self.monter_in_sight:
    #         if abs(monster.pos[0]-food.pos[0])+abs(monster[1]-food[1])<=2:
    #             return True
    #     return False
    # def eyes_sight(self,matrix,sight):
    #     #reset memory
    #     self.food_sight=[]
    #     self.monter_sight=[]
    #     for neighbor in matrix[self.cell]:
    #         self.recursive_eyessight(matrix,self.cell,neighbor,sight-1)
    #     monster_near_food=[]
    #     for food_sight in self.food_in_sight:
    #         if self.near_monster(food_sight):
    #             monster_near_food.append(food_sight)
    #     food_cell=[]
    #     for i in range(len(self.food_memory)):
    #         if self.near_monster(self.food_memory[i]):
    #             food_cell.append(i)
    #     if len(food_cell) != 0:
    #         for index in reversed(food_cell):
    #             self.food_memory.pop(index)
    #             self.path_food_memory.pop(index)
    #     for near_monster in monster_near_food:
    #         self.food_sight.remove(near_monster)

    #     #update memory
    #     for food_sight in self.food_in_sight:
    #         for index in range(len(self.food_memory)):
    #             if food_sight == self.food_memory[index]:
    #                 self.food_memory.remove(self.food_memory[index])
    #                 self.path_food_memory.remove(self.path_food_memory[index])
    #                 break
    #         self.food_memory.append(food_sight)
    #         self.path_food_memory.append([])

    # def recursive_eyessight(self,matrix,parentcell,cell,sight):
    #     if sight>=0:
    #         if cell.exist_food() and cell not in self.food_in_sight():
    #             self.food_in_sight.append(cell)

    #         if cell.exist_monster() and cell not in self.monter_in_sight():
    #             self.monter_in_sight.append(cell)

    #         for neighbor in matrix[cell]:
    #             if neighbor != parentcell:
    #                 self.recursive_eyessight(matrix, cell, neighbor, sight - 1)
