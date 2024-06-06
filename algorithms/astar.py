from heapq import heappop, heappush
from .utils import heuristic, distance, insideThePolygon, adj

def astar(grid, start, goal, log=None):
    closedList = set()  # Tập hợp các điểm đã được xem xét
    gValue = {start: 0}  # Chi phí từ điểm bắt đầu đến điểm hiện tại
    fValue = {start: heuristic(start, goal)}  # Chi phí ước tính từ điểm bắt đầu đến đích thông qua điểm hiện tại
    openList = [(fValue[start], start)]  # Hàng đợi ưu tiên của các điểm cần xem xét
    prev = {}  # Để tái tạo lại đường đi

    # print(f"Khởi động A* từ {start} đến {goal}")

    while openList:
        current = heappop(openList)[1]  # Điểm có giá trị f thấp nhất
        # print(f"Điểm hiện tại: {current}, đích: {goal}")
        if current == goal:
            route = []
            while current in prev:
                route.append(current)
                current = prev[current]
            route.append(start)
            if log:
                log(f"Đường đi tìm thấy: {route[::-1]}")
            return route[::-1]  # Trả về đường đi đảo ngược

        closedList.add(current)
        if log:
            log(f"Thêm {current} vào danh sách đóng")
        
        for i, j in adj:
            neighbor = current[0] + i, current[1] + j  # Điểm lân cận

            # kiểm tra các điểm lân cận có hợp lệ hay không
            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= grid.shape[1] or
                grid[neighbor[0], neighbor[1]] == 1 or
                neighbor in closedList):
                continue

            gValueNeighbor = gValue[current] + distance(current, neighbor)  # Chi phí đến điểm lân cận

            if (neighbor not in [item[1] for item in openList]) or (gValueNeighbor < gValue.get(neighbor, float('inf'))):
                gValue[neighbor] = gValueNeighbor
                fValue[neighbor] = gValueNeighbor + heuristic(neighbor, goal)  # Cập nhật giá trị f
                prev[neighbor] = current
                heappush(openList, (fValue[neighbor], neighbor))
                # Ghi log
                if log:
                    log(f"Đã thêm điểm lân cận {neighbor} với giá trị f {fValue[neighbor]} vào hàng đợi mở")

    # Ghi log khi không tìm thấy đường đi
    if log:
        log("Không tìm thấy đường đi")

    # print("Không tìm thấy đường đi")
    return False
