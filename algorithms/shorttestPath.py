from heapq import heappop, heappush
from .astar import astar
from .utils import costOfPath, heuristic

###########################################################################################################
# shorttestPath algorithm (tổng chi phí đi qua các điểm đón và về đích là nhỏ nhất)
# áp dụng thuật toán astar cho mỗi lần tìm đường (đi đến điểm đón có chi phí nhỏ nhất đối với điểm đang xét)
# pickupPoint là danh sách các điểm đón
# Hàm trả về tổng chi phí và lộ trình
def shorttestPath(grid, start, goal, pickupPoint):
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
                path = astar(grid, newStart, point)# đương đi ngắn nhất từ điểm đang xét đến nó
                if path == False: #Không tìm thấy đường đi
                    return (-1, False) 
                routes[point] = path
                # ở đây phải có 1 hàm tính chi phí đường đi
                heappush(pq, (costOfPath(path, newStart)-heuristic(point, goal), point) )
        cost, pickPoint = heappop(pq) #Cho ra điểm có chi phí nhỏ nhất
        sumCost += cost
        finalPath += routes[pickPoint]
        visited.append(pickPoint) #Đánh dấu là đã đi đến
        newStart = pickPoint
        length -= 1
    
    #Tìm lộ trình từ điểm đón cuối dùng đến đích
    path = astar(grid, newStart, goal)
    if path == False:
            return (-1, False)
    sumCost += costOfPath(path, newStart)
    finalPath += path

    #Trả về tổng chi phí và lộ trình
    return (sumCost, finalPath)
    
