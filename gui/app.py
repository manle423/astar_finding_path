# from algorithms.shorttestPath import shorttestPath
from tkinter import messagebox
import numpy as np
import tkinter as tk
from heapq import *
from math import sqrt 
from random import *

#Độ dời để xét các điểm liền kề (các trạng thái tiếp theo)
adj = [(-1, -1), (-1, 0), (-1, 1), (0, -1) , (0, 1), (1, -1), (1, 0), (1, 1)]


###########################################################################################################
#Kiểm tra để phát hiện đi chéo xuyên qua đa giác
def insideThePolygon(neighbor, current, grid):
    x1, y1 = current
    x2, y2 = neighbor
    xDiff = x2 - x1
    yDiff = y2 - y1

    if (y2 != y1) and (x2 != x1):  # Nếu đi chéo
        value1 = grid[y1 + yDiff][x1]
        value2 = grid[y1][x1 + xDiff]
        # Kiểm tra 2 điểm tiếp xúc với điểm hiện tại và kiểm đang xét có phải cùng thuộc 1 đa giác?
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
    print("cost ",i ,cost)
    return cost

def costOfPath1(path):
    cost = 0
    for i in range(len(path) - 1):
        if (path[i][0] == path[i + 1][0]) or (path[i][1] == path[i + 1][1]):
            cost += 1
        else:
            cost += sqrt(2)
    return cost


def astar(grid, start, goal):
    closedList = set()  # Closed set
    gValue = {start: 0}  # Cost from start to current node
    fValue = {start: heuristic(start, goal)}  # Estimated cost from start to goal through current node
    openList = [(fValue[start], start)]  # Priority queue of open nodes
    prev = {}  # To reconstruct the path

    while openList:
        current = heappop(openList)[1]  # Node with lowest f-value
        if current == goal:
            route = []
            while current in prev:
                route.append(current)
                current = prev[current]
            route.append(start)
            return route[::-1]  # Return reversed path

        closedList.add(current)

        for i, j in adj:
            neighbor = current[0] + i, current[1] + j  # Neighboring node

            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= grid.shape[1] or
                grid[neighbor[0], neighbor[1]] == 1 or
                neighbor in closedList):
                continue

            gValueNeighbor = gValue[current] + distance(current, neighbor)  # Cost to neighbor

            if (neighbor[0] != current[0]) and (neighbor[1] != current[1]):  # Diagonal move
                if insideThePolygon(neighbor, current, grid):
                    continue

            if (neighbor not in [item[1] for item in openList]) or (gValueNeighbor < gValue.get(neighbor, float('inf'))):
                gValue[neighbor] = gValueNeighbor
                fValue[neighbor] = gValueNeighbor + heuristic(neighbor, goal)  # Update f-value
                prev[neighbor] = current
                heappush(openList, (fValue[neighbor], neighbor))

    return False
###########################################################################################################
# shorttestPath algorithm (tổng chi phí đi qua các điểm đón và về đích là nhỏ nhất)
# áp dụng thuật toán astar cho mỗi lần tìm đường (đi đến điểm đón có chi phí nhỏ nhất đối với điểm đang xét)
# pickupPoint là danh sách các điểm đón
# Hàm trả về tổng chi phí và lộ trình
def shorttestPath(grid, start, goal, pickupPoint):
    visited = [] #Danh sách các điểm đón đã đi qua
    finalPath = [] #Đường đi của bài toán
    newStart = start 
    length = len(pickupPoint)
    sumCost = 0 #Tổng chi phí
    while(length > 0):
        routes = {} #Đường đi ngắn nhất từ điểm đang xét đến các điểm đón chưa đi qua
        pq = [] # Dùng priority queue để lưu điểm đón và chi phí từ điểm đang xét đến nó
        for point in pickupPoint:
            if point not in visited:
                path = astar(grid, newStart, point)# đương đi ngắn nhất từ điểm đang xét đến nó
                if path == False: #Không tìm thấy đường đi
                    return (-1, False) 
                routes[point] = path
                # ở đây phải có 1 hàm tính chi phí đường đi
                heappush(pq, (costOfPath1(path), point) )
                # heappush(pq, (costOfPath(path, newStart)-heuristic(point, goal), point) )
        cost, pickPoint = heappop(pq) #Cho ra điểm có chi phí nhỏ nhất
        sumCost += cost
        finalPath += routes[pickPoint]
        visited.append(pickPoint) #Đánh dấu là đã đi đến
        newStart = pickPoint
        length -= 1
    
    #Tìm lộ trình từ điểm đón cuối dùng đến đích
    path = astar(grid, newStart, goal)
    if path == False:
        return (-1, False)
    sumCost += costOfPath1(path)
    # sumCost += costOfPath(path, newStart)
    finalPath += path

    #Trả về tổng chi phí và lộ trình
    return (sumCost, finalPath)
    


