from settings import *

class Wumpus:
    def __init__(self, x, y):
        # Tải hình ảnh và chỉnh kích thước cho Wumpus
        self.image = pygame.image.load(IMAGE_WUMPUS).convert()
        self.image = pygame.transform.scale(self.image, (300, 300))
        
        # Khởi tạo các thuộc tính cho Wumpus
        self.size = 10  # Kích thước của môi trường (10x10)
        self.is_discovered = None  # Biểu thị xem Wumpus đã được khám phá hay chưa
        
        # Khởi tạo mảng 2 chiều để theo dõi thông báo và vị trí của Wumpus
        self.noti = [[False for i in range(self.size)] for j in range(self.size)]
        self.wumpus_pos = [[False for i in range(self.size)] for j in range(self.size)]
        
        # Đặt Wumpus vào vị trí đã chỉ định bởi danh sách `x` và `y`
        for i in range(len(x)):
            self.wumpus_pos[x[i]][y[i]] = True

    def wumpus_kill(self, screen, font):
        """Hiển thị thông báo khi Wumpus bị giết."""
        text = font.render('Wumpus is killed !!!', True, BLACK)
        textRect = text.get_rect()
        textRect.center = (900, 180)
        screen.blit(text, textRect)
        screen.blit(self.image, (805, 250))
        pygame.display.update()

    def wumpus_notification(self):
        """Cập nhật thông báo cho các ô xung quanh Wumpus."""
        for i in range(self.size):
            for j in range(self.size):
                if self.wumpus_pos[i][j]:
                    # Cập nhật thông báo cho các ô lân cận của Wumpus
                    if i > 0:
                        self.noti[i - 1][j] = True
                    if i < self.size - 1:
                        self.noti[i + 1][j] = True
                    if j > 0:
                        self.noti[i][j - 1] = True
                    if j < self.size - 1:   
                        self.noti[i][j + 1] = True

    def wumpus_killed(self, i, j):
        """Cập nhật trạng thái khi Wumpus bị giết."""
        self.wumpus_pos[i][j] = False
        # Đặt lại thông báo cho các ô lân cận
        if i > 0:
            self.noti[i-1][j] = False
        if i < self.size - 1:
            self.noti[i+1][j] = False
        if j > 0:
            self.noti[i][j - 1] = False
        if j < self.size - 1:
            self.noti[i][j + 1] = False

    def update(self, screen, font, is_discovered):
        """Cập nhật giao diện người dùng với thông báo về Wumpus."""
        for i in range(self.size):
            for j in range (self.size):
                if self.noti[i][j] and is_discovered[i][j]:
                    # Hiển thị thông báo "Stench" tại vị trí của Wumpus
                    text = font.render('Stench', True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (45 + j * 70, 30 + i * 70)
                    screen.blit(text, textRect)
                    # pygame.display.update()

    def stench_i_j(self, i, j):
        """Kiểm tra xem ô tại vị trí (i, j) có mùi Stench hay không."""
        return self.noti[i][j]