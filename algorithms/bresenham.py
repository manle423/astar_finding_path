###########################################################################################################
#Hàm trả về danh sách các điểm để nối 2 điểm p1, p2
#Hàm sử dụng thuật toán Bresenham để nối 2 điểm tạo thành đường chéo
def matchTwoPoint(p1, p2):
    res = []
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1]
    if yDiff == 0:
        for i in range(abs(xDiff) - 1):
            if xDiff > 0:
                x = p1[0] + 1 + i
            else:
                x = p1[0] - 1 - i
            y = p1[1]
            res.append((x,y))
        return res
    elif xDiff == 0:
        for i in range(abs(yDiff) - 1):
            if yDiff > 0:
                y = p1[1] + 1 + i
            else:
                y = p1[1] - 1 - i

            x = p1[0]
            res.append((x,y))
        return res
    else:
        res = bresenham(p1, p2)
    return res


###########################################################################################################
#Thuật toán Bresenham
def bresenham(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    steep = abs(y2 - y1) > abs(x2 - x1)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1 , x2 = x2, x1
        y1 , y2 = y2, y1

    Dx = x2 - x1
    Dy = abs(y2 - y1)
    err = Dx/2 - Dy
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    y = y1
    if err < 0:
        y = y + ystep
        err = err + Dx
    res = []

    for x in range(x1 + 1, x2):
        if steep:
            res.append((y,x))
        else:
            res.append((x,y))
        err = err - Dy
        if err < 0:
            y = y + ystep
            err = err + Dx
    return res

