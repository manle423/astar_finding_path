from heapq import heappop, heappush
from .utils import heuristic, insideThePolygon, adj

def greedy(grid, start, goal):
    closedList = []
    prev = {}
    fValue = {start:heuristic(start, goal)} # f = h
    openList = [((fValue[start], start))]

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
            fValueNeighbor = heuristic(neighbor, goal)  # f = h      
            if grid[neighbor[1],neighbor[0]] != 0: # kiểm tra trường hợp đụng phải chướng ngại vật
                continue
            
            if (neighbor[0] != current[0]) and (neighbor[1] != current[1]): # trường hợp nó nằm trên đường chéo
                if insideThePolygon(neighbor, current, grid): # kiểm tra xem điểm này có nằm trong đa giác hay chưa
                    continue
            
            #Nếu nằm trong tập đóng hoặc đang mở thì bỏ qua
            if (neighbor in closedList) or (neighbor in [item[1] for item in openList]):
                continue

            fValue[neighbor] = fValueNeighbor
            prev[neighbor] = current
            heappush(openList, (fValue[neighbor], neighbor))
    
    return False

