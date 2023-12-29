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
        # Để đơn giản hóa, chúng ta chỉ kiểm tra xem có một mệnh đề trong KB mà không hợp lệ hay không

        extended_kb = copy.deepcopy(self.KB)
        
        for clause in extended_kb:
            if self.is_unsatisfiable(clause, not_alpha):
                return True
        return False

    def is_unsatisfiable(self, clause1, clause2):
        """Kiểm tra xem hai mệnh đề có không thể đồng thời đúng hay không."""
        # Đơn giản là so sánh từng phần tử trong hai mệnh đề
        for literal in clause1:
            if -literal in clause2:  # -literal là phủ định của literal
                return True
        return False
