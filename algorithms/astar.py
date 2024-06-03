from heapq import heappop, heappush
from .utils import heuristic, distance, insideThePolygon, adj

def astar(grid, start, goal):
    closedList = []  # Closed set
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
            return route[::-1]  # Return reversed path

        if current in closedList:
            continue
        closedList.append(current)

        for i, j in adj:
            neighbor = current[0] + i, current[1] + j  # Neighboring node

            if neighbor in closedList:
                continue

            gValueNeighbor = gValue[current] + distance(current, neighbor)  # Cost to neighbor

            if grid[neighbor[1], neighbor[0]] == 1:  # Check for wall
                continue

            if (neighbor[0] != current[0]) and (neighbor[1] != current[1]):  # Diagonal move
                if insideThePolygon(neighbor, current, grid):
                    continue

            if (neighbor not in [item[1] for item in openList]) or (gValueNeighbor < gValue.get(neighbor, 0)):
                gValue[neighbor] = gValueNeighbor
                fValue[neighbor] = gValueNeighbor + heuristic(neighbor, goal)  # Update f-value
                prev[neighbor] = current
                heappush(openList, (fValue[neighbor], neighbor))
                
    return False