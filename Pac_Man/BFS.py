# best first search implemnetation
import heapq
import math

def bfs(matrix, start, goal):

    # get matrix size
    rows = len(matrix)
    cols = len(matrix[0])

    # check valid cell for pacman, ignore walls or out of map
    def valid_position(row, col):
        return 0 <= row < rows and 0 <= col < cols and matrix[row][col] not in (1, 3)
    
    # choose heuristic h(n) as f(n)
    def cal_heuristic(cell):
        return math.sqrt((cell[0]-goal[0])**2+(cell[1]-goal[1])**2)

    # store expaned cells with corresponding heuristic values in ascending order
    explored_set = []
    # add start first
    heapq.heappush(explored_set, (cal_heuristic(start), start))

    # track cell is visited or not
    visited = [[False] * cols for _ in range(rows)]

    # restore corresponding parents for path reconstruction
    came_from = [[None] * cols for _ in range(rows)]

    # recontruct path as result of bfs
    def reconstruct_path():
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current[0]][current[1]]

        path.append(start)
        path.reverse()
        return path

    # run the algorithm while explored set is not empty
    while explored_set:
        # pop the cell with the lowest cost to goal
        current_cell = heapq.heappop(explored_set)[1]

        # return path if this current cell is goal
        if (current_cell == goal):
            return reconstruct_path()

        # if current cell is not goal, mark it as visited
        # expand its neighbors and add valid neighbors into explored_set
        row, col = current_cell

        visited[row][col] = True

        neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor

            if valid_position(n_row, n_col) and not visited[n_row][n_col]:
                # add neighbor with its heuristic value
                heapq.heappush(
                    explored_set, (cal_heuristic(neighbor), neighbor))
                # track neighbor parent
                came_from[n_row][n_col] = current_cell

    # return None if can not found path or got any error
    return None
