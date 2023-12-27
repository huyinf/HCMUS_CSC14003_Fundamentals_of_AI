from generate_map import *

import heapq
import re
import os
import shutil

signal_pairs = {'W':'S',
                'S':'W',
                'B':'P',
                'P':'B',
                'BS':'PW',
                'E':''
                }

opposite_dir_pairs = (('U','D'),('D','U'),('L','R'),('R','L'))


# FOL model
'''
input:
    map M
    number of golds nG
    number of wumpus nW
output:
    state of game, number of iterations, left golds, left wumpuses, score, instruction list, path, shoot_wumpus list
'''
def FOLmodel(M,nG,nW):
    # knowledge: list of signals
    K = [[set() for _ in range(len(row))] for row in M]
    # track visiting times
    V = [[0 for _ in range(len(row))] for row in M]
    
    # entrance - bottom left
    start_pos = (len(M)-1,0)
    
    # empty and safe room
    K[len(M)-1][0].update(['A','V'])
    V[len(M)-1][0] = 1
    
    # exit - bottom left
    exit_pos = (len(M)-1,0)
    
    # state of game - win, die, out, loop
    state = ''

    # record visited cells
    pos_list = []
    
    # record path, not include cells that agent shoots more than once
    path = []
    
    # shoot lists
    shoot_wumpus = []
    
    # instruction list
    '''
    action - forward, turn back, turn left, turn right, shoot (no move)
    encode - F,B,L,R,S
    '''
    actions = []
    
    # initial direction
    direction = 'R'
    
    
    # get score and scores_list for game visualization
    scores_list = []
    
    score = 0
    
    # # record current position in while loop
    curr_pos = start_pos
    
    k = 1000
    iterations = 0
    def results():
        return state,iterations,nG,nW,score,actions,path,pos_list,shoot_wumpus
    
        # print('knowledge:',K)
        # print("Visited times:",V)      
        # print('path:',path)
        # print('score:',score)
        # print('left wumpuses:',nW)
        # print('left golds:',nG)
        # print('instruction: ',actions)
        # print("number of iterations: ",100-k)
    
    
    # run until win or die or out
    while True:
        iterations += 1
        
        # k -= 1
        # use for report
        if iterations >= k:
            iterations -= 1
            break
             
        x,y = curr_pos        
        
        signal = M[x][y]
        
        # skip visited cells
        if 'V' not in K[x][y]:
            
            # update signal of unvisited cells
            K[x][y].update(signal)
            # stupid defined logic leads this shit code
            remove_conflict(x,y,K)
            # check dead case: W or P in signals
            if 'W' in K[x][y] or 'P' in K[x][y]:
                # if W or P in current cell, dead
                state = 'die'
                score -= 10000
                scores_list.append(score)
                return results()
            
            # if agent is still alive and game is still running
            
            # regardless of knowledge, update knowledge with new information
            if 'G' in K[x][y]:
                # if map is out of gold, no action
                nG = max(nG-1,0)
                K[x][y].remove('G')
                # gold is not in same room with wumpus or pit
                K[x][y].update(['-P','-W'])

            # process signals of current cell for adjacent cells
            update_kb(K[x][y],x,y,M,K)
            # update current cell as visited
            K[x][y].update(['V'])
        
        # record visited times of cells
        # if last action was shooting, no increase
        if len(actions) > 0 and actions[-1] != 'S': # or == 'F'
            V[x][y] += 1
        # print(K)
        
        # make next action: shoot or move
        (rotation,new_direction),action = new_action(x,y,M,K,V,direction)
        # check state of agent
        # get all golds and kill all wumpuses
        if nG == 0 and nW == 0:
            state = 'win'
            return results()
        
        # if game is still running, update action
        actions.append(rotation)
        actions.append(action)
        
        # if agent shoots, preserve old direction and shoot
        if action == 'S':
            new_pos = new_move(x,y,M,new_direction)
            if kill_wumpus(new_pos[0],new_pos[1],M,K) == True:
                nW = max(nW-1,0)
            # record shooting positions
            shoot_wumpus.append(new_pos)
            # update score after shooting
            score -= 100
            scores_list.append(score)
            
        # if agent moves, get new direction and make move
        direction = new_direction
        if action == 'F':
            # if moving but not shooting
            curr_pos = new_move(x,y,M,direction)
            
        score -= 10
        scores_list.append(score)
        
        # update path and record visited cells
        pos_list.append(curr_pos)
    
        if path == [] or path[-1] != curr_pos:
            path.append(curr_pos)

        # more optimal design, but not implemented:
        # if agent can not find more optimal move, agent proactively finds the exit postion to end game
        
        # climb out of the cave
        if len(actions) > 0 and actions[-1] == 'F' and direction == 'L' and curr_pos == exit_pos:
            state = 'out'
            # a helper function for this case, not implemented
            return results()
    
    # if game cannot end in 100 iterations, it is a loop 
    state = 'loop'
    return results()


