import heapq


signal_pairs = {'W':'S',
                'S':'W',
                'B':'P',
                'P':'B',
                'BS':'PW',
                }

# map
M = []
# knowledge
K = []
# track visiting times for optimization
V = []

# number of golds
nG = 0
# number of wumpus
nW = 0

# input file
filename = './input.txt'
    


# FOL model
'''
input:
    map M
    number of golds nG
    number of wumpus nW
output:
    path, score
'''
def FOLmodel(M,nG,nW):
    # knowledge
    K = [[None for _ in range(len(row))] for row in M]
    # track visiting times
    V = [[0 for _ in range(len(row))] for row in M]
    
    # entrance
    start_pos = (0,0)
    
    V[0][0] = 1
    
    # exit
    exit_pos = (len(M)-1,len(M[0])-1)

    # record visited cells
    path = list()
        
    # record list of keyboards of changing direction
    keys = []
    
    # get score and score_list for game visualization
    scores_list = []
    
    score = 0
    
    # record current and previous position in while loop
    prev_pos = start_pos
    curr_pos = start_pos
    
    def results():
        print('knowledge:',K)
        # print(V)      
        print('path:',path)
        print('list of keyboards: ',keys)
        # print(scores_list)
        print('score:',score)
        print('left wumpuses:',nW)
        print('left golds:',nG)
        
    
    # run until win or die
    k = 10
    while k >= 0:
        k -= 1

        # print('curr: ',curr_pos)
        
        path.append(curr_pos)
        scores_list.append(score)

        x_prev,y_prev = prev_pos        
        x,y = curr_pos
        signal = M[x][y]
        
        
        # get all golds and kill all wumpuses
        if nG == 0 and nW == 0:
            print('state: win')
            results()
            return path,score

        # caught by wumpus or fall in pit  
        if signal == 'W' or signal == 'P':
            update_knowledge(x_prev,y_prev,x,y,signal,K,V)
            score -= 10000
            print('state: die')
            results()
            return path,score

        # climb out of the cave
        if curr_pos == exit_pos:
            print('state: out')
            results()
            return path,score

        # if agent is still agent or game is still running
        if signal == 'B' or signal == 'S' or signal == 'BS':
            update_knowledge(x_prev,y_prev,x,y,signal,K,V)
            
            # get adjacent cells of current cell to find and kill wumpus if possible
            adj_cells = list_of_moves(x,y,M,V)
            
            for _,pos in adj_cells:
                nX,nY = pos
                # use knowledge to determine whether wumpus is in room
                if K[nX][nY] in ('W'):
                    
                    # decrease the number of wumpuses
                    nW -= 1
                    kill(nX,nY,K)
                    # shoot an arrow
                    score -= 100
                     
        # mark empty visited room is E as a safe room
        if signal == '-':
            K[x][y] = 'E'
        
        
        # random good moves
        moves = list_of_moves(x,y,M,V)

        # print(f'{k}: ',moves)
        
        # update previous position
        prev_pos = curr_pos
        
        # choose the "best" move
        curr_pos = move(moves,M)
        
        keys.append(rotate(prev_pos[0],prev_pos[1],curr_pos[0],curr_pos[1]))
        
        score -= 10
        
        # update visiting times
        x,y = curr_pos
        V[x][y] += 1
    
            


# get list of the next possible moves for agent
'''
input:
    x,y - position of cell
    M   - map of game
    V   - matrix of visited times
output:
    a list of possible moves ordered by visited times (min_heap) for agent
'''
def list_of_moves(x,y,M,V):
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
            heapq.heappush(moves,(V[new_x][new_y],(new_x,new_y)))
            
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
    backup = []
    
    # get the "best" cell
    # smallest visiting times
    # not Pit or Wumpus
    while len(list_moves) > 0:
        
        item = heapq.heappop(list_moves)
        
        pos = item[1]
        
        x,y = pos
        
        if M[x][y] not in ('P','W'):
            res = pos
            return res
        else:
            heapq.heappush(backup,item)
        
    # return any dead cell
    return heapq.heappop(backup)[1]
  
  
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
def inference(x,y,val,K):

    # get the predicted value of current cell
    # use the current value of current cell to make inference
    
    prev = K[x][y]
    curr = val
    
    if prev == curr:
        pass
    elif prev == None:
        K[x][y] = curr
    elif prev == 'PW' and curr in ('P','W'):
        K[x][y] = curr
    
    elif prev in ('P','W') and curr == 'PW':
        K[x][y] = prev
        
    elif prev in ('S','B','P','W') and curr in ('E','BS'):
        K[x][y] = curr
        
    elif (prev,curr) == ('P','W') or (prev,curr) == ('W','P'):
        K[x][y] = 'E'
        
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
def update_knowledge(x_prev,y_prev,x_curr,y_curr,val,K,V):
    
    # (0,0) is top left in python, but (0,0) is bottom left in game
    # up, down, left, right
    # vertical
    dx = [-1,1,0,0]
    # horizontal
    dy = [0,0,-1,1]

    # if M[x][y] has not reached, assign new knowledge about it and make predictions
    if K[x_curr][y_curr] is None:
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
                    
    # apply inference on non-empty cells
    else:
        inference(x_curr,y_curr,val,K)


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
        sz = int(lines[0])
        # get value for cells, remove escape character '\n'
        rows = [[(cell[:-1] if cell.endswith('\n') else cell) for cell in line.split('.')] for line in lines[1:sz+1]]
    
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
    file at path './output.txt'
'''

def write_ouput(path,score):
    
    
    with open('output.txt','w') as f:
        for pos in path:    
            f.write(f"({pos[0]},{pos[1]})\n")
        f.write(str(score))
        

# rotation
'''
input:
    dir - current direction of agent (???)
    x,y - current position of agent
    x_next,y_next - position of the disired move of agent
output:
    rotation to the desired direction for game logic
    
        A   -   turn left
        D   -   turn right
        W   -   none (forward)
        S   -   turn left(x2) (backward)
        
    note: map with keyboard (gamer definitely understand.)
'''
def rotate(x,y,x_next,y_next):
    
    if x_next < x:
        return 'W'
    if x_next > x:
        return 'S'
    if y_next < y:
        return 'A'
    if y_next > y:
        return 'D'


# kill wumpus
'''
input:
    x,y - position of wumpus
    K   - knowledge of agent
output:
    update knowledge
'''
def kill(x,y,K):
    # update information for cell M[x,y] as empty/safe room
    K[x][y] = 'E'
    inference(x,y,'E',K)
    
# ========================================================================
# ranh roi

def check_out_of_gold():
    pass

def check_out_of_wumpus():
    pass

# ========================================================================


M,nW,nG = build_map(filename)
# print('Map:',M)
res = FOLmodel(M,nG,nW)
path = res[0]
score = res[1]
# print(type(path))
write_ouput(path,score)