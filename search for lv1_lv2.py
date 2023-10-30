def AStar(matrix,start):
    start = tuple(start)
    goal = tuple(find_food(map))
     # Using a queue: (total_cost, current, score)
    queue = [(0, start, 0)] 
    visited = set()
    came_from = {}
    """
    Node in frontier->node(food)->path
    Node in frontier->visit-> update path
    """
    while queue:
        # don't need first value
        _, current, score = queue.pop(0)

        if current == goal:
            return reconstruct_path(came_from, current)

        if current not in visited:
            visited.add(current)
            for node in get_node(current, map):
                if node not in visited:
                    total_cost = 1 + heuristic(node, goal)
                    came_from[node] = current
                    queue.append((total_cost, node, score - 1))
        queue.sort(
            key=lambda x: x[2], reverse=True
        )  # Sort based on score

    return []





def get_node(pos,map):
    """
        - create node neighbors
        - if node isn't wall and in map -> add to node list
    """
    node=[]
    # up down left right
    directions=[(0,-1),(0,1),(-1,0),(1,0)]
    for i,j in directions:
        x, y = pos[0] + i, pos[1] + j
        if (
            0 <= x < len(map)
            and 0 <= y < len(map[0])
            and (map[x][y] == 0 or map[x][y] == 2)
        ):
            node.append((x, y))

    return node
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))


def find_food(matrix): 
    for i in range(len(matrix)):    
        for j in range(len(matrix[0])):
            # if food in matrix=2
            if matrix[i][j]==2:
                return(i,j)






def heuristic(node, goal):# distance
     return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5






def run_lv1_lv2(matrix, start):
    return AStar(matrix,start)
