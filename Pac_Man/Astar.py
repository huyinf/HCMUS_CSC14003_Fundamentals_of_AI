import heapq
import math

def Astar(map,start,goal):

    open_set = []
    close_set = set()

    # restore parrent
    came_from = {}

    g_score = {start:0}
    f_score = {start:cal_heuristic(start,goal)}

    heapq.heappush(open_set,(f_score[start],start))

    while(open_set):

        # get the node has the lowest f_score
        current = heapq.heappop(open_set)[1]

        # if current is goal, find path and return
        if current == goal:
            path = []
            # reconstruct path using came_from array to get the corresponding parrent
            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()
            return path
        
        # if current is not goal, push it into close_set
        close_set.add(current)

        # iterate possible neighbors of current node
        neighbors = get_neighbors(current,map)

        for node in neighbors:
            tentative_g_score = g_score[current] + 1

            # if node is already in close set and new g_score is not less than previous g_score, skip this node
            if node in close_set and tentative_g_score >= g_score.get(node,float('inf')):
                continue

            # if current g_score is less than the previous g_score
            # update parent for this node
            # update g_score,f_score
            if tentative_g_score < g_score.get(node,float('inf')):
                came_from[node] = current
                g_score[node] = tentative_g_score
                f_score[node] = g_score[node] + cal_heuristic(node,goal)
                # if current node is not in close set, push it into open set
                if node not in close_set:
                    heapq.heappush(open_set,(f_score[node],node))

    # if there is no found path
    return None

def get_neighbors(node, adjacency_matrix):
    rows = len(adjacency_matrix)
    cols = len(adjacency_matrix[0])
    
    x, y = node
    neighbors = []

    # left
    if x > 0 and adjacency_matrix[x-1][y] != 1:
        neighbors.append((x-1, y))
    # right
    if x < rows-1 and adjacency_matrix[x+1][y] != 1:
        neighbors.append((x+1, y))
    # down
    if y > 0 and adjacency_matrix[x][y-1] != 1:
        neighbors.append((x, y-1))
    # up
    if y < cols-1 and adjacency_matrix[x][y+1] != 1:
        neighbors.append((x, y+1))

    return neighbors

# ecludian distance
def cal_heuristic(node, dest):
    return math.sqrt((node[0] - dest[0]) ** 2 + (node[1] - dest[1]) ** 2)
