import heapq
import re
import os

signal_pairs = {'W':'S',
                'S':'W',
                'B':'P',
                'P':'B',
                'BS':'PW',
                'E':''
                }

opposite_dir_pairs = (('U','D'),('D','U'),('L','R'),('R','L'))

'''
shooting optimization:
choose that direction the next move
'''


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
    # knowledge
    K = [['' for _ in range(len(row))] for row in M]
    # track visiting times
    V = [[0 for _ in range(len(row))] for row in M]
    
    # entrance - bottom left
    start_pos = (len(M)-1,0)
    
    # empty and safe room
    K[len(M)-1][0] = 'E'
    
    # V[len(M)-1][0] = 1
    
    # exit - bottom left
    exit_pos = (len(M)-1,0)
    
    # state of game - win, die, out, loop
    state = ''

    # record visited cells
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
    
    # get score and score_list for game visualization
    scores_list = []
    
    score = 0
    
    # record current and previous position in while loop
    prev_pos = start_pos
    curr_pos = start_pos
    
    k = 100
    iterations = 0
    def results():
        return state,iterations,nG,nW,score,actions,path,shoot_wumpus
    
        # print('knowledge:',K)
        # print("Visited times:",V)      
        # print('path:',path)
        # print('score:',score)
        # print('left wumpuses:',nW)
        # print('left golds:',nG)
        # print('instruction: ',actions)
        # print("number of iterations: ",100-k)
    
    # run until win or die
    while k >= 0:
        k -= 1
        iterations += 1
        
        # update path and score_list 
        path.append(curr_pos)
        scores_list.append(score)
        
        # # climb out of the cave
        # if curr_pos == exit_pos:
        #     results()


        x_prev,y_prev = prev_pos   
        # update previous position
        prev_pos = curr_pos
             
        x,y = curr_pos        
        
        signal = M[x][y]
        # modify signal based on knowledge and map and visting times
        # if agent has real knowledge about current cell, use it
        if V[x][y] != 0:
            signal = K[x][y]
        # if agent has no knowledge about current cell, but agent inferenced it as E
        # use it
        elif K[x][y] == 'E':
            signal = 'E'
        # other case, leave it as it is
        else:
            # get gold and modify signal
            if 'G' in signal:
                # if map is out of gold, no action
                nG = max(nG-1,0)
                signal = signal.replace('G','')


        # mark empty unvisited room or gold-only is E as a safe room
        if signal in ('-','','A'):
            signal = 'E'
            update_knowledge(x_prev,y_prev,x,y,signal,K,V,M)
                # if agent is still agent or game is still running
        elif signal in ('S','BS'):
            # no update if cell has been visited
            # if V[x][y] == 0:
            update_knowledge(x_prev,y_prev,x,y,signal,K,V,M)
            
              
        elif signal == 'B':
            # if V[x][y] == 0:
            update_knowledge(x_prev,y_prev,x,y,signal,K,V,M)
        # caught by wumpus or fall in pit  
        elif signal == 'W' or signal == 'P':
            # no update if cell has been visited
            # if V[x][y] == 0:
            update_knowledge(x_prev,y_prev,x,y,signal,K,V,M)

            score -= 10000
            state = 'die'
            return results()

                        
        
        
        # update visiting times
        V[x][y] += 1
        
        # in case agent go back to visited rooms if there is danger
        # and there is one unvisited room left on the next move
        # random shoot for safety
        
        
        # get adjacent cells of current cell to find and kill wumpus if possible
        adj_cells = list_of_moves(x,y,M,V,K)
        
        # if there are still some wumpuses, kill them randomly
        if nW > 0:
            # for _,pos in adj_cells:
            
            nX,nY = max(adj_cells,key= lambda x: x[0])[1]
            # use knowledge to determine whether wumpus is in room
            # do not shoot in visited rooms
            if V[nX][nY] == 0:
                if K[nX][nY] in ('W'):
                    
                    # track actions for shooting
                    rotation,new_direction = rotate(direction,x,y,nX,nY)
                    actions.append(rotation)
                    direction = new_direction
                    actions.append('S')
                    
                    # check if wumpus is killed
                    killed = kill(nX,nY,K,M)
                    
                    if killed:
                        # decrease the number of wumpuses if possible
                        nW = max(nW-1,0)

                    # shoot an arrow
                    score -= 100
                    # record shooting rooms
                    shoot_wumpus.append((nX,nY))
    
                # set this cell as the next move
                curr_pos = (nX,nY)
                
    
        
        # get all golds and kill all wumpuses
        if nG == 0 and nW == 0:
            # print('state: win')
            state = 'win'
            return results()
            # return path,score    
        
        
        # if there is no updation in current position, choose another random move
        if curr_pos == prev_pos:
        
            # random good moves
            moves = list_of_moves(x,y,M,V,K)
            
            # choose the "best" move
            curr_pos = move(moves,M)
        
        # change direction for new move
        '''
        '''
        rotation,new_direction = rotate(direction,x,y,curr_pos[0],curr_pos[1])
        actions.append(rotation)
        actions.append('F')
        direction = new_direction
        
        score -= 10

    
    # if game cannot end in 100 iterations, it is a loop 
    state = 'loop'
    return results()


