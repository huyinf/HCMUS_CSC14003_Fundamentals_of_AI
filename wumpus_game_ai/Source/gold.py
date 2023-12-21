# Import các cài đặt từ module settings
from settings import *

class Gold:
    def __init__(self):
        """ Load image """
        self.image = pygame.image.load(IMAGE_GOLD).convert()
        
        # Thay đổi kích thước của hình ảnh vàng để nó phù hợp với màn hình
        self.image = pygame.transform.scale(self.image, (300,300))
        
        # Đặt vị trí text vàng trên màn hình
        self.pos = (900, 100)

    def grab_gold(self, screen, font):
        """Hiển thị thông báo vàng đã được tìm thấy và cập nhật điểm số trên màn hình."""
        
        # Tạo và vị trí cho dòng thông báo "You found a gold!!!"
        text = font.render('Gold is founded !!!', True, BLACK)
        textRect = text.get_rect()
        textRect.center = self.pos
        
        # Vẽ dòng thông báo trên màn hình
        screen.blit(text, textRect)
        
        # Hiển thị hình ảnh vàng tại vị trí cố định trên màn hình
        screen.blit(self.image, (805, 200))
        
        # Tạo và vị trí cho dòng thông báo "Score + 100"
        text = font.render('Score + 100', True, BLACK)
        textRect.center = (900, 600)
        
        # Vẽ dòng thông báo về điểm số trên màn hình
        screen.blit(text, textRect)
        
        # Cập nhật màn hình để hiển thị các thay đổi mới
        pygame.display.update()
