from Astar import *
import math
import copy

# pos_food = [(2,1)]
# for y, row in enumerate(map):
#     for x, block in enumerate(row):
#         if map[y][x] == 2:
#             pos_food.append((y,x))
def minimax_alg(map, pos_pacman, pos_ghost, score, deep):
    down, left, right = -9999,-9999,-9999
    upp = -9999
    
    if deep == 10:
        return score
    
    '''
        Pacman di toi cho ghost
    '''
    # pos_food = []
    # for y, row in enumerate(map):
    #     for x, block in enumerate(row):
    #         if map[y][x] == 2:
    #             pos_food.append((y,x))

    # upp = down = left = right = -9999 
    
    for ghost in pos_ghost:
        if pos_pacman == ghost:
            score -= 99999

    if map[pos_pacman[0]][pos_pacman[1]] == 0:
        score -= 1
    elif map[pos_pacman[0]][pos_pacman[1]] == 2:
        score += 20
        map[pos_pacman[0]][pos_pacman[1]] = 0
        # pos_food = [item for item in pos_food if item != (pos_pacman[0], pos_pacman[1])]

    # for y, row in enumerate(map):
    #     for x, block in enumerate(row):
    #         if map[y][x] == 2:
    #             pos_food.append((y,x))
    
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
            score -= 99999
    
    # deep = deep + 1
    # print(deep)
    # upp, down, left, right la score
    if  map[pos_pacman[0]][pos_pacman[1] - 1] != 1: # kiem tra di len khac tuong
        upp = minimax_alg(map, (pos_pacman[0], pos_pacman[1] - 1), pos_ghost, copy.deepcopy(score), deep + 1)
    if  map[pos_pacman[0]][pos_pacman[1] + 1] != 1: # kiem tra di down khac tuong
        down = minimax_alg(map, (pos_pacman[0], pos_pacman[1] + 1), pos_ghost, copy.deepcopy(score), deep + 1)
    if  map[pos_pacman[0] - 1][pos_pacman[1]] != 1: # kiem tra di left khac tuong
        left = minimax_alg(map, (pos_pacman[0] - 1, pos_pacman[1]), pos_ghost, copy.deepcopy(score), deep + 1)
    if  map[pos_pacman[0] + 1][pos_pacman[1]]!= 1: # kiem tra di right khac tuong
        right = minimax_alg(map, (pos_pacman[0] + 1, pos_pacman[1]), pos_ghost, copy.deepcopy(score), deep + 1)


    max_score = max(upp, down, left, right)
    return max_score