# get list of the next possible moves for agent
'''
input:
    x,y - position of cell
    M   - map of game
    V   - matrix of visited times
    K   - knowledge of agent
output:
    a list of possible moves ordered by visited times and knowledge (min_heap) for agent
'''
def list_of_moves(x,y,M,V,K):
    moves = []
    
    # (0,0) is top left in python, but (0,0) is bottom left in game
    # up, down, left, right
    # vertical
    dx = [-1,1,0,0]
    # horizontal
    dy = [0,0,-1,1]
    
    
    for i in range(len(dx)):
        new_x,new_y = x+dx[i],y+dy[i]        
                
        if valid_cell(new_x,new_y,M):
            # add weight to cell based on visited times and knowledge
            weight = V[new_x][new_y]
            
            if K[new_x][new_y] == 'W':
                weight += 3
            # elif K[new_x][new_y] == 'E':
            #     weight += 50
            # # N/A knowledge
            # elif K[new_x][new_y] == '':
            #     weight += 30
            # dead case
            elif K[new_x][new_y] == 'P':
                weight += 5
            
            heapq.heappush(moves,(weight,(new_x,new_y)))
            
    # print(moves)
    return moves
    

# get the next "best" move for agent
'''
input:
    list_moves  - list of possible moves of agent at the current position
    M           - map of game
output:
    "best" move - 1. cell with the smallest visiting times and not (pit or wumpus)
                - 2. whatever (dead move possible)
'''
def move(list_moves,M):
    
    res = None
    # backup = []
    
    # # get the "best" cell
    # # smallest visiting times
    # # not Pit or Wumpus
    # while len(list_moves) > 0:
        
    #     item = heapq.heappop(list_moves)
        
    #     pos = item[1]
        
    #     x,y = pos
        
    #     if M[x][y] not in ('P','W'):
    #         res = pos
    #         return res
    #     else:
    #         heapq.heappush(backup,item)
        
    # # return any dead cell
    # return heapq.heappop(backup)[1]
    
    res = heapq.heappop(list_moves)[1]
    return res
  
  
# valid cell is not outside of map
'''
input:
    x,y - position of cell
    M   - map of game
output:
    check if cell is inside map
'''
def valid_cell(x,y,M):
    return x >= 0 and x < len(M) and y >= 0 and y < len(M[0])


# make inference based on first order logic (list of possible cases in __init__.py)
'''
input:
    x,y - position of current cell of agent
    val - new information of input cell (not the predicted information)
    K   - knowledge of agent
output:
    updated knowledge of agent based on FOL
'''
# def inference(x,y,val,K):

#     # get the predicted value of current cell
#     # use the current value of current cell to make inference
    
#     prev = K[x][y]
#     curr = val
    
#     if prev == curr:
#         pass
#     elif prev == '':
#         K[x][y] = curr
#     elif prev == 'PW' and curr in ('P','W'):
#         K[x][y] = curr
    
#     elif prev in ('P','W') and curr == 'PW':
#         K[x][y] = prev
        
#     elif prev in ('S','B','P','W') and curr in ('E','BS'):
#         K[x][y] = curr
        
#     elif (prev,curr) == ('P','W') or (prev,curr) == ('W','P'):
#         K[x][y] = 'E'
        
#     elif curr in ('B','S'):
#         if prev not in ('B','S'):
#             K[x][y] = curr
#         else:
#             K[x][y] = 'BS'

def inference(x,y,val,K):

    # get the predicted value of current cell
    # use the current value of current cell to make inference
    
    prev = K[x][y]
    curr = val
    
    # same value --> real knowledge
    if prev == curr:
        pass
    # new knowledge --> real ??
    elif prev == '':
        K[x][y] = curr
    # any previous knowledge 
    # --> real knowledge because adjacent cells of E are not wumpus or pit
    elif re.search('P|W',prev) and curr == '':
        K[x][y] = curr
    # comfirm of pit or wumpus because wumpus and pit are not in the same cell
    elif prev == 'PW' and curr in ('P','W'):
        K[x][y] = curr
    elif prev in ('P','W') and curr == 'PW':
        K[x][y] = prev
    # any previous knowledge
    # --> E is stronger than other knowledge
    elif curr == 'E':
        K[x][y] = curr
    # BS is stronger than B or S, but weaker than E
    # and B or S is not in than same cell with W or P
    elif curr == 'BS':
        K[x][y] = curr
    # W and P can be in the same cell
    elif (prev,curr) == ('P','W') or (prev,curr) == ('W','P'):
        K[x][y] = 'E'
    # if previous knowledge is not B or S,
    # and current knowledge is B or S (based on wumpus or pit)
     
    elif curr in ('B','S'):
        if prev not in ('B','S'):
            K[x][y] = curr
        else:
            K[x][y] = 'BS'


