from Astar import *
import math
import copy

def minimax_alg(map, pos_pacman, pos_ghost, score, deep,upp_list,down_list,right_list,left_list):
    
    check_pacman_near_ghost = False
    min_ghost = calculate_distance(pos_pacman,pos_ghost[0])
    for ghost in pos_ghost:
        if min_ghost > calculate_distance(pos_pacman,ghost):
            min_ghost = calculate_distance(pos_pacman,ghost)
    if min_ghost < 3:
        check_pacman_near_ghost = True
    else:
        check_pacman_near_ghost = False
    if check_pacman_near_ghost == True:
        #Pacman di toi cho ghost
        for ghost in pos_ghost:
            if pos_pacman == ghost:
                score = -999
                return score

        if map[pos_pacman[0]][pos_pacman[1]] == 0:
            score -= 1
        elif map[pos_pacman[0]][pos_pacman[1]] == 2:
            score += 20
            map[pos_pacman[0]][pos_pacman[1]] = 0
            check_food_hard = 0
            if map[pos_pacman[0] - 1][pos_pacman[1]] == 1:
                check_food_hard += 1
            if map[pos_pacman[0] + 1][pos_pacman[1]] == 1:
                check_food_hard += 1
            if map[pos_pacman[0]][pos_pacman[1] - 1] == 1:
                check_food_hard += 1
            if map[pos_pacman[0]][pos_pacman[1] + 1] == 1:
                check_food_hard += 1
            if check_food_hard == 3:
                score = -10
                return score
    
        # tao ghost di chuyen toi pacman
        pos_ghost_new = []
        for ghost in pos_ghost:
            path = Astar(map, ghost, pos_pacman)

            if path:
                # Nếu có đường đi, thì di chuyển con ma tới vị trí tiếp theo trong đường đi
                next_pos = path[1] if len(path) > 1 else path[0]
                pos_ghost_new.append(next_pos)
        
        '''
            Truong hop pacman di roi, toi ghost di toi cho pacman
        '''
        for ghost in pos_ghost_new:
            if ghost == pos_pacman:
                score = -999
                return score
    
        if deep == 10:
            return score
        if  map[pos_pacman[0] - 1][pos_pacman[1]] != 1: # kiem tra di len khac tuong
            upp_list[deep] = minimax_alg(copy.deepcopy(map), (pos_pacman[0] - 1, pos_pacman[1]), copy.deepcopy(pos_ghost_new), copy.deepcopy(score), deep + 1,upp_list,down_list,right_list,left_list)
        if  map[pos_pacman[0] + 1][pos_pacman[1]] != 1: # kiem tra di down khac tuong
            down_list[deep] = minimax_alg(copy.deepcopy(map), (pos_pacman[0] + 1, pos_pacman[1]), copy.deepcopy(pos_ghost_new), copy.deepcopy(score), deep + 1,upp_list,down_list,right_list,left_list)
        if  map[pos_pacman[0]][pos_pacman[1] - 1] != 1: # kiem tra di left khac tuong
            left_list[deep] = minimax_alg(copy.deepcopy(map), (pos_pacman[0], pos_pacman[1] - 1), copy.deepcopy(pos_ghost_new), copy.deepcopy(score), deep + 1,upp_list,down_list,right_list,left_list)
        if  map[pos_pacman[0]][pos_pacman[1] + 1]!= 1: # kiem tra di right khac tuong
            right_list[deep] = minimax_alg(copy.deepcopy(map), (pos_pacman[0], pos_pacman[1] + 1), copy.deepcopy(pos_ghost_new), copy.deepcopy(score), deep + 1,upp_list,down_list,right_list,left_list)


        max_score = max(upp_list[deep], down_list[deep], left_list[deep], right_list[deep])
        return max_score
    else:
        for ghost in pos_ghost:
            if pos_pacman == ghost:
                score = -999
                return score

        if map[pos_pacman[0]][pos_pacman[1]] == 0:
            score -= 1
        elif map[pos_pacman[0]][pos_pacman[1]] == 2:
            score += 20
            map[pos_pacman[0]][pos_pacman[1]] = 0
            check_food_hard = 0
            if map[pos_pacman[0] - 1][pos_pacman[1]] == 1:
                check_food_hard += 1
            if map[pos_pacman[0] + 1][pos_pacman[1]] == 1:
                check_food_hard += 1
            if map[pos_pacman[0]][pos_pacman[1] - 1] == 1:
                check_food_hard += 1
            if map[pos_pacman[0]][pos_pacman[1] + 1] == 1:
                check_food_hard += 1
            if check_food_hard == 3:
                score += 500
       
    
        # tao ghost di chuyen toi pacman
        pos_ghost_new = []
        for ghost in pos_ghost:
            path = Astar(map, ghost, pos_pacman)

            if path:
                # Nếu có đường đi, thì di chuyển con ma tới vị trí tiếp theo trong đường đi
                next_pos = path[1] if len(path) > 1 else path[0]
                pos_ghost_new.append(next_pos)
        
        '''
            Truong hop pacman di roi, toi ghost di toi cho pacman
        '''
        for ghost in pos_ghost_new:
            if ghost == pos_pacman:
                score = -999
                return score
    
        if deep == 10:
            return score
        if  map[pos_pacman[0] - 1][pos_pacman[1]] != 1: # kiem tra di len khac tuong
            upp_list[deep] = minimax_alg(copy.deepcopy(map), (pos_pacman[0] - 1, pos_pacman[1]), copy.deepcopy(pos_ghost_new), copy.deepcopy(score), deep + 1,upp_list,down_list,right_list,left_list)
        if  map[pos_pacman[0] + 1][pos_pacman[1]] != 1: # kiem tra di down khac tuong
            down_list[deep] = minimax_alg(copy.deepcopy(map), (pos_pacman[0] + 1, pos_pacman[1]), copy.deepcopy(pos_ghost_new), copy.deepcopy(score), deep + 1,upp_list,down_list,right_list,left_list)
        if  map[pos_pacman[0]][pos_pacman[1] - 1] != 1: # kiem tra di left khac tuong
            left_list[deep] = minimax_alg(copy.deepcopy(map), (pos_pacman[0], pos_pacman[1] - 1), copy.deepcopy(pos_ghost_new), copy.deepcopy(score), deep + 1,upp_list,down_list,right_list,left_list)
        if  map[pos_pacman[0]][pos_pacman[1] + 1]!= 1: # kiem tra di right khac tuong
            right_list[deep] = minimax_alg(copy.deepcopy(map), (pos_pacman[0], pos_pacman[1] + 1), copy.deepcopy(pos_ghost_new), copy.deepcopy(score), deep + 1,upp_list,down_list,right_list,left_list)


        max_score = max(upp_list[deep], down_list[deep], left_list[deep], right_list[deep])
        return max_score


