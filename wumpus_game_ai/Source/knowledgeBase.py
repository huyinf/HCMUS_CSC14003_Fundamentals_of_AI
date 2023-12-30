import copy

# Kiểm tra xem hai literal có phải là các literal bù của nhau không
def is_complentary_literals(literal_1, literal_2):
    return (literal_1 + literal_2 == 0)

# Kiểm tra một clause có hợp lệ hay không (tức là không có hai literal bù của nhau trong cùng một clause)
def is_valid_clause(clause):
    for i in range(len(clause) - 1):
        if is_complentary_literals(clause[i], clause[i + 1]):
            return True
    return False

# Chuẩn hóa một clause: xóa bỏ các phần tử trùng lặp và sắp xếp clause
def standard_clause(clause):
    return sorted(list(set(copy.deepcopy(clause))))

# Sinh tất cả các tổ hợp từ các tập hợp trong set_list
def generate_combinations_recursively(set_list, combination_list, combination, depth):
    if depth == len(set_list):
        combination_list.append(copy.deepcopy(combination))
        return

    for element in set_list[depth]:
        combination.append(copy.deepcopy(element))
        generate_combinations_recursively(set_list, combination_list, combination, depth + 1)
        combination.pop()

# Sinh tất cả các tổ hợp từ các tập hợp trong set_list
def generate_combinations(set_list):
    combination_list, combination, depth = [], [], 0
    generate_combinations_recursively(set_list, combination_list, combination, 0)
    return combination_list

# Giải quyết hai clause bằng phương pháp Resolution
def resolve(clause_1, clause_2):
    resolvents = []
    for i in range(len(clause_1)):
        for j in range(len(clause_2)):
            if is_complentary_literals(clause_1[i], clause_2[j]):
                resolvent = clause_1[:i] + clause_1[i + 1:] + clause_2[:j] + clause_2[j + 1:]
                resolvents.append(standard_clause(resolvent))
    return resolvents

# Thuật toán PL Resolution
def pl_resolution(KB, neg_alpha):
    cnf_clause_list = copy.deepcopy(KB)
    for clause in neg_alpha:
        if clause not in cnf_clause_list:
            cnf_clause_list.append(clause)
    new_clauses_list = []
    solution = False
    while True:
        new_clauses_list.append([])

        for i in range(len(cnf_clause_list)):
            for j in range(i + 1, len(cnf_clause_list)):
                resolvents = resolve(cnf_clause_list[i], cnf_clause_list[j])
                if [] in resolvents:
                    solution = True
                    new_clauses_list[-1].append([])
                    return solution

                for resolvent in resolvents:
                    if is_valid_clause(resolvent):
                        break
                    if resolvent not in cnf_clause_list and resolvent not in new_clauses_list[-1]:
                        new_clauses_list[-1].append(resolvent)

        if len(new_clauses_list[-1]) == 0:
            solution = False
            return solution
        cnf_clause_list += new_clauses_list[-1]

# Lớp KnowledgeBase
class KnowledgeBase:
    def __init__(self):
        self.KB = []

    # Chuẩn hóa một clause và thêm vào KB nếu chưa tồn tại
    def standardize_clause(self, clause):
        return sorted(list(set(clause)))

    def add_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause not in self.KB:
            self.KB.append(clause)

    def del_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)

    # Dùng thuật toán PL Resolution để suy luận
    def infer(self, neg_alpha):
        clause_list = copy.deepcopy(self.KB)
        state = pl_resolution(clause_list, neg_alpha)
        return state

# # Dữ liệu kiểm thử
# KB = [[-1, 2], [1, -2], [1, 2]]
# alpha = [[-1]]
# kb = KnowledgeBase()
# kb.add_clause(KB[0])
# kb.add_clause(KB[1])
# kb.add_clause(KB[2])
# result = kb.infer(alpha)
# print(result)  # Kết quả in ra là True
