from heapq import *
from math import sqrt 
from random import *

#Độ dời để xét các điểm liền kề (các trạng thái tiếp theo)
adj = [(-1, -1), (-1, 0), (-1, 1), (0, -1) , (0, 1), (1, -1), (1, 0), (1, 1)]


###########################################################################################################
#Kiểm tra để phát hiện đi chéo xuyên qua đa giác
def insideThePolygon(neighbor, current, grid):
    x1 , y1 = current
    x2 , y2 = neighbor
    xDiff = x2 - x1
    yDiff = y2 - y1

    if (y2 != y1) and (x2 != x1): #Nếu đi chéo
        value1 = grid[y1 + yDiff][x1]
        value2 = grid[y1][x1 + xDiff]
        #Kiểm tra 2 điểm tiếp xúc với điểm hiện tại và kiểm đang xét có phải cùng thuộc 1 đa giác?
        if (value1 != 0) and (value2 != 0) and (value1 == value2):
            return True

    return False

###########################################################################################################
#Hàm tính Heuritic (theo norm 2) khoảng cách từ điểm đang xét đếm đích
def heuristic(p, goal):
    return sqrt((goal[0] - p[0]) ** 2 + (goal[1] - p[1]) ** 2)

###########################################################################################################
#Hàm tính khoảng cách giữa 2 điểm trên mặt phẳng tọa độ
def distance(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

###########################################################################################################
# Hàm tính chi phí đường đi. Đi thẳng thì tính chi phí bằng 1, đi chéo thì tính chi phí bằng sqrt(2)
def costOfPath(path, start):
    cost = 0
    for i in range(len(path) - 1):
        if (path[i][0] == path[i+1][0]) or ( path[i][1] == path[i+1][1]):
            cost += 1
        else:
            cost += sqrt(2)

    if (start[0] == path[0][0]) or (start[1] == path[0][1]):
        cost += 1
    else:
        cost += sqrt(2)

    return cost

##############################################################
# changeCoordinate: thay đổi tọa độ các polygon trên bản đồ
def changeCoordinate(grid, noThisWay, quantity):
    for i in range(quantity):
        value = i + 3
        if value in noThisWay:
            x_limit = noThisWay[value][0]
            y_limit = noThisWay[value][1]
            new_X = randint(-1, 1) if x_limit == 0 else (randint(0, 1) if x_limit > 0 else randint(-1, 0))
            new_Y = randint(-1, 1) if y_limit == 0 else (randint(0, 1) if y_limit > 0 else randint(-1, 0))
        for i in range(grid.shape[1]):  # x
            for j in range(grid.shape[0]):  # y
                if grid[j, i] == value:
                    grid[j, i] = 0
                    grid[j + new_Y, i + new_X] = value

