from heapq import heappop, heappush
from .utils import heuristic, distance, adj

def dijkstra(grid, start, goal, log=None):
    closedList = set()
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
            route.append(start)
            if log:
                log(f"Đường đi tìm thấy: {route[::-1]}")
            return route[::-1]

        closedList.add(current)
        if log:
            log(f"Thêm {current} vào danh sách đã được xem xét")
        
        for i, j in adj:
            neighbor = current[0] + i, current[1] + j

            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= grid.shape[1] or
                grid[neighbor[0], neighbor[1]] == 1 or
                neighbor in closedList):
                continue

            gValueNeighbor = gValue[current] + distance(current, neighbor)

            if (neighbor not in [item[1] for item in openList]) or (gValueNeighbor < gValue.get(neighbor, float('inf'))):
                gValue[neighbor] = gValueNeighbor
                prev[neighbor] = current
                heappush(openList, (gValue[neighbor], neighbor))
                if log:
                    log(f"Đã thêm điểm lân cận {neighbor} với giá trị g {gValue[neighbor]} vào hàng đợi mở")

    if log:
        log("Không tìm thấy đường đi")
    return False
