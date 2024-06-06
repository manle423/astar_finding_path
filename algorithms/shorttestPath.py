from heapq import heappop, heappush
from .astar import astar
from .utils import costOfPath, heuristic, costOfPath1

###########################################################################################################
# shorttestPath algorithm (tổng chi phí đi qua các điểm đón và về đích là nhỏ nhất)
# áp dụng thuật toán astar cho mỗi lần tìm đường (đi đến điểm đón có chi phí nhỏ nhất đối với điểm đang xét)
# pickupPoint là danh sách các điểm đón
# Hàm trả về tổng chi phí và lộ trình
def shorttestPath(grid, start, goal, pickupPoint, log=None):
    visited = [] #Danh sách các điểm đón đã đi qua
    finalPath = [] #Đường đi của bài toán
    newStart = start 
    length = len(pickupPoint)
    sumCost = 0 #Tổng chi phí
    
    while(length > 0):
        routes = {} #Đường đi ngắn nhất từ điểm đang xét đến các điểm đón chưa đi qua
        pq = [] # Dùng priority queue để lưu điểm đón và chi phí từ điểm đang xét đến nó
        
        for point in pickupPoint:
            if point not in visited:
                path = astar(grid, newStart, point, log=log)  # đương đi ngắn nhất từ điểm đang xét đến nó
                if path == False: #Không tìm thấy đường đi
                    return (-1, False) 
                routes[point] = path
                heappush(pq, (costOfPath1(path), point) )
                
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
    if path == False:
        return (-1, False)
    sumCost += costOfPath1(path)
    finalPath += path

    # Ghi log
    if log:
        log(f"Tìm thấy đường đi từ {newStart} đến {goal}: {path}")
        log(f"Tổng chi phí: {sumCost}")
        log(f"Lộ trình cuối cùng: {finalPath}")
        
    #Trả về tổng chi phí và lộ trình
    return (sumCost, finalPath)