class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Application")

        self.grid_size = 10  # Default grid size
        self.grid = np.zeros((self.grid_size, self.grid_size))

        self.start_point = None
        self.goal_point = None
        self.pickup_points = []
        self.walls = []

        self.current_action = None

        self.create_widgets()
        self.set_grid_size()  # Initialize the grid with walls
        self.draw_grid()

    # Create and place widgets in the GUI
    def create_widgets(self):
        self.grid_size_label = tk.Label(self.root, text="Grid Size:")
        self.grid_size_label.grid(row=0, column=0)
        self.grid_size_entry = tk.Entry(self.root)
        self.grid_size_entry.grid(row=0, column=1)
        self.grid_size_entry.insert(0, str(self.grid_size))

        self.set_grid_button = tk.Button(self.root, text="Set Grid Size", command=self.set_grid_size)
        self.set_grid_button.grid(row=0, column=2)

        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.grid(row=1, column=0, columnspan=3, rowspan=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.start_button = tk.Button(self.root, text="Set Start Point", command=self.set_start_point)
        self.start_button.grid(row=1, column=3)

        self.goal_button = tk.Button(self.root, text="Set Goal Point", command=self.set_goal_point)
        self.goal_button.grid(row=2, column=3)

        self.pickup_button = tk.Button(self.root, text="Add Pickup Point", command=self.add_pickup_point)
        self.pickup_button.grid(row=3, column=3)

        self.wall_button = tk.Button(self.root, text="Add Wall", command=self.add_wall)
        self.wall_button.grid(row=4, column=3)

        self.run_button = tk.Button(self.root, text="Run Pathfinding", command=self.run_pathfinding)
        self.run_button.grid(row=5, column=3)

        self.cost_label = tk.Label(self.root, text="Cost: N/A")
        self.cost_label.grid(row=6, column=3)

    # Set the grid size based on user input
    def set_grid_size(self):
        try:
            size = int(self.grid_size_entry.get())
            if size > 0:
                self.grid_size = size
                self.grid = np.zeros((self.grid_size, self.grid_size))
                self.start_point = None
                self.goal_point = None
                self.pickup_points = []
                self.walls = []
                self.create_boundaries()
                self.draw_grid()
            else:
                messagebox.showerror("Error", "Grid size must be a positive integer.")
        except ValueError:
            messagebox.showerror("Error", "Invalid grid size. Please enter a positive integer.")

    # Create boundaries around the grid
    def create_boundaries(self):
        self.grid[0, :] = 1
        self.grid[self.grid_size-1, :] = 1
        self.grid[:, 0] = 1
        self.grid[:, self.grid_size-1] = 1
        self.walls = [(0, i) for i in range(self.grid_size)] + \
                     [(self.grid_size-1, i) for i in range(self.grid_size)] + \
                     [(i, 0) for i in range(self.grid_size)] + \
                     [(i, self.grid_size-1) for i in range(self.grid_size)]

    # Draw the grid and color the points based on their type
    def draw_grid(self):
        self.canvas.delete("all")
        cell_size = 500 // self.grid_size
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = "white"
                if (i, j) == self.start_point:
                    color = "green"
                elif (i, j) == self.goal_point:
                    color = "red"
                elif (i, j) in self.pickup_points:
                    color = "blue"
                elif self.grid[i, j] == 1:
                    color = "black"
                self.canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color)

    # Handle canvas click events
    def on_canvas_click(self, event):
        cell_size = 500 // self.grid_size
        x = event.x // cell_size
        y = event.y // cell_size
        if self.current_action == "start":
            self.start_point = (y, x)
        elif self.current_action == "goal":
            self.goal_point = (y, x)
        elif self.current_action == "pickup":
            self.pickup_points.append((y, x))
        elif self.current_action == "wall":
            self.walls.append((y, x))
            self.grid[y, x] = 1
        self.draw_grid()

    # Set the current action to "start"
    def set_start_point(self):
        self.current_action = "start"

    # Set the current action to "goal"
    def set_goal_point(self):
        self.current_action = "goal"

    # Set the current action to "pickup"
    def add_pickup_point(self):
        self.current_action = "pickup"

    # Set the current action to "wall"
    def add_wall(self):
        self.current_action = "wall"

    # Run the pathfinding algorithm and draw the route
    def run_pathfinding(self):
        for wall in self.walls:
            self.grid[wall[0], wall[1]] = 1

        print("Grid: \n", self.grid)
        print("Start: ", self.start_point)
        print("Goal: ", self.goal_point)
        print("PickupPoint: ", self.pickup_points)
        
        # Assume shorttestPath returns (route, cost)
        cost, route = shorttestPath(self.grid, self.start_point, self.goal_point, self.pickup_points)
        print("Route", route)
        if route:
            self.draw_route(route)
            self.cost_label.config(text=f"Cost: {round(cost, 2)}")
        else:
            messagebox.showinfo("Result", "No path found")
            self.cost_label.config(text="Cost: N/A")

    # Draw the route on the canvas
    def draw_route(self, route):
        cell_size = 500 // self.grid_size
        visited = []
        dot_size = cell_size // 3  # Kích thước của chấm nhỏ, bạn có thể điều chỉnh cho phù hợp

        for (y, x) in route:
            color = "red" if (y, x) in visited else "black"
            dot_x = x * cell_size + cell_size // 2
            dot_y = y * cell_size + cell_size // 2
            self.canvas.create_oval(
                dot_x - dot_size // 2, dot_y - dot_size // 2,
                dot_x + dot_size // 2, dot_y + dot_size // 2,
                fill=color, outline=color
            )
            visited.append((y, x))
            self.canvas.update()
            self.root.after(10)  # Pause for 10 milliseconds to simulate animation

            
if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
