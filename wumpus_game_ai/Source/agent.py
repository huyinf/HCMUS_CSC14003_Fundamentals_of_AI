import pygame
from stack_data import *
from settings import *

class Agent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.img_list = []
        self.i = x - 1 # Tọa độ hàng
        self.j = y - 1 # Tọa độ cột
        self.spacing = 70

        self.load_images()
        self.set_initial_position(x, y)

    """Load images for agent"""
    def load_images(self):
        self.agent_right = pygame.image.load(IMAGE_AGENT_RIGHT).convert()
        self.agent_left = pygame.transform.flip(self.agent_right, True, False)
        self.agent_up = pygame.transform.rotate(self.agent_right, -90)
        self.agent_down = pygame.transform.flip(self.agent_up, False, True)
        self.img_list = [self.agent_right, self.agent_left, self.agent_up, self.agent_down]

    """Đặt vị trí ban đầu """
    def set_initial_position(self, x, y):
        """
            Vị trí ban đầu của agent là ở ô (1, 1)
            Tọa độ của ô (1, 1) là (40, 40) (Tính trung tâm của ô)
            Mỗi ô có kích thước là 70x70
            => Tọa độ của agent là (40 + (y-1)*70, 40 + (x-1)*70)
        """
        self.x = 40 + (y-1) * 70
        self.y = 40 + (x-1) * 70
        self.rect = self.agent_right.get_rect()
        self.rect.center = (self.x, self.y)

    def save_image_to_lst(self):
        self.img_list.append(self.agent_right)
        self.img_list.append(self.agent_left)
        self.img_list.append(self.agent_up)
        self.img_list.append(self.agent_down)

    """ Hiển thị hình ảnh của agent """
    # def appear(self, screen):
    #     screen.blit(self.agent_right, (self.x - 30, self.y - 30))

    """ Lấy điểm của agent """
    def get_score(self):
        return self.score

    """ Di chuyển agent """
    def move_forward(self, direct):
        if direct == 0:
            self.move_up()
        elif direct == 1:
            self.move_down()
        elif direct == 2:
            self.move_left()
        elif direct == 3:
            self.move_right()

    def move_up(self):
        self.y -= self.spacing
        self.score -= 10
        if self.i > 0:
            self.i -= 1

    def move_down(self):
        self.y += self.spacing
        self.score -= 10
        if self.i < 9:
            self.i += 1

    def move_left(self):
        self.x -= self.spacing
        self.score -= 10
        if self.j > 0:
            self.j -= 1

    def move_right(self):
        self.x += self.spacing
        self.score -= 10
        if self.j < 9:
            self.j += 1

    """ Hướng của agent """
    def turn_up(self):
        self.image = self.img_list[3]
        return 0

    def turn_down(self):
        self.image = self.img_list[2]
        return 1

    def turn_left(self):
        self.image = self.img_list[1]
        return 2

    def turn_right(self):
        self.image = self.img_list[0]
        return 3

    """ Cập nhật vị trí của agent """
    def update(self):
        if self.x > 670:
            self.x -= self.spacing
            self.score += 10

        elif self.x < 40:
            self.x += self.spacing
            self.score += 10

        elif self.y < 40:
            self.y += self.spacing
            self.score += 10

        elif self.y > 670:
            self.y -= self.spacing
            self.score += 10

        self.rect.center = (self.x, self.y)

    """ Lấy vị trí của agent """
    def get_pos(self):
        return self.i, self.j

    """ Bắn mũi tên """
    def shoot(self):
        self.score -= 100

    """ Kiểm tra va chạm với wumpus hoặc pit """
    def wumpus_or_pit_collision(self):
        self.score -= 10000

    """ Lấy vàng và cập nhật điểm"""
    def grab_gold(self):
        self.score += 100

    """ Lên cầu thang và cập nhật điểm """
    def climb(self):
        self.score += 10