# update knowledge for agent based on information of previous cell, current cell, current signal, and visited times of cells
'''
input:
    x_prev,y_prev   - previous position of agent
    x_curr,y_curr   - current position of agent
    val             - signal of current position of agent
    K               - knowledge of agent
    V               - matrix of visited times of cells
output:
    None (apply inference to update knowledge)
'''
def update_knowledge(x_prev,y_prev,x_curr,y_curr,val,K,V,M):
    
    # (0,0) is top left in python, but (0,0) is bottom left in game
    # up, down, left, right
    # vertical
    dx = [-1,1,0,0]
    # horizontal
    dy = [0,0,-1,1]

    # if M[x][y] has not reached, assign new knowledge about it and make predictions
    if V[x_curr][y_curr] == 0:
        # assign new value
        K[x_curr][y_curr] = val
        
        # make prediction for valid adjacent cells but not the cell of agent 
        for i in range(len(dx)):
            x,y = x_curr+dx[i],y_curr+dy[i]
            
            # make prediction with valid cells and not the previous cell of agent
            if (x,y) != (x_prev,y_prev) and valid_cell(x,y,M):
                
                # if a cell has not visited, information of it is just a prediction
                # else, apply first order logic to make inference and update the knowledge of that cell
                if V[x][y] == 0:
                    inference(x,y,signal_pairs[val],K)
                    
    # apply inference on non-empty cells and non-visited cells
    # elif V[x_curr][y_curr] == 0:
    #     inference(x_curr,y_curr,val,K)


# read from input file and build map
'''
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
    
    nG = 0
    nW = 0
    
    for row in rows:
        for cell in row:
            # count Wumpus
            if 'W' in cell:
                nW += 1
            # count gold
            elif 'G' in cell:
                nG += 1
            
    return rows,nW,nG

# write results to output file
'''
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
input:
    x,y - position of wumpus
    M   - map
output:
    update knowledge if wumpus is killed
    or return false if there is no wumpus at (x,y)
'''
def kill(x,y,K,M):
    # update information for cell M[x,y] as empty/safe room
    if M[x][y] == 'W':
        K[x][y] = 'E'
        inference(x,y,'E',K)
        return True
    
    return False
    
    
# transform map from top-left-rooted to bottom-left-rooted
'''
break into 2 steps = transpose + horizontal flip
'''
# def transform(M):
#     # M is a square matrix, size = 10
#     size = len(M)
#     # transpose
#     for i in range(size):
#         for j in range(i+1):
#             M[i][j],M[j][i] = M[j][i],M[i][j]
            
#     # horizontal flip
#     for i in range((size+1)/2):
#         for j in range(size):
#             M[i][j],M[size-i][j] = M[size-i][j],M[i][j]



# ========================================================================
# ranh roi

def check_out_of_gold():
    pass

def check_out_of_wumpus():
    pass

# ========================================================================



# input file & output file

def report(n_maps):
    
    for i in range(n_maps):
        
        inputFile = f'input/input{i}.txt'
        outputFile = f'output/output{i}.txt'
        parentDir = os.path.dirname(os.path.abspath(__file__))
        inputPath = os.path.join(parentDir, inputFile)
        outputPath = os.path.join(parentDir, outputFile)
        
        M,nW,nG = build_map(inputPath)

        state,iterations,nG,nW,score,actions,path,shoot_wumpus = FOLmodel(M,nG,nW)
        print(state,'\t\t',iterations,'\t\t',nG,'\t\t',nW,'\t\t',score)
        # write_ouput(path,score,outputPath)
        
               




# cnt_maps = 5

# report(cnt_maps)

inputFile = 'input/input0.txt'
outputFile = 'output/output0.txt'
parentDir = os.path.dirname(os.path.abspath(__file__))
inputPath = os.path.join(parentDir, inputFile)
outputPath = os.path.join(parentDir, outputFile)

M,nW,nG = build_map(inputPath)

state,iterations,nG,nW,score,actions,path,shoot_wumpus = FOLmodel(M,nG,nW)
print(state,'\t\t',iterations,'\t\t',nG,'\t',nW,'\t',score)