'''
remove confict signals
input:
    pair of conflict signals
    K   - knowledge
    x,y - position of cell
ouput:
    remove - positive signal
'''
def helper(a,b,x,y,K):
    a_exists = a in K[x][y]
    b_exists = b in K[x][y]
    
    if a_exists and b_exists:
        K[x][y].remove(a)


def remove_conflict(x,y,K):
    a_list = ['S','B','W','P']
    b_list = ['-S','-B','-W','-P']
    
    for a,b in zip(a_list,b_list):
        helper(a,b,x,y,K)
     
        
'''
update knowledge with new information
input:
    sig_list   - list of signals of current cell
    x,y - position of cell
    K   - knowledge of agent
    # V   - matrix of visited times (maybe no use)
    M  - map of game
output:
    updated knowledge of agent based on new information
'''
def update_kb(sig_list,x,y,M,K):
    
    if 'A' in sig_list or '-' in sig_list:
        # sig_list.clear()
        K[x][y].update(['-P','-W','-S','-B'])
        if '-' in sig_list:
            K[x][y].remove('-')
            
    # update signals for current cell
    if 'S' not in K[x][y]:
        K[x][y].update(['-S'])
    if 'B' not in K[x][y]:
        K[x][y].update(['-B'])
    if 'W' in K[x][y]:
        K[x][y].update(['-P','-B','-S'])
    if 'P' in K[x][y]:
        K[x][y].update(['-W','-B','-S'])

    # process confictions
    remove_conflict(x,y,K)
    
    # neighbors of current cell
    neighbors = get_neighbors(x,y,M)
    
    # order of processing signals
    for s in K[x][y]:
        # skip 'V' signal and non-valuable signals (-W,-P)
        if s in ('V','-W','-P'):
            continue
        # update knowledge of univisted neighbors
        
        for n in neighbors:
            nX,nY = n
            if 'V' not in K[nX][nY]:
                # adjacent cells of A are not wumpus or pit
                if s == 'A' or s == 'G':
                    K[nX][nY].update(['-P','-W'])
                # adjacent cells of B are P
                elif s == 'B':
                    K[nX][nY].update(['P'])
                # adjacent cells of S are W
                elif s == 'S':
                    K[nX][nY].update(['W'])
                # adjacent cells of P are B
                elif s == 'P':
                    K[nX][nY].update(['B'])
                # adjacent cells of W are S
                elif s == 'W':
                    K[nX][nY].update(['S'])
                # adjacent cells of -B are -P, remove P if possible
                elif s == '-B':
                    if 'P' in K[nX][nY]:
                        K[nX][nY].remove('P')
                    K[nX][nY].update(['-P'])
                # adjacent cells of -S are -W, remove W if possible
                elif s == '-S':
                    if 'W' in K[nX][nY]:
                        K[nX][nY].remove('W')
                    K[nX][nY].update(['-W'])
                    
                # not sure
                
                # # adjacent cells of -P are -B, remove B if possible
                # elif s == '-P':
                #     if 'B' in K[nX][nY]:
                #         K[nX][nY].remove('B')
                #     K[nX][nY].update(['-B'])
                # # adjacent cells of -W are -S, remove S if possible
                # elif s == '-W':
                #     if 'S' in K[nX][nY]:
                #         K[nX][nY].remove('S')
                #     K[nX][nY].update(['-S'])
    
                
    # post-process knowledge of adjacent cells of current cell
    # ignore all opposite signals
    for n in neighbors:
        nX,nY = n
        # if adjacent cells of current cell are not visited
        if 'V' not in K[nX][nY]:
            # # print(K[nX][nY])
            # # if {'P','-P'} in K[nX][nY]:
            # a = 'P' in K[nX][nY]
            # b = '-P' in K[nX][nY]
            # if (a and b) == True:
            #     K[nX][nY].remove('P')
            
            # a = 'W' in K[nX][nY]
            # b = '-W' in K[nX][nY]
            # if (a and b) == True:
            #     K[nX][nY].remove('W')
                
            # a = 'B' in K[nX][nY]
            # b = '-B' in K[nX][nY]
            # if (a and b) == True:
            #     K[nX][nY].remove('B')
            
            # a = 'S' in K[nX][nY]
            # b = '-S' in K[nX][nY]
            # if (a and b) == True:
            #     K[nX][nY].remove('S')
            
            remove_conflict(nX,nY,K)    
            a = 'P' in K[nX][nY]
            b = 'W' in K[nX][nY]
            
            if (a and b) == True:
                K[nX][nY].difference_update(['P','W'])
                # K[nX][nY].update({'P','W'})
   
            
