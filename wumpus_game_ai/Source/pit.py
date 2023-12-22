from settings import *

class Pit:
    def __init__(self, x, y):
        # Khởi tạo các thuộc tính cho Pit
        self.is_discovered = None  # Biểu thị xem Pit đã được khám phá hay chưa
        self.size = 10  # Kích thước của môi trường (10x10)
        
        # Khởi tạo mảng 2 chiều để theo dõi thông báo và vị trí của các Pit
        self.noti = [[False for i in range(self.size)] for j in range(self.size)]
        self.pit_pos = [[False for i in range(self.size)] for j in range(self.size)]
        
        # Đặt các Pit vào vị trí đã chỉ định
        for i in range(len(x)):
            self.pit_pos[x[i]][y[i]] = True

    def pit_discovered(self):
        """Đánh dấu Pit đã được khám phá."""
        self.is_discovered = True

    def pit_notification(self):
        """Cập nhật thông báo cho các ô xung quanh Pit."""
        for i in range(self.size):
            for j in range(self.size):
                if self.pit_pos[i][j]:
                    # Cập nhật thông báo cho các ô lân cận của Pit
                    if i > 0:
                        self.noti[i - 1][j] = True
                    if i < self.size - 1:
                        self.noti[i + 1][j] = True
                    if j > 0:
                        self.noti[i][j - 1] = True
                    if j < self.size - 1:
                        self.noti[i][j + 1] = True

    def update(self, screen, font, is_discovered):
        """Cập nhật giao diện người dùng với thông báo về Pit."""
        for i in range(self.size):
            for j in range(self.size):
                # Nếu có thông báo từ Pit và ô đó đã được khám phá
                if self.noti[i][j] and is_discovered[i][j]:
                    # Hiển thị thông báo "Breeze" tại vị trí của Pit
                    text = font.render('Breeze', True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (42 + j * 70, 40 + i * 70)
                    screen.blit(text, textRect)
                    # pygame.display.update()