# Tim vi tri tot nhat de di chuyen
def best_move(map, pos_pacman, pos_ghost,pos_food):
    down, left, right = -9999,-9999,-9999
    upp = -9999
    # for y, row in enumerate(map):
    #     for x, block in enumerate(row):
    #         if map[y][x] == 2:
    #             pos_food.append((y,x))
    # map1 = copy.deepcopy(map)
    # upp, down, left, right la score
    pos_pacman1 = copy.deepcopy(pos_pacman)
    pos_pacman2 = copy.deepcopy(pos_pacman)
    pos_pacman3 = copy.deepcopy(pos_pacman)
    pos_pacman4 = copy.deepcopy(pos_pacman)

    if  map[pos_pacman[0]][pos_pacman[1] - 1] != 1: # kiem tra di len khac tuong
        upp = minimax_alg(copy.deepcopy(map), (pos_pacman1[0], pos_pacman1[1] - 1), pos_ghost, 0, 1)
    if  map[pos_pacman[0]][pos_pacman[1] + 1] != 1: # kiem tra di down khac tuong
        down = minimax_alg(copy.deepcopy(map), (pos_pacman2[0], pos_pacman2[1] + 1), pos_ghost, 0, 1)
    if  map[pos_pacman[0] - 1][pos_pacman[1]] != 1: # kiem tra di left khac tuong
        left = minimax_alg(copy.deepcopy(map), (pos_pacman3[0] - 1, pos_pacman3[1]), pos_ghost, 0, 1)
    if  map[pos_pacman[0] + 1][pos_pacman[1]]!= 1: # kiem tra di right khac tuong
        right = minimax_alg(copy.deepcopy(map), (pos_pacman4[0] + 1, pos_pacman4[1]), pos_ghost, 0, 1)

    max_score = max(upp, down, left, right)
    # Check truong hop sore 4 thang khac nhau
    if upp != down and upp != left and upp != right and down != left and down != right and left != right:
        if max_score == upp:
            return  (pos_pacman[0], pos_pacman[1] - 1)
        elif max_score == down:
            return (pos_pacman[0], pos_pacman[1] + 1)
        elif max_score == left:
            return (pos_pacman[0] - 1, pos_pacman[1])
        else:
            return (pos_pacman[0] + 1, pos_pacman[1])
        '''
        Check truong hop score 2 thang bang nhau: vi du upp == down
        '''
    # Check upp = down (voi upp, down, left, right la score)
    elif upp == down and upp != left and upp != right and left != right:
        if max_score == left:
            return  (pos_pacman[0] - 1, pos_pacman[1])
        if max_score == right:
            return (pos_pacman[0] + 1, pos_pacman[1])
        if max_score == upp: # Chung to max_score = down luon
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_down, food):
                return pos_upp
            else:
                return pos_down
    

    # Check upp == right
    elif upp == right and upp != left and upp != down and left != down:
        if max_score == left:
            return  (pos_pacman[0] - 1, pos_pacman[1])
        if max_score == down:
            return (pos_pacman[0], pos_pacman[1] + 1)
        if max_score == upp: # Chung to max_score = right luon
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_right, food):
                return pos_upp
            else:
                return pos_right
    
    # Check upp == left
    elif upp == left and upp != right and upp != down and right != down:
        if max_score == right:
            return  (pos_pacman[0] + 1, pos_pacman[1])
        if max_score == down:
            return (pos_pacman[0], pos_pacman[1] + 1)
        if max_score == upp: # Chung to max_score = right luon
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)
            pos_left = (pos_pacman[0] - 1, pos_pacman[1])
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_left, food):
                return pos_upp
            else:
                return pos_left
            
    # Check down == left
    elif down == left and down != right and down != upp and right != upp:
        if max_score == right:
            return  (pos_pacman[0] + 1, pos_pacman[1])
        if max_score == upp:
            return (pos_pacman[0], pos_pacman[1] - 1)
        if max_score == down: # Chung to max_score = left luon
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            pos_left = (pos_pacman[0] - 1, pos_pacman[1])
            if calculate_distance(pos_down, food) <= calculate_distance(pos_left, food):
                return pos_down
            else:
                return pos_left
            
    # check down == right
    elif down == right and down != left and down != upp and left != upp:
        if max_score == left:
            return  (pos_pacman[0] - 1, pos_pacman[1])
        if max_score == upp:
            return (pos_pacman[0], pos_pacman[1] - 1)
        if max_score == down: # Chung to max_score = left luon
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            if calculate_distance(pos_down, food) <= calculate_distance(pos_right, food):
                return pos_down
            else:
                return pos_right
    # check left == right
    elif left == right and right != upp and down != right and down != upp:
        if max_score == down:
            return  (pos_pacman[0], pos_pacman[1] + 1)
        if max_score == upp:
            return (pos_pacman[0], pos_pacman[1] - 1)
        if max_score == right: # Chung to max_score = left luon
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_left = (pos_pacman[0] -  1, pos_pacman[1])
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            if calculate_distance(pos_left, food) <= calculate_distance(pos_right, food):
                return pos_left
            else:
                return pos_right
            
        '''
            truong hop 2 cap bang nhau, khac nhau 
        '''
    elif right == left and upp == down and right != upp:
        if max_score == right:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_left = (pos_pacman[0] -  1, pos_pacman[1])
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            if calculate_distance(pos_left, food) <= calculate_distance(pos_right, food):
                return pos_left
            else:
                return pos_right
        if max_score == upp:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_down, food):
                return pos_upp
            else:
                return pos_down
    #
    elif right == upp and left == down and right != left:
        if max_score == right:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_right, food):
                return pos_upp
            else:
                return pos_right
        if max_score == left:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_left = (pos_pacman[0] - 1, pos_pacman[1])
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            if calculate_distance(pos_left, food) <= calculate_distance(pos_down, food):
                return pos_left
            else:
                return pos_down
    elif right == down and upp == left and right != upp:
        if max_score == right:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            if calculate_distance(pos_down, food) <= calculate_distance(pos_right, food):
                return pos_down
            else:
                return pos_right
        if max_score == upp:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            if calculate_distance(pos_upp, food) <= calculate_distance(pos_right, food):
                return pos_upp
            else:
                return pos_right
        '''
            Check truong hop 3 score bang nhau: vi du score cua upp == down == left , ...
        '''
    # Check upp = left = right
    elif upp == left and left == right and right != down:
        if max_score == down:
            return (pos_pacman[0], pos_pacman[1] + 1)
        else:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_left = (pos_pacman[0] -  1, pos_pacman[1])
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)

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
            return (pos_pacman[0] + 1, pos_pacman[1])
        else:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_left = (pos_pacman[0] - 1, pos_pacman[1])
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)

            min_pos = min(calculate_distance(pos_left, food), calculate_distance(pos_down, food), calculate_distance(pos_upp, food)) 
            if min_pos == calculate_distance(pos_left, food):
                return pos_left
            elif min_pos == calculate_distance(pos_right, food):
                return pos_right
            else:
                return pos_down
    # Check upp = right = down
    elif upp == right and right == down and left != right:
        if max_score == left:
            return (pos_pacman[0] - 1, pos_pacman[1])
        else:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            pos_upp = (pos_pacman[0], pos_pacman[1] - 1)

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
            return (pos_pacman[0], pos_pacman[1] - 1)
        else:
            food = check_pos_nearest_food(pos_pacman, pos_food)
            pos_right = (pos_pacman[0] + 1, pos_pacman[1])
            pos_down = (pos_pacman[0], pos_pacman[1] + 1)
            pos_left = (pos_pacman[0] - 1, pos_pacman[1])

            min_pos = min(calculate_distance(pos_right, food), calculate_distance(pos_down, food), calculate_distance(pos_left, food)) 
            if min_pos == calculate_distance(pos_left, food):
                return pos_left
            elif min_pos == calculate_distance(pos_right, food):
                return pos_right
            else:
                return pos_down

    # Check upp =down = left= right
    elif upp == down and down == left and left == right:
        food = check_pos_nearest_food(pos_pacman, pos_food)
        pos_upp = (pos_pacman[0], pos_pacman[1] - 1)
        pos_right = (pos_pacman[0] + 1, pos_pacman[1])
        pos_down = (pos_pacman[0], pos_pacman[1] + 1)
        pos_left = (pos_pacman[0] - 1, pos_pacman[1])

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
    food1 = pos_food[0]
    min = calculate_distance(pos_pacman, food1)
    food_dis_min =  food1 # luu toa do food gan pac man nhat
    # Duyet qua tat cac ca food de tinh khoang cach min
    for food in pos_food:
        if min > calculate_distance(pos_pacman, food):
            min = calculate_distance(pos_pacman, food)
            food_dis_min = food

    return food_dis_min

# Tinh khoang cach pac man toi food
def calculate_distance(pos_pacman, pos_food):
    return math.sqrt((pos_food[0]-pos_pacman[0])**2 + (pos_food[1]-pos_pacman[1])**2)
