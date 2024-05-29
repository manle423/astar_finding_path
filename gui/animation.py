from heapq import heappop, heappush
import matplotlib.pyplot as plt
from matplotlib import colors
from algorithms.utils import heuristic, insideThePolygon, changeCoordinate, adj
import numpy as np

def animation(grid, start, goal, quantity):
    openList = [(heuristic(start,goal), start)] #Tập mở (dùng cấu trúc priority queue)
    current=start
    while(1):        
        if current==goal:
            return
        # mở các trạng thái đường đi có thể
        for i,j in adj:
            neighbor= current[0]+i, current[1]+j
            if grid[neighbor[1], neighbor[0]] != 0: # kiểm tra trường hợp đụng phải chướng ngại vật
                continue
             #kiểm tra xem nó sắp đi vào đa giác hay không
            if (neighbor[0] != current[0]) and (neighbor[1] != current[1]): # trường hợp nó nằm trên đường chéo
                if insideThePolygon(neighbor, current, grid):
                    continue
            cost = heuristic(neighbor, goal)
            heappush(openList,(cost, neighbor))
        
        current=heappop(openList)[1]
        plt.scatter(current[0] + 0.5, current[1] + 0.5, color="black")
        # lúc này ta tìm xem những hướng mà biểu đồ không thể di chuyển được
        # (x, 0) là giới hạn ở việc di chuyển trục x , y thoải mái
        # (0,y) là giới hạn di chuyển ở trục y, x thoải mái
        # (x,y) là giới hạn di chuyển cả theo trục x, y
        noThisWay={}
        for i,j in adj:
            value=grid[current[1]+j,current[0]+i] #value có thể cho ta biết được đó là đa giác nào
            if value >2: # tức là điểm lúc này là đa giác
                diffX=i
                diffY=j
                if not value in noThisWay:
                    noThisWay[value]=(i,j)  #đa giác không thể di chuyển theo hướng x này, và hướng y này
                    continue
                # có thể trên kia hướng x, hoặc y chưa nhận giá trị 0 tức là không có cản trở ở trục y
                # Muốn cập nhật lại sự cản trở theo hướng x, hay y
                if diffX==0 and diffX != noThisWay[value][0]: 
                    noThisWay[value][0]=diffX
                if diffY==0 and diffY != noThisWay[value][1]:
                    noThisWay[value][1]=diffY
        
        # Cập nhật lại tọa độ bản đồ mới
        changeCoordinate(grid, noThisWay, quantity)
        cmap = colors.ListedColormap(["white", "black", "red", "green", "blue", "brown", "orange", "pink", "purple", "grey"])
        plt.pcolor(grid,cmap=cmap,edgecolors='k', linewidths=1)
        plt.pause(0.01)
        