# Tim vi tri tot nhat de di chuyen
def best_move(map, pos_pacman, pos_ghost,pos_food):
    pos_pacman1 = copy.deepcopy(pos_pacman)
    pos_pacman2 = copy.deepcopy(pos_pacman)
    pos_pacman3 = copy.deepcopy(pos_pacman)
    pos_pacman4 = copy.deepcopy(pos_pacman)
    upp = -9999
    down = -9999
    left = -9999
    right = -9999
    if  map[pos_pacman[0] - 1][pos_pacman[1]] != 1: # kiem tra di len khac tuong
        upp_list = [-9999] * 10
        down_list = [-9999] * 10
        left_list = [-9999] * 10
        right_list = [-9999] * 10
        upp = minimax_alg(copy.deepcopy(map), (pos_pacman1[0] - 1, pos_pacman1[1]), copy.deepcopy(pos_ghost), 0, 1,upp_list,down_list,right_list,left_list)
    if  map[pos_pacman[0] + 1][pos_pacman[1]] != 1: # kiem tra di down khac tuong
        upp_list = [-9999] * 10
        down_list = [-9999] * 10
        left_list = [-9999] * 10
        right_list = [-9999] * 10
        down = minimax_alg(copy.deepcopy(map), (pos_pacman2[0] + 1, pos_pacman2[1]), copy.deepcopy(pos_ghost), 0, 1,upp_list,down_list,right_list,left_list)
    if  map[pos_pacman[0]][pos_pacman[1] - 1] != 1: # kiem tra di left khac tuong
        upp_list = [-9999] * 10
        down_list = [-9999] * 10
        left_list = [-9999] * 10
        right_list = [-9999] * 10
        left = minimax_alg(copy.deepcopy(map), (pos_pacman3[0], pos_pacman3[1] - 1), copy.deepcopy(pos_ghost), 0, 1,upp_list,down_list,right_list,left_list)
    if  map[pos_pacman[0]][pos_pacman[1] + 1]!= 1: # kiem tra di right khac tuong
        upp_list = [-9999] * 10
        down_list = [-9999] * 10
        left_list = [-9999] * 10
        right_list = [-9999] * 10
        right = minimax_alg(copy.deepcopy(map), (pos_pacman4[0], pos_pacman4[1] + 1), copy.deepcopy(pos_ghost), 0, 1,upp_list,down_list,right_list,left_list)
    
    max_score = max(upp, down, left, right)
    
    pos_upp = (pos_pacman[0] - 1, pos_pacman[1])
    pos_down = (pos_pacman[0] + 1, pos_pacman[1])
    pos_left = (pos_pacman[0], pos_pacman[1] - 1)
    pos_right = (pos_pacman[0], pos_pacman[1] + 1)
    # Check truong hop sore 4 thang khac nhau
    if upp != down and upp != left and upp != right and down != left and down != right and left != right:
        if max_score == upp:
            return  pos_upp
        elif max_score == down:
            return pos_down
        elif max_score == left:
            return pos_left
        else:
            return pos_right
        '''
        Check truong hop score 2 thang bang nhau: vi du upp == down
        '''
    # Check upp = down (voi upp, down, left, right la score)
    elif upp == down and upp != left and upp != right and left != right:
        if max_score == left:
            return  pos_left
        if max_score == right:
            return pos_right
        if max_score == upp: # Chung to max_score = down luon
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_down, food):
                return pos_upp
            else:
                return pos_down
    

    # Check upp == right
    elif upp == right and upp != left and upp != down and left != down:
        if max_score == left:
            return  pos_left
        if max_score == down:
            return pos_down
        if max_score == upp: # Chung to max_score = right luon
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_right, food):
                return pos_upp
            else:
                return pos_right
    
    # Check upp == left
    elif upp == left and upp != right and upp != down and right != down:
        if max_score == right:
            return pos_right
        if max_score == down:
            return pos_down
        if max_score == upp: # Chung to max_score = right luon
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_left, food):
                return pos_upp
            else:
                return pos_left
            
    # Check down == left
    elif down == left and down != right and down != upp and right != upp:
        if max_score == right:
            return  pos_right
        if max_score == upp:
            return pos_upp
        if max_score == down: # Chung to max_score = left luon
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_down, food) <= calculate_distance(pos_left, food):
                return pos_down
            else:
                return pos_left
            
    # check down == right
    elif down == right and down != left and down != upp and left != upp:
        if max_score == left:
            return  pos_left
        if max_score == upp:
            return pos_upp
        if max_score == down: # Chung to max_score = left luon
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_down, food) <= calculate_distance(pos_right, food):
                return pos_down
            else:
                return pos_right
    # check left == right
    elif left == right and right != upp and down != right and down != upp:
        if max_score == down:
            return  pos_down
        if max_score == upp:
            return pos_upp
        if max_score == right: # Chung to max_score = left luon
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_left, food) <= calculate_distance(pos_right, food):
                return pos_left
            else:
                return pos_right
            
        '''
            truong hop 2 cap bang nhau, khac nhau 
        '''
    elif right == left and upp == down and right != upp:
        if max_score == right:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_left, food) <= calculate_distance(pos_right, food):
                return pos_left
            else:
                return pos_right
        if max_score == upp:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_down, food):
                return pos_upp
            else:
                return pos_down
    #
    elif right == upp and left == down and right != left:
        if max_score == right:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_right, food):
                return pos_upp
            else:
                return pos_right
        if max_score == left:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_left, food) <= calculate_distance(pos_down, food):
                return pos_left
            else:
                return pos_down
    elif right == down and upp == left and right != upp:
        if max_score == right:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_down, food) <= calculate_distance(pos_right, food):
                return pos_down
            else:
                return pos_right
        if max_score == upp:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_left, food):
                return pos_upp
            else:
                return pos_left
        '''
            Check truong hop 3 score bang nhau: vi du score cua upp == down == left , ...
        '''
    # Check upp = left = right
    elif upp == left and left == right and right != down:
        if max_score == down:
            return pos_down
        else:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            min_pos = min(calculate_distance(pos_left, food), calculate_distance(pos_right, food), calculate_distance(pos_upp, food)) 
            if min_pos == calculate_distance(pos_left, food):
                return pos_left
            elif min_pos == calculate_distance(pos_right, food):
                return pos_right
            else:
                return pos_upp
    # Check upp = left = down
    elif upp == left and left == down and down != right:
        if max_score == right:
            return pos_right
        else:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            min_pos = min(calculate_distance(pos_left, food), calculate_distance(pos_down, food), calculate_distance(pos_upp, food)) 
            if min_pos == calculate_distance(pos_left, food):
                return pos_left
            elif min_pos == calculate_distance(pos_upp, food):
                return pos_upp
            else:
                return pos_down
    # Check upp = right = down
    elif upp == right and right == down and left != right:
        if max_score == left:
            return pos_left
        else:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            min_pos = min(calculate_distance(pos_right, food), calculate_distance(pos_down, food), calculate_distance(pos_upp, food)) 
            if min_pos == calculate_distance(pos_upp, food):
                return pos_upp
            elif min_pos == calculate_distance(pos_right, food):
                return pos_right
            else:
                return pos_down
    # Check left = right = down
    elif left == right and right == down and left != upp:
        if max_score == upp:
            return pos_upp
        else:
            food_check = check_pos_nearest_food(pos_pacman, pos_food)
            index_opt = check_food_index_opt(food_check,map)
            food = food_check[index_opt]
            min_pos = min(calculate_distance(pos_right, food), calculate_distance(pos_down, food), calculate_distance(pos_left, food)) 
            if min_pos == calculate_distance(pos_left, food):
                return pos_left
            elif min_pos == calculate_distance(pos_right, food):
                return pos_right
            else:
                return pos_down

    # Check upp =down = left= right
    elif upp == down and down == left and left == right:
        food_check = check_pos_nearest_food(pos_pacman, pos_food)
        index_opt = check_food_index_opt(food_check,map)
        food = food_check[index_opt]
        min_pos = min(calculate_distance(pos_right, food), calculate_distance(pos_down, food), calculate_distance(pos_left, food),calculate_distance(pos_upp, food)) 
        if min_pos == calculate_distance(pos_left, food):
            return pos_left
        elif min_pos == calculate_distance(pos_right, food):
            return pos_right
        elif min_pos == calculate_distance(pos_upp, food):
            return pos_upp
        else:
            return pos_down

# Ham tra ve toa do food gan pacman nhat
def check_pos_nearest_food(pos_pacman, pos_food):
    sorted_food = sorted(pos_food, key=lambda food: calculate_distance(pos_pacman, food))
    return sorted_food

# Tinh khoang cach pac man toi food
def calculate_distance(pos_pacman, pos_food):
    return math.sqrt((pos_food[0]-pos_pacman[0])**2 + (pos_food[1]-pos_pacman[1])**2)

def check_food_index_opt(food_check,map):
    index = 0
    for food_temp in food_check:
        check_food_hard = 0
        if map[food_temp[0] - 1][food_temp[1]] == 1:
            check_food_hard += 1
        if map[food_temp[0] + 1][food_temp[1]] == 1:
            check_food_hard += 1
        if map[food_temp[0]][food_temp[1] - 1] == 1:
            check_food_hard += 1
        if map[food_temp[0]][food_temp[1] + 1] == 1:
            check_food_hard += 1
        if check_food_hard != 3:
            return index
        else:
            index += 1
    return 0
    
