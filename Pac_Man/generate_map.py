import random
import os

# level 1,2 --> 1 food, 0 ghosts
# level 3,4 --> nultiple foods, multiple ghosts
# level = 0


# define macro for object in pacman game
wall='1'
food='2'
ghost='3'
emptyPath='0'

map_dir = os.path.dirname(os.path.abspath(__file__))
print(map_dir)

def generate_map(level,map_count):

    # for level 1,2
    foods = 1
    # for level 1
    ghosts = 0

    for m in range(map_count):

        # get random size for map
        rows = random.randint(10,15)
        cols = random.randint(10,20)

        # calculate total of cells in map
        total_cells = rows*cols
        # set a boundary for map as full of walls
        bound_wall = rows*2 + cols*2 - 4

        # choose random number of walls inside map
        # choose "good" formula for upper_bound and lower_bound !!!
        inside_wall = random.randint(int(total_cells/5),int((total_cells-bound_wall)/2))

        # initalize zero map
        map = [['0' for _ in range(cols)] for _ in range(rows)]

        # set bound walls
        for i in range(rows):
            map[i][0] = wall
            map[i][-1] = wall

        for i in range(cols):
            map[0][i] = wall
            map[-1][i] = wall

        # set random inside walls
        for _ in range(inside_wall):
            # skip first and last row/column
            r = random.randint(1,rows-1)
            c = random.randint(1,cols-1)
            map[r][c] = wall

        # set random position for pacman
        # note ignore walls
        x = random.randint(1,rows-1)
        y = random.randint(1,cols-1)

        while map[x][y] == wall:
            x = random.randint(1,rows-1)
            y = random.randint(1,cols-1)


        # for future initialization of ghosts
        # in order to bad case for pacman
        # intialized ghost positions are not
        # around pacman at first
        PacmanNeighbor = []
        for i in (-1,0,1):
            for j in (-1,0,1):
                PacmanNeighbor.append((x+i,y+j))


        # store ghost positions
        ghostsPos = []
        if level > 1:           
            # set random of ghosts in map
            ghosts = random.randint(2,5)

            

            for _ in range(ghosts):
                r = 1
                c = 1
                # ignore walls and pacman
                while map[r][c] == wall or (r,c) in PacmanNeighbor:
                    r = random.randint(1,rows-1)
                    c = random.randint(1,cols-1)

                ghostsPos.append((r,c))


            for (r,c) in ghostsPos:
                map[r][c] = ghost


        if(level==1 or level ==2):
            r,c=1,1
            # igore ghosts, walls, pacman
            while (r,c) == (x,y) or (r,c) in ghostsPos or map[r][c] == wall:
                r = random.randint(1,rows-1)
                c = random.randint(1,cols-1)

            map[r][c] = food

        else:
            # set random number of foods in map
            foods = random.randint(min(int(total_cells/10),3),total_cells-bound_wall-inside_wall-ghosts-1)

            foodsPos = []

            for _ in range(foods):
                r,c=1,1
                # igore ghosts, walls, pacman
                while (r,c) == (x,y) or (r,c) in ghostsPos or map[r][c] == wall:
                    r = random.randint(1,rows-1)
                    c = random.randint(1,cols-1)
                
                foodsPos.append((r,c))

            for (r,c) in foodsPos:
                map[r][c] = food


        # create level folder if it is not existed
        level_path = os.path.join(map_dir,f"map/level-{level}")
        if not os.path.exists(level_path):
            os.makedirs(level_path)

        filename = f"map{m+1}.txt"

        # write file content
        with open(filename,'w') as file:
            file.write(str(rows)+" "+str(cols)+'\n')
            for row in map:
                file.write(''.join(row)+'\n')
            file.write(str(x) + ' ' + str(y) + '\n')
            
        print(f"{filename} has been writen!")

        # make file path
        file_path = os.path.join(level_path,filename)

        # remove existed file
        if os.path.exists(file_path):
            os.remove(file_path)

        # change created file to new path
        os.rename(filename,file_path)

    # print([total_cells,bound_wall,inside_wall,ghosts,foods])
    # return

# generate_map(4,5)


def mapConvert(filename: str) -> tuple[list[list[int]],tuple[int,int]]:

    rows , cols = 0,0
    matrix = []
    with open(filename,'r') as file:
        lines = file.readlines()
        
        rows,cols = map(int,lines[0].split())
        matrix = [[int(cell) for cell in line.split()] for line in lines[1:rows+1]]

        start = tuple(map(int,lines[rows+1].split()))

    return matrix,start


# return goal as a tuple
def findGoal(map: list[list[int]]) -> tuple[int,int]:
    # goal = 0,0

    rows = len(map)
    cols = len(map[0])
    for x in range(rows):
        for y in range(cols):
            if map[x][y] == 2:
                return (x,y)








    

