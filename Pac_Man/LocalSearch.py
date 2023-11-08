import math
import copy

# Hàm tính khoảng cách giữa hai điểm
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Local search
def local_search(map, pos_pacman, score, deep, upp_list, down_list, right_list, left_list, ghost_pos):
    # Kiểm tra tại vị trí (x,y) là thức ăn, hay ô trống
    if map[pos_pacman[0]][pos_pacman[1]] == 0:
        score -= 1
    elif map[pos_pacman[0]][pos_pacman[1]] == 2:
        score += 50
    elif map[pos_pacman[0]][pos_pacman[1]] == 3:
        score -= 999

    if deep == 3:
        return score
    
    directions = [(pos_pacman[0] - 1, pos_pacman[1]), (pos_pacman[0] + 1, pos_pacman[1]), 
                (pos_pacman[0], pos_pacman[1] - 1), (pos_pacman[0], pos_pacman[1] + 1)]
    
    for direction in directions:
        if map[direction[0]][direction[1]] != 1:
            new_score = local_search(copy.deepcopy(map), direction, copy.deepcopy(score), deep + 1, upp_list, down_list, right_list, left_list, ghost_pos)
            if direction == directions[0]:
                upp_list[deep] = new_score
            elif direction == directions[1]:
                down_list[deep] = new_score
            elif direction == directions[2]:
                left_list[deep] = new_score
            elif direction == directions[3]:
                right_list[deep] = new_score

    max_score = max(upp_list[deep], down_list[deep], left_list[deep], right_list[deep])
    return max_score

# Tìm đường đi tốt nhất trả về một tọa độ (x,y)
def find_best_move(map, pos_pacman, ghost_pos):
    directions = [(pos_pacman[0] - 1, pos_pacman[1]), (pos_pacman[0] + 1, pos_pacman[1]), 
                (pos_pacman[0], pos_pacman[1] - 1), (pos_pacman[0], pos_pacman[1] + 1)]
    
    scores = [-9999] * 4
    for i, direction in enumerate(directions):
        if map[direction[0]][direction[1]] != 1:
            upp_list = [-9999] * 3
            down_list = [-9999] * 3
            left_list = [-9999] * 3
            right_list = [-9999] * 3
            scores[i] = local_search(copy.deepcopy(map), direction, 0, 1, upp_list, down_list, right_list, left_list, ghost_pos)
    
    max_score = max(scores)
    best_moves = [directions[i] for i, score in enumerate(scores) if score == max_score]
    
    # Chọn một trong những nước đi tốt nhất dựa trên khoảng cách Euclidean đến tất cả các ghost
    best_distance = float('inf')  # Khởi tạo khoảng cách tối ưu ban đầu
    best_move = None

    for move in best_moves:
        distances_to_ghosts = [euclidean_distance(move, ghost_position) for ghost_position in ghost_pos]
        min_distance_to_ghost = min(distances_to_ghosts)
        if min_distance_to_ghost < best_distance:
            best_distance = min_distance_to_ghost
            best_move = move
    
    return best_move
