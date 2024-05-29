from heapq import heappop, heappush
from .utils import heuristic, distance, insideThePolygon, adj

def astar(grid, start, goal):
    closedList = [] #Tập đóng
    gValue = {start: 0} #Lưu giá trị g (khoảng cách tính từ đích):
    fValue = {start: heuristic(start, goal)} # f = g + h
    openList = [((fValue[start], start))] #Tập mở (dùng cấu trúc priority queue)
    prev = {} #Lưu điểm trước (dùng để truy vết)
    
    while openList:
        current = heappop(openList)[1] #Sử dụng priority queue để lấy ra điểm có f nhỏ nhất trong tập mở
        if current == goal: #Nếu tìm thấy đích (là trạng thái đích)
            route = []
            while current in prev:
                route.append(current)
                current = prev[current]
            return route[::-1] #Trả về lộ trình

        if current in closedList: #Nếu trong điểm đang xét trong tập đóng thì bỏ qua
            continue
        closedList.append(current) #Thêm vào tập đóng

        #Xét các điểm liền kề (các trạng thái tiếp theo)
        #Mở các đỉnh
        for i, j in adj:
            neighbor = current[0] + i, current[1] + j #Điểm liền kề (Trạng thái tiếp theo)

            if neighbor in closedList: #Nếu đã trong tập đóng thì bỏ qua
                continue

            gValueNeighbor = gValue[current] + distance(current, neighbor)  # gValue của điểm này
                           
            if grid[neighbor[1], neighbor[0]] != 0: # kiểm tra trường hợp đụng phải chướng ngại vật
                continue
            #kiểm tra xem nó sắp đi vào đa giác hay không
            if (neighbor[0] != current[0]) and (neighbor[1] != current[1]): # trường hợp nó nằm trên đường chéo
                if insideThePolygon(neighbor, current, grid):
                    continue
            
            #Nếu chưa trong tập mở hoặc đã trong tập mở mà có gValue tốt hơn thì cập nhật giá trị và thêm vào tập mở
            if  (neighbor not in [item[1] for item in openList]) or (gValueNeighbor < gValue.get(neighbor, 0)):
                gValue[neighbor] = gValueNeighbor
                fValue[neighbor] = gValueNeighbor + heuristic(neighbor, goal) # f = g + h
                prev[neighbor] = current
                heappush(openList, (fValue[neighbor], neighbor))
                
    return False

