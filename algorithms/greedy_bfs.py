from heapq import heappop, heappush
from .utils import heuristic, distance, adj

def greedy_bfs(grid, start, goal, log=None):
    closedList = set()
    openList = [(heuristic(start, goal), start)]
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

            if neighbor not in [item[1] for item in openList]:
                prev[neighbor] = current
                heappush(openList, (heuristic(neighbor, goal), neighbor))
                if log:
                    log(f"Đã thêm điểm lân cận {neighbor} vào hàng đợi mở với heuristic {heuristic(neighbor, goal)}")

    if log:
        log("Không tìm thấy đường đi")
    return False
