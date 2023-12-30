# from generate_map import *
from bfs import *
import heapq
import re
import os
import shutil

class FOL:
    def __init__(self, filename,outputFile):

        self.filename = filename
        self.outputFile = outputFile
        # record path, not include cells that agent shoots more than once
        self.path = []
        # record visited cells
        self.pos_list = []
        # instruction list
        '''
        action - forward, turn back, turn left, turn right, shoot (no move)
        encode - F,B,L,R,S
        '''
        self.actions = []
        # shoot lists
        self.shoot_wumpus = []
        # state of game - win, die, out, loop
        self.state = ''

        self.M = []
        self.nG = 0
        self.nW = 0
        
        # entrance - bottom left
        self.start_pos = None
        # exit - bottom left
        self.exit_pos = None
        # initial direction
        self.direction = None
        # get score and scores_list for game visualization        
        self.scores_list = []
        # init score
        self.score = 0
        # record current position in while loop
        self.curr_pos = None

        # init knowledge and visited matrix
        self.K = []
        self.V = []

        # self ghep code huong
        # huong va ban
        self.cuong = []
        


    # FOL model
    '''
    input:
        map M
        number of golds nG
        number of wumpus nW
    output:
        state of game, number of iterations, left golds, left wumpuses, score, instruction list, path, shoot_wumpus list
    '''
    def FOLmodel(self):
        
        # read map from input file
        self.build_map()
        
        # init game
        # entrance - bottom left
        self.start_pos = len(self.M)-1,0
        # exit - bottom left
        self.exit_pos = len(self.M)-1,0
        # initial direction
        self.direction = 'R'
        # get score and scores_list for game visualization        
        self.scores_list = []
        # init score
        self.score = 0
        # record current position in while loop
        self.curr_pos = self.start_pos

        
        x,y = self.curr_pos
        
        # knowledge: list of signals
        self.K = [[set() for _ in range(len(row))] for row in self.M]
        # track visiting times
        self.V = [[0 for _ in range(len(row))] for row in self.M]
        
        # empty and safe room
        self.K[x][y].update(['A','V'])
        self.V[x][y] = 1
        
        k = 1000
        iterations = 0
        
        # run until win or die or out
        while True:
            iterations += 1
            
            # k -= 1
            # use for report
            if iterations >= k:
                iterations -= 1
                break
                
            x,y = self.curr_pos    
            
            signal = self.M[x][y]
            
            # skip visited cells
            if 'V' not in self.K[x][y]:
                
                # update signal of unvisited cells
                self.K[x][y].update(signal)
                # stupid defined logic leads this shit code
                self.remove_conflict(x,y)
                # check dead case: W or P in signals
                if 'W' in self.K[x][y]:
                    # if W or P in current cell, dead
                    self.state = 'die'
                    self.score -= 10000
                    self.scores_list.append(self.score)
                    self.cuong.append('Wumpus')
                    # return results()
                    # return
                
                elif 'P' in self.K[x][y]:
                    # if W or P in current cell, dead
                    self.state = 'die'
                    self.score -= 10000
                    self.scores_list.append(self.score)
                    self.cuong.append('Pit')
                    # return results()
                    # return
                
                # if agent is still alive and game is still running
                
                # regardless of knowledge, update knowledge with new information
                elif 'G' in self.K[x][y]:
                    self.cuong.append('G')
                    # if map is out of gold, no action
                    self.nG = max(self.nG-1,0)
                    self.K[x][y].remove('G')
                    # gold is not in same room with wumpus or pit
                    self.K[x][y].update(['-P','-W'])

                # process signals of current cell for adjacent cells
                self.update_kb(self.K[x][y],x,y)
                # update current cell as visited
                self.K[x][y].update(['V'])
                '''
                debug
                '''
                # self.write_knowledge(f'./results/knowledge/csv/knowledge{self.iterations}.csv')

                if self.state == 'die':
                    return
            
            # record visited times of cells
            # if last action was shooting, no increase
            if len(self.actions) > 0 and self.actions[-1] != 'S': # or == 'F'
                self.V[x][y] += 1
            # print(K)
            
            
            # check state of agent
            # get all golds and kill all wumpuses
            if self.nG == 0 and self.nW == 0:
                self.state = 'win'
                self.cuong.append('win')
                # return self.results()
                return
            
            # check loop case
            if self.loop() == True:
                # print('iterations =',iterations)
                # print('loop here:',self.curr_pos)
                self.state = 'out'
                out_path = bfs(self.M,self.curr_pos,self.exit_pos)
                out_path = out_path[1:]
                # print('out_path:',out_path)

                for pos in out_path:
                    # get new rotation and direction
                    rotation,self.direction = self.rotate(self.curr_pos[0],self.curr_pos[1],pos[0],pos[1])
                    self.actions.append(rotation)
                    self.actions.append(self.direction)
                    
                    # cuong.append(rotation)
                    self.cuong.append(self.direction)
                    self.cuong.append('F')
                    
                    self.pos_list.append(pos)
                    if self.path == [] or pos != self.path[-1]:
                        self.path.append(pos)
                    
                    self.score -= 10
                    self.scores_list.append(self.score)
                    
                    iterations += 1
                    
                    # update current position
                    self.curr_pos = pos
                
                # climb out 
                self.cuong.append('out')
                return
            
            # make next action: shoot or move
            (rotation,new_direction),action = self.new_action(x,y)
            
            # if game is still running, update action
            self.actions.append(rotation)
            self.actions.append(action)
            # update new direction
            self.direction = new_direction
            # code cuong
            self.cuong.append(self.direction)
            self.cuong.append(action)
            
            # if agent shoots, preserve old direction and shoot
            if action == 'S':
                new_pos = self.new_move(x,y)
                if self.kill_wumpus(new_pos[0],new_pos[1]) == True:
                    self.nW = max(self.nW-1,0)
                    self.cuong.append('K')
                # record shooting positions
                self.shoot_wumpus.append(new_pos)
                # update score after shooting
                self.score -= 100
                self.scores_list.append(self.score)
                
            # if agent moves, get new direction and make move
            if action == 'F':
                # if moving but not shooting
                self.curr_pos = self.new_move(x,y)


                # self.actions.append(rotation)
                # self.actions.append(action)
                # self.direction = new_direction

                # self.cuong.append(self.direction)
                # self.cuong.append(action)
                
                self.score -= 10
                self.scores_list.append(self.score)
            
            # update path and record visited cells
            self.pos_list.append(self.curr_pos)
        
            if self.path == [] or self.path[-1] != self.curr_pos:
                self.path.append(self.curr_pos)

            
        # if game cannot end in 100 iterations, it is a loop 
        self.state = 'loop'
        # return self.results()
        return


    '''
    remove confict signals
    input:
        pair of conflict signals
        K   - knowledge
        x,y - position of cell
    ouput:
        remove - positive signal
    '''
    def helper(self,a,b,x,y):
        a_exists = a in self.K[x][y]
        b_exists = b in self.K[x][y]
        
        if a_exists and b_exists:
            self.K[x][y].remove(a)


    def remove_conflict(self,x,y):
        a_list = ['S','B','W','P']
        b_list = ['-S','-B','-W','-P']
        
        for a,b in zip(a_list,b_list):
            self.helper(a,b,x,y)
        
            
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
    def update_kb(self,sig_list,x,y):
        
        if 'A' in sig_list or '-' in sig_list:
            # sig_list.clear()
            self.K[x][y].update(['-P','-W','-S','-B'])
            if '-' in sig_list:
                self.K[x][y].remove('-')
                
        # update signals for current cell
        if 'S' not in self.K[x][y]:
            self.K[x][y].update(['-S'])
        if 'B' not in self.K[x][y]:
            self.K[x][y].update(['-B'])
        if 'W' in self.K[x][y]:
            self.K[x][y].update(['-P','-B','-S'])
        if 'P' in self.K[x][y]:
            self.K[x][y].update(['-W','-B','-S'])

        # process confictions
        self.remove_conflict(x,y)
        
        # neighbors of current cell
        neighbors = self.get_neighbors(x,y)
        
        # order of processing signals
        for s in self.K[x][y]:
            # skip 'V' signal and non-valuable signals (-W,-P)
            if s in ('V','-W','-P'):
                continue
            # update knowledge of univisted neighbors
            
            for n in neighbors:
                nX,nY = n
                if 'V' not in self.K[nX][nY]:
                    # adjacent cells of A are not wumpus or pit
                    if s == 'A' or s == 'G':
                        self.K[nX][nY].update(['-P','-W'])
                    # adjacent cells of B are P
                    elif s == 'B':
                        self.K[nX][nY].update(['P'])
                    # adjacent cells of S are W
                    elif s == 'S':
                        self.K[nX][nY].update(['W'])
                    # adjacent cells of P are B
                    elif s == 'P':
                        self.K[nX][nY].update(['B'])
                    # adjacent cells of W are S
                    elif s == 'W':
                        self.K[nX][nY].update(['S'])
                    # adjacent cells of -B are -P, remove P if possible
                    elif s == '-B':
                        if 'P' in self.K[nX][nY]:
                            self.K[nX][nY].remove('P')
                        self.K[nX][nY].update(['-P'])
                    # adjacent cells of -S are -W, remove W if possible
                    elif s == '-S':
                        if 'W' in self.K[nX][nY]:
                            self.K[nX][nY].remove('W')
                        self.K[nX][nY].update(['-W'])
                    
                    
        # post-process knowledge of adjacent cells of current cell
        # ignore all opposite signals
        for n in neighbors:
            nX,nY = n
            # if adjacent cells of current cell are not visited
            if 'V' not in self.K[nX][nY]:
                
                self.remove_conflict(nX,nY) 
                
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
    def new_action(self,x,y):
        # dir_priority = ['F','L','R','B']
        # 0,1,2,3
        
        list_actions = []
            
        neighbors = self.get_neighbors(x,y)
        
        # choose from neighbors
        for n in neighbors:
            nX,nY = n
            if(self.valid_cell(nX,nY)):
                rotation,new_direction = self.rotate(x,y,nX,nY)
                # forward
                if rotation == None:
                    # print(self.K[nX][nY])
                    a = 'P' not in self.K[nX][nY]
                    b = 'W' not in self.K[nX][nY]
                    # print(a and b)
                    c = a and b
                    # ({'P'} not in self.K[nX][nY]) and ({'W'} not in self.K[nX][nY])
                    if c == True:
                        # return rotate(direction,x,y,forward_cell[0],forward_cell[1]),'F'
                        list_actions.append((0,self.V[nX][nY],(rotation,new_direction),'F'))
                    elif a == True and b == False:
                        list_actions.append((0,self.V[nX][nY],(rotation,new_direction),'S'))
                # left
                elif rotation == 'L':
                    if 'P' not in self.K[nX][nY]:
                        # if maybe 'W', no move, just
                        if 'W' in self.K[nX][nY]:
                            # return rotate(direction,x,y,left_cell[0],left_cell[1]),'S'
                            list_actions.append((1,self.V[nX][nY],(rotation,new_direction),'S'))
                        else:
                            # return rotate(direction,x,y,left_cell[0],left_cell[1]),'F'
                            list_actions.append((1,self.V[nX][nY],(rotation,new_direction),'F'))
                # right
                elif rotation == 'R':
                    if 'P' not in self.K[nX][nY]:
                        # if maybe 'W', no move, just
                        if 'W' in self.K[nX][nY]:
                            # return rotate(direction,x,y,right_cell[0],right_cell[1]),'S'
                            list_actions.append((2,self.V[nX][nY],(rotation,new_direction),'S'))
                        else:
                            # return rotate(direction,x,y,right_cell[0],right_cell[1]),'F'
                            list_actions.append((2,self.V[nX][nY],(rotation,new_direction),'F'))
                # backward
                elif rotation == 'B':
                    # return rotate(direction,x,y,backward_cell[0],backward_cell[1]),'F'
                    list_actions.append((3,self.V[nX][nY],(rotation,new_direction),'F'))
        
        # sort list of actions based on priority
        list_actions.sort(key=lambda x: (x[1],x[0]))
        
        return list_actions[0][2],list_actions[0][3]


    '''
    new move base on direction
    '''
    def new_move(self,x,y):
        # up, down, left, right
        # vertical
        dx = [-1,1,0,0]
        # horizontal
        dy = [0,0,-1,1]
        
        nX,nY = x,y
        if self.direction == 'U':
            nX += dx[0]
        elif self.direction == 'D':
            nX += dx[1]
        elif self.direction == 'L':
            nY += dy[2]
        elif self.direction == 'R':
            nY += dy[3]
        
        return (nX,nY) if self.valid_cell(nX,nY) else None


    '''
    get valid neighbors of current cell
    input:
        x,y - position of current cell
        M   - map of game
    output:
        a list of valid neighbors of current cell
    '''
    def get_neighbors(self,x,y):
        # (0,0) is top left in python, but (0,0) is bottom left in game
        # up, down, left, right
        # vertical
        dx = [-1,1,0,0]
        # horizontal
        dy = [0,0,-1,1]
        
        res = []
        
        for i in range(len(dx)):
            new_x,new_y = x+dx[i],y+dy[i]
            if self.valid_cell(new_x,new_y):
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
    def valid_cell(self,x,y):
        return x >= 0 and x < len(self.M) and y >= 0 and y < len(self.M[0])


    '''
    read from input file and build map
    input:
        filename - path to input file
    output:
        M   - map of game
        nG  - number of golds
        nW  - number of wumpuses
    '''
    def build_map(self):
        rows = []
        
        with open(self.filename,'r') as f:
            lines = f.readlines()
            # get size of map --> map: sz x sz
            # sz = int(lines[0])
            # get value for cells, remove escape character '\n'
            rows = [[(cell[:-1] if cell.endswith('\n') else cell) for cell in line.split('.')] for line in lines[1:]]


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
                
        # return m,nW,nG
        self.nG = nG
        self.nW = nW
        self.M = m

        self.G_init = self.nG
        self.W_init = self.nW

    '''
    write results to output file
    input:
        path,score
    output:
        file at path '../output.txt'
    '''
    def write_ouput(self):
        with open(self.outputFile,'w') as f:
            for pos in self.path:    
                f.write(f"({pos[0]},{pos[1]})\n")
            f.write(str(self.score))
            

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
    def rotate(self,x,y,x_next,y_next):
        
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
            
        id_dir = dirs.index(self.direction)
        
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
    def kill_wumpus(self,x,y):
        result = False
        if 'W' in self.M[x][y]:
            result = True
        
        # if wumpus is in this cell, kill it and set as '-W'
        # if wumpus is not in this cell, set as '-W'
        self.K[x][y].update(['-W'])
        self.update_kb(self.K[x][y],x,y)
        return result
    
    '''
    agent proactively wants to out game
    input:
        # desired state - default None if agent detect loop case, or 'out'
        curr - current position of agent
        M - map of game
        exit_pos - 
    output:
        a path two out game and neccessary information
        (path finding algorithm: breadth-first-search)
    '''
    def out_game(self):
        path = bfs2(self.M,self.curr_pos,self.exit_pos)
        pass

    '''
    detect loop case

    if all of visited cells (more than once) are in list of visited positions of agent
    and there is no extra cell, agent is in loop case

    input:
        V - visited times matrix
        pos_list - list of visited positions
    ouput:
        loop or not
    '''

    def loop(self):

        if(len(self.pos_list) == 0):
            return False
        
        visited_set = set()
        for x in range(0,len(self.V)):
            for y in range(0,len(self.V[0])):
                if self.V[x][y] > 1:
                    visited_set.update([(x,y)])
                    
        pos_set = set()
        for pos in self.pos_list:
            pos_set.update([pos])
            
        l1 = sorted(list(pos_set))
        l2 = sorted(list(visited_set))
            
        return l1 == l2          

    '''
    tricky loop detection
    if current cell has visited times bigger than its neighbors do
    and its neighbors are also visited at least once

    ==> this is loop case

    input:
        V - visited times matrix
        x,y - position of current cell
        M - map of game
    output:
        loop or not
    '''    

    def tricky_loop(self,x,y):
        # neighbors of current cell
        neighbors = self.get_neighbors(x,y)
        
        # if current cell has visited times bigger than its neighbors do
        # and its neighbors are also visited at least once
        for n in neighbors:
            nX,nY = n
            if self.V[x][y] <= self.V[nX][nY] or self.V[nX][nY] <= 1:
                return False
            
        return True


    def results(self):
        return self.state,self.G_init,self.W_init,self.score,self.actions,self.path,self.pos_list,self.shoot_wumpus,self.cuong
        
            # print('knowledge:',K)
            # print("Visited times:",V)      
            # print('path:',path)
            # print('score:',score)
            # print('left wumpuses:',nW)
            # print('left golds:',nG)
            # print('instruction: ',actions)
            # print("number of iterations: ",100-k)
            
os.chdir(os.path.dirname(os.path.abspath(__file__)))
inputFile = '../Input/map3.txt'
outputFile = '../Output/output0.txt'
parentDir = os.path.dirname(os.path.abspath(__file__))
inputPath = os.path.join(parentDir, inputFile)
outputPath = os.path.join(parentDir, outputFile)

obj = FOL(inputFile,outputFile)
obj.FOLmodel()
# obj.write_ouput()
print(obj.results()[0])