'''
make new action base on knowledge of agent
input:
    x,y - position of agent
    M   - map of game
    K   - knowledge of agent
    V   - matrix of visited times
    direction - current direction of agent
    
    priority:
    if next cell is valid
    forward if safe (-W and -P)
    shoot if maybe wumpus (W)
    left or right if no W and P
    back if not safe (W or P)
output:
    shoot (S) or move(F) signal, rotation and direction
    all returned move are safe, choose one with the smallest visted times
'''
def new_action(x,y,M,K,V,direction):
    # dir_priority = ['F','L','R','B']
    # 0,1,2,3
    
    list_actions = []
        
    neighbors = get_neighbors(x,y,M)
    
    # choose from neighbors
    for n in neighbors:
        nX,nY = n
        if(valid_cell(nX,nY,M)):
            rotation,new_direction = rotate(direction,x,y,nX,nY)
            # forward
            if rotation == None:
                # print(K[nX][nY])
                a = 'P' not in K[nX][nY]
                b = 'W' not in K[nX][nY]
                # print(a and b)
                c = a and b
                # ({'P'} not in K[nX][nY]) and ({'W'} not in K[nX][nY])
                if c == True:
                    # return rotate(direction,x,y,forward_cell[0],forward_cell[1]),'F'
                    list_actions.append((0,V[nX][nY],(rotation,new_direction),'F'))
            # left
            elif rotation == 'L':
                if 'P' not in K[nX][nY]:
                    # if maybe 'W', no move, just
                    if 'W' in K[nX][nY]:
                        # return rotate(direction,x,y,left_cell[0],left_cell[1]),'S'
                        list_actions.append((1,V[nX][nY],(rotation,new_direction),'S'))
                    else:
                        # return rotate(direction,x,y,left_cell[0],left_cell[1]),'F'
                        list_actions.append((1,V[nX][nY],(rotation,new_direction),'F'))
            # right
            elif rotation == 'R':
                if 'P' not in K[nX][nY]:
                    # if maybe 'W', no move, just
                    if 'W' in K[nX][nY]:
                        # return rotate(direction,x,y,right_cell[0],right_cell[1]),'S'
                        list_actions.append((2,V[nX][nY],(rotation,new_direction),'S'))
                    else:
                        # return rotate(direction,x,y,right_cell[0],right_cell[1]),'F'
                        list_actions.append((2,V[nX][nY],(rotation,new_direction),'F'))
            # backward
            elif rotation == 'B':
                # return rotate(direction,x,y,backward_cell[0],backward_cell[1]),'F'
                list_actions.append((3,V[nX][nY],(rotation,new_direction),'F'))
    
    # forward_cell = new_move(x,y,M,direction)
    # # if cell is valid and safe, move forward
    # if forward_cell is not None:
    #     if {'W','P'} not in K[forward_cell[0]][forward_cell[1]]:
    #         # return rotate(direction,x,y,forward_cell[0],forward_cell[1]),'F'
    #         list_actions.append((0,V[forward_cell[0]][forward_cell[1]],rotate(direction,x,y,forward_cell[0],forward_cell[1]),'F'))
    
    # # if left cell is valid, not pit
    # new_direction = 'L'
    # left_cell = new_move(x,y,M,new_direction)
    # if left_cell is not None:
    #     if 'P' not in K[left_cell[0]][left_cell[1]]:
    #         # if maybe 'W', no move, just
    #         if 'W' in K[left_cell[0]][left_cell[1]]:
    #             # return rotate(direction,x,y,left_cell[0],left_cell[1]),'S'
    #             list_actions.append((1,V[left_cell[0]][left_cell[1]],rotate(direction,x,y,left_cell[0],left_cell[1]),'S'))
    #         else:
    #             # return rotate(direction,x,y,left_cell[0],left_cell[1]),'F'
    #             list_actions.append((1,V[left_cell[0]][left_cell[1]],rotate(direction,x,y,left_cell[0],left_cell[1]),'F'))
            
    # # if right cell is valid, not pit
    # new_direction = 'R'
    # right_cell = new_move(x,y,M,new_direction)
    # if right_cell is not None:
    #     if 'P' not in K[right_cell[0]][right_cell[1]]:
    #         # if maybe 'W', no move, just
    #         if 'W' in K[right_cell[0]][right_cell[1]]:
    #             # return rotate(direction,x,y,right_cell[0],right_cell[1]),'S'
    #             list_actions.append((2,V[right_cell[0]][right_cell[1]],rotate(direction,x,y,right_cell[0],right_cell[1]),'S'))
    #         else:
    #             # return rotate(direction,x,y,right_cell[0],right_cell[1]),'F'
    #             list_actions.append((2,V[right_cell[0]][right_cell[1]],rotate(direction,x,y,right_cell[0],right_cell[1]),'F'))
            
    # # backward if there is no safe cell
    # direction = 'D'
    # backward_cell = new_move(x,y,M,new_direction)
    # # return rotate(direction,x,y,backward_cell[0],backward_cell[1]),'F'
    # list_actions.append((3,V[backward_cell[0]][backward_cell[1]],rotate(direction,x,y,backward_cell[0],backward_cell[1]),'F'))
    
    # sort list of actions based on priority
    list_actions.sort(key=lambda x: (x[1],x[0]))
    
    return list_actions[0][2],list_actions[0][3]


