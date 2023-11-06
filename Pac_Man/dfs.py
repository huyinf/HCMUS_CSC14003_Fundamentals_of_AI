'''
depth first search algorithm
'''

def dfs(matrix,start,goal):

    # get map size
    rows = len(matrix)
    cols = len(matrix[0])

    # check valid position for pacman
    def valid_position(node):
        return 0<=node[0]<rows and 0<=node[1]<cols and matrix[node[0]][node[1]] not in (1,3)
    
    # use a stack for frontier
    frontier = []
    frontier.append(start)

    # track visited cells
    visited = [[False]*cols for _ in range(rows)]
    # mark start as visited
    visited[start[0]][start[1]] = True

    # track corresponding parent of nodes
    parents = [[None]*cols for _ in range(rows)]

    # while stack is not empty
    while frontier:

        # get the top of stack
        current_node = frontier.pop()

        # if current node is goal, reconstruct and return path
        if current_node == goal:
            path = []
            while current_node != start:
                path.append(current_node)
                current_node = parents[current_node[0]][current_node[1]]

            path.append(start)
            path.reverse()
            return path
        
        # if current node is not goal, iterate it neighbors
        row,col = current_node
        neighbors = [(row+1,col),(row-1,col),(row,col+1),(row,col-1)]

        for neighbor in neighbors:
            
            # if neighbor is in valid cell and not visited
            # mark it as visited, push into stack
            # restore it parent as current node
            if valid_position(neighbor):
                n_row,n_col = neighbor
                if visited[n_row][n_col] == False:
                    visited[n_row][n_col] = True
                    frontier.append(neighbor)
                    parents[n_row][n_col] = current_node

    # return None if there is no found path
    return None
