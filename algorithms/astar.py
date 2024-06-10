from heapq import heappop, heappush
from .utils import heuristic, distance, adj

def astar(grid, start, goal, log=None):
    closedList = set()  # Tập hợp các điểm đã được xem xét
    gValue = {start: 0}  # Chi phí từ điểm bắt đầu đến điểm hiện tại
    fValue = {start: heuristic(start, goal)}  # Chi phí ước tính từ điểm bắt đầu đến đích thông qua điểm hiện tại
    openList = [(fValue[start], start)]  # Hàng đợi ưu tiên của các điểm cần xem xét
    prev = {}  # Để tái tạo lại đường đi

    # f = g + h
    
    # print(f"Khởi động A* từ {start} đến {goal}")

    # chạy vòng lặp đến khi openList còn điểm cần xem xét 
    while openList:
        # lấy điểm có giá trị f thấp nhất từ openList
        current = heappop(openList)[1]  # Điểm có giá trị f thấp nhất
        
        if current == goal:
            # tạo danh sách rỗng để chứa đường đi
            route = []
            
            # duyệt ngược từ điểm hiện tại về điểm bắt đầu 
            while current in prev:
                # thêm điểm hiện tại vào lộ trình
                route.append(current)
                
                # di chuyển đến điểm trước đó 
                current = prev[current]
            # thêm điểm bắt đầu vào lộ trình
            route.append(start)
            
            if log:
                log(f"Đường đi tìm thấy: {route[::-1]}")
            return route[::-1]  # Trả về đường đi đảo ngược

        
        if log:
            log(f"Thêm {current} vào closedList: {closedList}")
        # thêm điểm hiện tại vào danh sách đã được xem xét
        closedList.add(current)
        
        for i, j in adj:
            # Tính toán tọa độ của điểm lân cận (neighbor)
            neighbor = current[0] + i, current[1] + j

            # kiểm tra các điểm lân cận có hợp lệ hay không nếu không thì bỏ qua điểm này
            # Điểm lân cận phải nằm trong lưới.
            # Điểm lân cận không phải là chướng ngại vật (giá trị 1 trong lưới).
            # Điểm lân cận chưa được xem xét (không nằm trong closedList).
            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= grid.shape[1] or
                grid[neighbor[0], neighbor[1]] == 1 or
                neighbor in closedList):
                continue

            gValueNeighbor = gValue[current] + distance(current, neighbor)  # Chi phí đến điểm lân cận
            
            # Kiểm tra xem điểm lân cận có trong openList không hoặc chi phí đến điểm lân cận nhỏ hơn chi phí đã biết
            if ((neighbor not in [item[1] for item in openList]) or 
                (gValueNeighbor < gValue.get(neighbor, float('inf')))):
                
                gValue[neighbor] = gValueNeighbor # cập nhật chi phí đến điểm lân cận
                fValue[neighbor] = gValueNeighbor + heuristic(neighbor, goal)  # Cập nhật giá trị f
                prev[neighbor] = current # Cập nhật điểm trước đó của điểm lân cận trong route
                
                # Thêm điểm lân cận vào openList với giá trị f
                heappush(openList, (fValue[neighbor], neighbor))
                # Ghi log
                if log:
                    log(f"Đã thêm điểm lân cận {neighbor} với giá trị f {fValue[neighbor]} vào openList: {openList}")

    # Ghi log khi không tìm thấy đường đi
    if log:
        log("Không tìm thấy đường đi")

    # print("Không tìm thấy đường đi")
    return False

