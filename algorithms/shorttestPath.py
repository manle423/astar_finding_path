from heapq import heappop, heappush
from .astar import astar
from .bfs import bfs
from .dfs import dfs
from .dijkstra import dijkstra
from .greedy_bfs import greedy_bfs
from .utils import costOfPath

###########################################################################################################
# shorttestPath algorithm (tổng chi phí đi qua các điểm đón và về đích là nhỏ nhất)
# áp dụng thuật toán astar cho mỗi lần tìm đường (đi đến điểm đón có chi phí nhỏ nhất đối với điểm đang xét)
# pickupPoint là danh sách các điểm đón
# Hàm trả về tổng chi phí và lộ trình
def shorttestPath(grid, start, goal, pickupPoint, log=None):
    visited = [] # Danh sách các điểm đón đã đi qua
    finalPath = [] # Đường đi của bài toán
    newStart = start 
    length = len(pickupPoint)
    sumCost = 0 # Tổng chi phí
    
    while(length > 0):
        routes = {} # Đường đi ngắn nhất từ điểm đang xét đến các điểm đón chưa đi qua
        pq = [] # Dùng priority queue để lưu điểm đón và chi phí từ điểm đang xét đến nó
        
        for point in pickupPoint:
            if point not in visited:
                path = astar(grid, newStart, point, log=log)
                # path = bfs(grid, newStart, point, log=log)
                # path = dfs(grid, newStart, point, log=log)
                # path = greedy_bfs(grid, newStart, point, log=log)
                # path = dijkstra(grid, newStart, point, log=log)
                if path == False: #Không tìm thấy đường đi
                    return (-1, False) 
                routes[point] = path
                heappush(pq, (costOfPath(path), point))
                
                # Ghi log
                if log:
                    log(f"Tìm thấy đường đi từ {newStart} đến {point}: {path}")
                
        if not pq:
            return (-1, False)
        
        cost, pickPoint = heappop(pq) #Cho ra điểm có chi phí nhỏ nhất
        sumCost += cost
        finalPath += routes[pickPoint]
        visited.append(pickPoint) #Đánh dấu là đã đi đến
        newStart = pickPoint
        length -= 1
    
    #Tìm lộ trình từ điểm đón cuối dùng đến đích
    path = astar(grid, newStart, goal, log=log)
    # path = bfs(grid, newStart, goal, log=log)
    # path = dfs(grid, newStart, goal, log=log)
    # path = greedy_bfs(grid, newStart, goal, log=log)
    # path = dijkstra(grid, newStart, goal, log=log)
    if path == False:
        return (-1, False)
    sumCost += costOfPath(path)
    finalPath += path

    # Ghi log
    if log:
        log(f"Tìm thấy đường đi từ {newStart} đến {goal}: {path}")
        log(f"Tổng chi phí: {sumCost}")
        log(f"Lộ trình cuối cùng: {finalPath}")
        
    #Trả về tổng chi phí và lộ trình
    return (sumCost, finalPath)

