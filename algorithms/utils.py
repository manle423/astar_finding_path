from heapq import *
from math import sqrt 
from random import *

#Độ dời để xét các điểm liền kề (các trạng thái tiếp theo) (cho phép đi chéo)
adj = [(-1, -1), (-1, 0), (-1, 1), (0, -1) , (0, 1), (1, -1), (1, 0), (1, 1)]

# chỉ đi thẳng
# adj = [(-1, 0), (0, -1) , (0, 1), (1, 0)]

# để tính khoảng cách từ điểm đang xét tới điểm đích cuối cùng
def heuristic(p, goal):
    return sqrt((goal[0] - p[0]) ** 2 + (goal[1] - p[1]) ** 2)

# để tính khoảng cách giữa 2 điểm đang xét
def distance(p1, p2):
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

# để tính chi phí nếu đi dọc thì tính là 1, và đi chéo thì tính là sqrt(2)
def costOfPath(path):
    cost = 0
    for i in range(len(path) - 1):
        if (path[i][0] == path[i + 1][0]) or (path[i][1] == path[i + 1][1]):
            cost += 1
        else:
            cost += sqrt(2)
    return cost
