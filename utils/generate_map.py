import random
import os
import re

'''
setting for easy game:
    adjacent rooms of first room of agent are wumpus or pit

    room for wumpus and for pit are not adjacent
    
'''
parentDir = os.path.dirname(os.path.abspath(__file__))
inputPath = os.path.join(parentDir,"input")
# default parameters
size = 10
nW = 4
nP = 3
nG = 9
cnt = 5

# object_adjObj pairs
pairs = {'W':'S','P':'B','G':None}

# unique objects not in the same room with others
uniques = ['W','P','A']

not_adjacent_pairs = {'W':['P','A'],
                      'P':['W','A'],
                      }

# helper function to ignore adjacent cases
def not_adjacent(object,x,y,M):
    
    if object == "G":
        return True
    
    # up, down, left, right, up-left, up-right, down-left, down-right
    dx = [-1,1,0,0,-1,-1,1,1]
    dy = [0,0,-1,1,-1,1,-1,1]
    
    for i in range(8):
        nX = x+dx[i]
        nY = y+dy[i]
        if valid_cell(nX,nY,M):
            if M[nX][nY] not in not_adjacent_pairs[object]:
                return True
            
    return False
    

# check cell is inside map
def valid_cell(x:int,y:int,m:list[list[str]]):
    return 0 <= x < len(m) and 0 <= y < len(m[0])

# random location for objects
'''
input:
    cnt: number of objects
    object: object type
    m: map
output:
    m: map with objects
'''
def random_objects(cnt: int,object: str, m: list[list[str]]):
    
    row = len(m)
    col = len(m[0])
    
    # up, down, left, right
    dx = [-1,1,0,0]
    dy = [0,0,-1,1]
    
    for i in range(cnt):
        x = random.randint(0,row-1)
        y = random.randint(0,col-1)
        while m[x][y] != "-" and m[x][y] in uniques and not_adjacent(object,x,y,m) == False:
            x = random.randint(0,row-1)
            y = random.randint(0,col-1)
        
        if object == "G":
            if m[x][y] == "-":
                m[x][y] = object
            elif re.search('B|S',m[x][y]):
                m[x][y] += object
            # continue
        else:
            m[x][y] = object
            
            for j in range(4):
                nX = x+dx[j]
                nY = y+dy[j]
                if valid_cell(nX,nY,m):
                    if m[nX][nY] == "-":
                        m[nX][nY] = pairs[object]
                    elif m[nX][nY] not in uniques:
                        m[nX][nY] += pairs[object]

# post-process map after randoming objects
'''
input:
    m: map
output:
    m: map after post-processing with cells are sorted and duplicated characters are removed
'''
def post_process(m:list[list[str]]):
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] not in uniques and m[i][j] != "-":
                # remove duplicated characters
                m[i][j] = ''.join(sorted(set(m[i][j]),key=m[i][j].index))
                # sort characters
                m[i][j] = ''.join(sorted(m[i][j]))
                
     
def print_map(M):
    
    for row in M:
        for cell in row:
            print(cell,end="\t")
        print("\n")
   

def map_to_file(M,filename):
    
    with open(filename,"w") as f:
        f.write(str(size)+'\n')
        for row in M:
            line = ".".join(row)
            f.write(line+'\n')

# generate maps
'''
input:
    size: size of map
    nW: number of wumpus
    nP: number of pit
    nG: number of gold
    cnt_maps: number of maps
output:
    desired files
'''
def generate_maps(size:int = size,nW:int = nW,nP:int = nP,nG:int = nG,cnt_maps:int = cnt):
    
    for i in range(cnt_maps):
        m = [["-" for _ in range(size)] for _ in range(size)]
        m[-1][0] = "A"
        # random wumpus
        random_objects(nW,"W",m)
        # random pit
        random_objects(nP,"P",m)
        # random gold
        random_objects(nG,"G",m)
        # post-process
        post_process(m)
        
        filePath = os.path.join(inputPath,"input"+str(i)+".txt")
        # write map to file
        map_to_file(m,filePath)


# # sample run
generate_maps(size,nW,nP,nG,cnt)