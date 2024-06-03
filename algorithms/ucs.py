from heapq import heappop, heappush
from .utils import distance, insideThePolygon, adj

def UCS(grid, start, goal):
    closedList = []
    gValue = {start: 0}
    openList = [(gValue[start], start)]
    prev = {}

    while openList:
        current = heappop(openList)[1]
        if current == goal:
            route = []
            while current in prev:
                route.append(current)
                current = prev[current]
            return route[::-1]

        if current in closedList:
            continue
        closedList.append(current)

        for i, j in adj:
            neighbor = current[0] + i, current[1] + j
            gValueNeighbor = gValue[current] + distance(current, neighbor)

            if grid[neighbor[1], neighbor[0]] == 1:
                continue

            if (neighbor[0] != current[0]) and (neighbor[1] != current[1]):
                if insideThePolygon(neighbor, current, grid):
                    continue

            if neighbor in closedList:
                continue

            if (neighbor not in [item[1] for item in openList]) or (gValueNeighbor < gValue.get(neighbor, 0)):
                gValue[neighbor] = gValueNeighbor
                prev[neighbor] = current
                heappush(openList, (gValue[neighbor], neighbor))
    
    return False