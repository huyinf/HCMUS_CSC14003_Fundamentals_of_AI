from settings import *

class Arrow:
    def __init__(self):
        self.img_list = []

        self.load_images()

    """ Load và chuyển đổi hình ảnh cho mũi tên."""
    def load_images(self):
        self.arrow_right = pygame.image.load(IMAGE_ARROW_RIGHT).convert_alpha()
        self.arrow_left = pygame.transform.rotate(self.arrow_right, 180)
        self.arrow_up = pygame.transform.rotate(self.arrow_right, 90)
        self.arrow_down = pygame.transform.rotate(self.arrow_right, -90)
        self.img_list = [self.arrow_right, self.arrow_left, self.arrow_up, self.arrow_down]

    """ Hiển thị hình ảnh của mũi tên """
    def shoot(self, direct, screen, y, x):
        if direct == 0:
            self.shoot_up(screen, x, y)
        elif direct == 1:
            self.shoot_down(screen, x, y)
        elif direct == 2:
            self.shoot_left(screen, x, y)
        elif direct == 3:
            self.shoot_right(screen, x, y)

    """ Hiển thị hình ảnh của mũi tên khi bắn sang phải """
    def shoot_right(self, screen, x, y):
        x = 10 + (x + 1) * 70
        y = 10 + y * 70
        screen.blit(self.img_list[0], (x, y))
        pygame.display.update()

    """ Hiển thị hình ảnh của mũi tên khi bắn sang trái"""
    def shoot_left(self, screen, x, y):
        x = 10 + (x - 1) * 70
        y = 10 + y * 70
        screen.blit(self.img_list[1], (x, y))
        pygame.display.update()

    """ Hiển thị hình ảnh của mũi tên khi bắn lên """
    def shoot_up(self, screen, x, y):
        x = 10 + x * 70
        y = 10 + (y - 1) * 70
        screen.blit(self.img_list[2], (x, y))
        pygame.display.update()

    """ Hiển thị hình ảnh của mũi tên khi bắn xuống"""
    def shoot_down(self, screen, x, y):
        i = 10 + x * 70
        j = 10 + (y + 1) * 70
        screen.blit(self.img_list[3], (i, j))
        pygame.display.update()
