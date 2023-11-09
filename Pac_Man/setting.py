# setting.py
class Setting:
    def __init__(self):
        # Chon level cho map
        self.level_map = 1

        # Chon thuat toan cho level 1, 2
        '''
            1. BFS: best-first search
            2. BFS2: breath-first search
            3. Astar (Default)
            4. DFS
        '''
        self.choose_algorithm = 3

        # Chọn map: Co tat ca 5 map .txt
        self.choose_map_txt = 1
    
    # Cập nhật giá trị cho choose_map_txt
    def set_choose_map_txt(self, value):
        self.choose_map_txt = value
