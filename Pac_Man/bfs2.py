'''
breadth-first search implementation
'''

import heapq

def bfs2(matrix,start,goal):

    # get map size
    rows = len(matrix)
    cols = len(matrix[0])

    # check valid position for pacman agent
    def valid_position(node):
        return 0<=node[0]<rows and 0<=node[1]<cols and matrix[node[0]][node[1]] not in (1,3)

    
    frontier = []
    frontier.append(start)

    # track visited cells
    visited = [[False]*cols for _ in range(rows)]
    visited[start[0]][start[1]] = True

    # track corresponding parent of cells
    parents = [[None]*cols for _ in range(rows)]

    # while frontier is not empty
    while frontier:

        # get the head of frontier
        current_node = frontier.pop(0)

        # if current node is goal, reconstruct and return path
        if current_node == goal:
            path = []
            while current_node != start:
                path.append(current_node)
                current_node = parents[current_node[0]][current_node[1]]

            path.append(start)
            path.reverse()
            return path
        
        # if current node is not goal
        # check its neighbors
        row,col = current_node
        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        
        for neighbor in neighbors:
            # if neighbor is a valid cell and not visited
            # mark it as visited and track its parent as current node
            # append it into frontier
            if valid_position(neighbor):
                n_row, n_col = neighbor

                if visited[n_row][n_col] == False:
                    visited[n_row][n_col] = True
                    parents[n_row][n_col] = current_node
                    frontier.append(neighbor)

    # return none if there is no found path
    return None
    