'''
new move base on direction
'''
def new_move(x,y,M,direction):
    # up, down, left, right
    # vertical
    dx = [-1,1,0,0]
    # horizontal
    dy = [0,0,-1,1]
    
    nX,nY = x,y
    if direction == 'U':
        nX += dx[0]
    elif direction == 'D':
        nX += dx[1]
    elif direction == 'L':
        nY += dy[2]
    elif direction == 'R':
        nY += dy[3]
    
    return (nX,nY) if valid_cell(nX,nY,M) else None


'''
get valid neighbors of current cell
input:
    x,y - position of current cell
    M   - map of game
output:
    a list of valid neighbors of current cell
'''
def get_neighbors(x,y,M):
    # (0,0) is top left in python, but (0,0) is bottom left in game
    # up, down, left, right
    # vertical
    dx = [-1,1,0,0]
    # horizontal
    dy = [0,0,-1,1]
    
    res = []
    
    for i in range(len(dx)):
        new_x,new_y = x+dx[i],y+dy[i]
        if valid_cell(new_x,new_y,M):
            res.append((new_x,new_y))
            
    return res
 
  
'''
# valid cell is not outside of map
input:
    x,y - position of cell
    M   - map of game
output:
    check if cell is inside map
'''
def valid_cell(x,y,M):
    return x >= 0 and x < len(M) and y >= 0 and y < len(M[0])


'''
read from input file and build map
input:
    filename - path to input file
output:
    M   - map of game
    nG  - number of golds
    nW  - number of wumpuses
'''
def build_map(filename):
    rows = []
    
    with open(filename,'r') as f:
        lines = f.readlines()
        # get size of map --> map: sz x sz
        # sz = int(lines[0])
        # get value for cells, remove escape character '\n'
        rows = [[(cell[:-1] if cell.endswith('\n') else cell) for cell in line.split('.')] for line in lines]


    m = []
    for row in rows:
        row = [set(cell) for cell in row]
        m.append(row)

    nG = 0
    nW = 0
    
    
    for row in m:
        for cell in row:
            # count Wumpus
            if 'W' in cell:
                nW += 1
            # count gold
            elif 'G' in cell:
                nG += 1
            
    return m,nW,nG


'''
write results to output file
input:
    path,score
output:
    file at path '../output.txt'
'''
def write_ouput(path,score,filename):
    
    
    with open(filename,'w') as f:
        for pos in path:    
            f.write(f"({pos[0]},{pos[1]})\n")
        f.write(str(score))
        

# rotation
'''
input:
    direction - current direction of agent (???)
    x,y - current position of agent
    x_next,y_next - position of the disired move of agent
output:
    action - rotate or not
    new_direction
'''
def rotate(direction,x,y,x_next,y_next):
    
    # no action
    if x == x_next and y == y_next:
        return None
    
    # directions - 0,1,2,3
    dirs = ['U','L','D','R']
    # keys - 0,1,2,3
    keys = ['W','A','S','D']
    
    key = ''
    if x_next < x:
        key = 'W'
    if x_next > x:
        key = 'S'
    if y_next < y:
        key = 'A'
    if y_next > y:
        key = 'D'
        
    id_dir = dirs.index(direction)
    
    id_key = keys.index(key)
    
    gap = id_key - id_dir
    
    '''
    '''
    rotation = None
    
    if gap == -1 or gap == 3:
        rotation = 'R'
    
    elif gap == 1 or gap == -3:
        rotation = 'L'
    elif abs(gap) == 2:
        rotation = 'B'
    
    # excel
    # id_new_dir = (id_dir+id_key)%4 if (id_dir%2==0) else (id_dir + id_key + 2)%4
    
    new_direction = dirs[id_key]
    
    return rotation,new_direction
        
    
# kill wumpus
'''
new version for killing wumpus
input:
    x,y - position of wumpus
    M   - map of game
    K   - knowledge of agent
output:
    return True if wumpus is in M[x,y] and update M,K
    if False (signal 'S' are still there) --> update K
'''
def kill_wumpus(x,y,M,K):
    result = False
    if 'W' in M[x][y]:
        result = True
    
    # if wumpus is in this cell, kill it and set as '-W'
    # if wumpus is not in this cell, set as '-W'
    K[x][y].update(['-W'])
    update_kb(K[x][y],x,y,M,K)
    return result