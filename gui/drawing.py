import numpy as np
from algorithms.bresenham import matchTwoPoint

def drawing(grid, fi, quantity):
    #tạo đường biên
    grid[0,:] = 1
    grid[(grid.shape[0]-1),:] = 1
    grid[:,0] = 1
    grid[:,(grid.shape[1]-1)] = 1
    
    #đọc vào số hình
    for k in range(quantity):
        line = fi.readline()

        token = line.split(',')
        vertices = []
        pair_Index = [] #Chỉ số các cặp đỉnh của đa giác theo chiều kim đồng hồ để xét nối với nhau


        for i in range(int(len(token) / 2)):
            x = int(token[2*i])
            y = int(token[2*i +  1])
            vertices.append((x, y))
            grid[y][x] = k + 3


        #nếu trường hợp là vẽ đoạn thẳng
        if len(vertices) == 2:
            pair_Index.append((0,1))
        else:
            for i in range(len(vertices) - 1):
                pair_Index.append((i, i + 1))
            pair_Index.append((len(vertices) - 1, 0))

        for i,j in pair_Index:

            for x, y in matchTwoPoint(vertices[i], vertices[j]):
                grid[y][x] = k + 3

    fi.close()




