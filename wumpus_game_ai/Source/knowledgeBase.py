# Import thư viện Glucose3 từ pysat.solvers và thư viện copy của Python
from pysat.solvers import Glucose3
import copy

class KnowledgeBase:
    def __init__(self):
        """Khởi tạo KnowledgeBase với một bảng kiến thức trống (KB)."""
        self.KB = []

    @staticmethod
    def standardize_clause(clause):
        """ Chuẩn hóa một mệnh đề bằng cách sắp xếp và loại bỏ trùng lặp."""
        return sorted(list(set(clause)))

    def add_clause(self, clause):
        """Thêm một mệnh đề vào KB, trước tiên Chuẩn hóa mệnh đề và kiểm tra sự tồn tại."""
        clause = self.standardize_clause(clause)
        if clause not in self.KB:
            self.KB.append(clause)

    def del_clause(self, clause):
        """Xóa một mệnh đề khỏi KB, sau tiêu chuẩn hóa và kiểm tra sự tồn tại."""
        clause = self.standardize_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)

    def infer(self, not_alpha):
        """Kiểm tra tính suy luận: nếu KB và not_alpha đồng thời không hợp lệ thì trả về True, ngược lại trả về False."""
        # Tạo một bộ giải quyết bài toán SAT từ Glucose3
        g = Glucose3()
        
        # Sao chép danh sách mệnh đề từ KB để không ảnh hưởng đến KB gốc
        clause_list = copy.deepcopy(self.KB)
        
        # Thêm mệnh đề phủ định của alpha (not_alpha) vào bộ giải quyết
        negative_alpha = not_alpha
        for it in clause_list:
            g.add_clause(it)
        for it in negative_alpha:
            g.add_clause(it)
        
        # Giải bài toán SAT và kiểm tra nếu có lời giải
        sol = g.solve()
        if sol:
            return False
        return True
