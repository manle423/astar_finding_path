from heapq import heappop, heappush
from .utils import *

def astarTest(grid, start, goal, log=None, debug_mode=False, update_canvas=None):
    closedList = set()  
    gValue = {start: 0}  
    fValue = {start: heuristic(start, goal)}  
    openList = [(fValue[start], start)]  
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

        if log:
            log(f"Thêm {current} vào closedList: {closedList}")
        closedList.add(current)

        if debug_mode and update_canvas:
            update_canvas(current, "gray")  # Màu xám cho các điểm đã xét
            update_canvas(start, "yellow", override=True)
            update_canvas(goal, "pink", override=True)

        for i, j in adj:
            neighbor = current[0] + i, current[1] + j
            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= grid.shape[1] or
                grid[neighbor[0], neighbor[1]] == 1 or
                neighbor in closedList):
                continue

            gValueNeighbor = gValue[current] + distance(current, neighbor)  
            if ((neighbor not in [item[1] for item in openList]) or 
                (gValueNeighbor < gValue.get(neighbor, float('inf')))):
                
                gValue[neighbor] = gValueNeighbor 
                fValue[neighbor] = gValueNeighbor + heuristic(neighbor, goal)  
                prev[neighbor] = current 
                
                heappush(openList, (fValue[neighbor], neighbor))

                if debug_mode and update_canvas:
                    update_canvas(neighbor, "yellow")  # Màu vàng cho các điểm đang được xét
                if log:
                    log(f"Đã thêm điểm lân cận {neighbor} với giá trị f {fValue[neighbor]} vào openList: {openList}")

    if log:
        log("Không tìm thấy đường đi")

    return False



def shorttestPathTest(grid, start, goal, pickupPoint, log=None, debug_mode=False, update_canvas=None):
    visited = [] 
    finalPath = [] 
    newStart = start 
    length = len(pickupPoint)
    sumCost = 0 
    
    while length > 0:
        routes = {} 
        pq = [] 
        
        for point in pickupPoint:
            if point not in visited:
                path = astarTest(grid, newStart, point, log=log, debug_mode=debug_mode, update_canvas=update_canvas)
                if path == False: 
                    return (-1, False) 
                routes[point] = path
                heappush(pq, (costOfPath(path), point))
                
                if log:
                    log(f"Tìm thấy đường đi từ {newStart} đến {point}: {path}")
                
        if not pq:
            return (-1, False)
        
        cost, pickPoint = heappop(pq) 
        sumCost += cost
        finalPath += routes[pickPoint]
        visited.append(pickPoint) 
        newStart = pickPoint
        length -= 1
    
    path = astarTest(grid, newStart, goal, log=log, debug_mode=debug_mode, update_canvas=update_canvas)
    if path == False:
        return (-1, False)
    sumCost += costOfPath(path)
    finalPath += path

    if log:
        log(f"Tìm thấy đường đi từ {newStart} đến {goal}: {path}")
        log(f"Tổng chi phí: {sumCost}")
        log(f"Lộ trình cuối cùng: {finalPath}")
        
    return (sumCost, finalPath)
