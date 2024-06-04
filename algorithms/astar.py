from heapq import heappop, heappush
from .utils import heuristic, distance, insideThePolygon, adj

def astar(grid, start, goal):
    closedList = set()  # Closed set
    gValue = {start: 0}  # Cost from start to current node
    fValue = {start: heuristic(start, goal)}  # Estimated cost from start to goal through current node
    openList = [(fValue[start], start)]  # Priority queue of open nodes
    prev = {}  # To reconstruct the path

    while openList:
        current = heappop(openList)[1]  # Node with lowest f-value
        if current == goal:
            route = []
            while current in prev:
                route.append(current)
                current = prev[current]
            route.append(start)
            return route[::-1]  # Return reversed path

        closedList.add(current)

        for i, j in adj:
            neighbor = current[0] + i, current[1] + j  # Neighboring node

            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= grid.shape[1] or
                grid[neighbor[0], neighbor[1]] == 1 or
                neighbor in closedList):
                continue

            gValueNeighbor = gValue[current] + distance(current, neighbor)  # Cost to neighbor

            # if (neighbor[0] != current[0]) and (neighbor[1] != current[1]):  # Diagonal move
            #     if insideThePolygon(neighbor, current, grid):
            #         continue

            if (neighbor not in [item[1] for item in openList]) or (gValueNeighbor < gValue.get(neighbor, float('inf'))):
                gValue[neighbor] = gValueNeighbor
                fValue[neighbor] = gValueNeighbor + heuristic(neighbor, goal)  # Update f-value
                prev[neighbor] = current
                heappush(openList, (fValue[neighbor], neighbor))

    return False
