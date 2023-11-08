import random
import math
import copy

# Vị trí ban đầu của Pac-Man và quái vật
pacman_position = (1, 1)
ghost_position = (2, 2)

# Hàm tính khoang cách giữa hai điểm
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Local search
def local_search(map, pos_pacman, score, deep, upp_list, down_list, right_list, left_list):
    # Kiem tra tai vi tri (x,y) la thuc an, hay o trong
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
            new_score = local_search(copy.deepcopy(map), direction, copy.deepcopy(score), deep + 1, upp_list, down_list, right_list, left_list)
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

# Tim duong di tot nhat tra ve mot toa do (x,y)
def find_best_move(map, pos_pacman):
    directions = [(pos_pacman[0] - 1, pos_pacman[1]), (pos_pacman[0] + 1, pos_pacman[1]), 
                (pos_pacman[0], pos_pacman[1] - 1), (pos_pacman[0], pos_pacman[1] + 1)]
    
    scores = [-9999] * 4
    for i, direction in enumerate(directions):
        if map[direction[0]][direction[1]] != 1:
            upp_list = [-9999] * 3
            down_list = [-9999] * 3
            left_list = [-9999] * 3
            right_list = [-9999] * 3
            scores[i] = local_search(copy.deepcopy(map), direction, 0, 1, upp_list, down_list, right_list, left_list)
    
    max_score = max(scores)
    best_moves = [directions[i] for i, score in enumerate(scores) if score == max_score]
    
    return random.choice(best_moves)

# Example usage
map = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 2, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

best_move = find_best_move(map, pacman_position)
print("Best move:", best_move)
