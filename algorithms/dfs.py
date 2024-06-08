import numpy as np
from .utils import heuristic, distance, adj

def dfs(grid, start, goal, log=None):
    stack = [start]
    prev = {}
    visited = set([start])

    while stack:
        current = stack.pop()
        if current == goal:
            route = []
            while current in prev:
                route.append(current)
                current = prev[current]
            route.append(start)
            if log:
                log(f"Đường đi tìm thấy: {route[::-1]}")
            return route[::-1]

        if log:
            log(f"Đang xem xét {current}")
        
        for i, j in adj:
            neighbor = current[0] + i, current[1] + j

            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= grid.shape[1] or
                grid[neighbor[0], neighbor[1]] == 1 or
                neighbor in visited):
                continue

            stack.append(neighbor)
            visited.add(neighbor)
            prev[neighbor] = current
            if log:
                log(f"Đã thêm điểm lân cận {neighbor} vào ngăn xếp")

    if log:
        log("Không tìm thấy đường đi")
    return False
