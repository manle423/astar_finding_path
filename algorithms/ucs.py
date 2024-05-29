from heapq import heappop, heappush
from .utils import distance, insideThePolygon, adj

def UCS(grid, start, goal):
    closedList = []
    gValue = {start:0}
    openList = [(gValue[start], start)]
    prev = {}

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
            gValueNeighbor = gValue[current] + distance(current, neighbor)  # khoảng cách

            if grid[neighbor[1], neighbor[0]] != 0: # kiểm tra trường hợp đụng phải chướng ngại vật
                continue

            if (neighbor[0] != current[0]) and (neighbor[1] != current[1]): # trường hợp nó nằm trên đường chéo
                if insideThePolygon(neighbor, current, grid): # kiểm tra xem điểm này có nằm trong đa giác hay chưa
                    continue

            #Nếu nằm trong tập đóng thì bỏ qua
            # đã tồn tại và đường đi tới nó hiện tại ngắn hơn đường đi mới tìm được thì không xét
            if neighbor in closedList: 
                continue

            #Nếu chưa trong tập mở hoặc đang trong tập mở mà có giá trị tốt hơn thì push vào tập mở
            if (neighbor not in [item[1] for item in openList]) or (gValueNeighbor < gValue.get(neighbor,0)):
                gValue[neighbor] = gValueNeighbor
                prev[neighbor] = current
                heappush(openList, (gValue[neighbor],neighbor))
    
    return False

