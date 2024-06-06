from algorithms.shorttestPath import shorttestPath
from tkinter import messagebox, filedialog
import numpy as np
import tkinter as tk
import json
import random

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Application")

        self.root.state('zoomed')  # Maximize the window on launch

        self.grid_size = 10  # Default grid size
        self.grid = np.zeros((self.grid_size, self.grid_size))

        self.start_point = None
        self.goal_point = None
        self.pickup_points = []
        self.walls = []

        self.current_action = None

        self.show_coordinates = False

        self.create_widgets()
        self.set_grid_size()  # Initialize the grid with walls
        self.draw_grid()

    # Create and place widgets in the GUI
    def create_widgets(self):
        # Create a frame for the main widgets
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a frame for the log
        self.log_frame = tk.Frame(self.root, width=300)
        self.log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(self.log_frame, state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.grid_size_label = tk.Label(self.main_frame, text="Grid Size:")
        self.grid_size_label.grid(row=0, column=0)
        self.grid_size_entry = tk.Entry(self.main_frame)
        self.grid_size_entry.grid(row=0, column=1)
        self.grid_size_entry.insert(0, str(self.grid_size))

        self.pickup_label = tk.Label(self.main_frame, text="Pickup Points:")
        self.pickup_label.grid(row=1, column=0)
        self.pickup_entry = tk.Entry(self.main_frame)
        self.pickup_entry.grid(row=1, column=1)
        self.pickup_entry.insert(0, "3")

        self.walls_label = tk.Label(self.main_frame, text="Additional Walls:")
        self.walls_label.grid(row=2, column=0)
        self.walls_entry = tk.Entry(self.main_frame)
        self.walls_entry.grid(row=2, column=1)
        self.walls_entry.insert(0, "10")

        self.set_grid_button = tk.Button(self.main_frame, text="Set Grid Size", command=self.set_grid_size)
        self.set_grid_button.grid(row=0, column=2)

        self.canvas = tk.Canvas(self.main_frame, width=500, height=500)
        self.canvas.grid(row=3, column=0, columnspan=3, rowspan=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.start_button = tk.Button(self.main_frame, text="Set Start Point", command=self.set_start_point)
        self.start_button.grid(row=3, column=3, pady=1)

        self.goal_button = tk.Button(self.main_frame, text="Set Goal Point", command=self.set_goal_point)
        self.goal_button.grid(row=4, column=3, pady=1)

        self.pickup_button = tk.Button(self.main_frame, text="Add Pickup Point", command=self.add_pickup_point)
        self.pickup_button.grid(row=5, column=3, pady=1)

        self.wall_button = tk.Button(self.main_frame, text="Add Wall", command=self.add_wall)
        self.wall_button.grid(row=6, column=3, pady=1)

        self.run_button = tk.Button(self.main_frame, text="Run Pathfinding", command=self.run_pathfinding)
        self.run_button.grid(row=7, column=3, pady=1)
        
        self.clear_point_button = tk.Button(self.main_frame, text="Clear Point", command=self.clear_point)
        self.clear_point_button.grid(row=8, column=3, pady=1)
        
        self.clear_button = tk.Button(self.main_frame, text="Clear", command=self.clear_all_points)
        self.clear_button.grid(row=9, column=3, pady=1)

        self.save_button = tk.Button(self.main_frame, text="Save Current Map", command=self.save_current_map)
        self.save_button.grid(row=0, column=3, pady=1)

        self.load_button = tk.Button(self.main_frame, text="Load Input Data", command=self.load_from_file)
        self.load_button.grid(row=1, column=3, pady=1)

        self.random_button = tk.Button(self.main_frame, text="Generate Random Data", command=self.generate_random_data)
        self.random_button.grid(row=2, column=3, pady=1)

        self.clearlog_button = tk.Button(self.main_frame, text="Clear Log", command=self.clear_log)
        self.clearlog_button.grid(row=10, column=3, pady=1)

        self.cost_label = tk.Label(self.main_frame, text="Cost: N/A")
        self.cost_label.grid(row=11, column=3, pady=1)

        self.run_button_without_logging = tk.Button(self.main_frame, text="Run Pathfinding (No Logging)", command=self.run_pathfinding_without_logging)
        self.run_button_without_logging.grid(row=12, column=3, pady=1)
        
        self.toggle_coordinates_button = tk.Button(self.main_frame, text="Toggle Coordinates", command=self.toggle_coordinates)
        self.toggle_coordinates_button.grid(row=13, column=3, pady=1)
        
    def run_pathfinding_without_logging(self):
        for wall in self.walls:
            self.grid[wall[0], wall[1]] = 1

        cost, route = shorttestPath(self.grid, self.start_point, self.goal_point, self.pickup_points)
        print("Route", route)
        if route:
            self.draw_route(route)
            self.cost_label.config(text=f"Cost: {round(cost, 2)}")
        else:
            messagebox.showinfo("Result", "No path found")
            self.cost_label.config(text="Cost: N/A")    
        
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

                # Add text labels for start and goal points
                if (i, j) == self.start_point:
                    self.canvas.create_text(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2, text="S", fill="white")
                elif (i, j) == self.goal_point:
                    self.canvas.create_text(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2, text="G", fill="white")
                elif (i, j) in self.pickup_points:
                    self.canvas.create_text(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2, text="P", fill="white")

                # Add Oxy coordinates (only for debugging purposes)
        if self.show_coordinates:
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self.canvas.create_text(j * cell_size + cell_size // 2, i * cell_size + cell_size // 2 + cell_size // 3, text=f"({i},{j})", fill="gray")

    def toggle_coordinates(self):
        self.show_coordinates = not self.show_coordinates
        self.draw_grid()

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
        elif self.current_action == "clear":
            self.clear_specific_point(y, x)
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

    # Set the current action to "clear"
    def clear_point(self):
        self.current_action = "clear"

    # Set the current action to "save"
    def load_from_file(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.grid_size = data['grid_size']
                self.grid_size_entry.delete(0, tk.END)
                self.grid_size_entry.insert(0, str(self.grid_size))
                self.grid = np.zeros((self.grid_size, self.grid_size))
                self.start_point = tuple(data['start_point'])
                self.goal_point = tuple(data['goal_point'])
                self.pickup_points = [tuple(point) for point in data['pickup_points']]
                self.walls = [tuple(wall) for wall in data['walls']]
                for wall in self.walls:
                    self.grid[wall[0], wall[1]] = 1
                self.draw_grid()

    def generate_random_data(self):
        grid_size = int(self.grid_size_entry.get())
        num_pickup_points = int(self.pickup_entry.get())
        num_additional_walls = int(self.walls_entry.get())
        data = self.create_random_data(grid_size, num_pickup_points, num_additional_walls)
        self.load_data(data)

    def create_random_data(self, grid_size=10, num_pickup_points=3, num_additional_walls=10):
        grid = np.zeros((grid_size, grid_size))

        # Create boundaries around the grid
        walls = [(0, i) for i in range(grid_size)] + \
                [(grid_size-1, i) for i in range(grid_size)] + \
                [(i, 0) for i in range(grid_size)] + \
                [(i, grid_size-1) for i in range(grid_size)]

        # Mark boundaries in the grid
        for wall in walls:
            grid[wall[0], wall[1]] = 1

        def get_random_point(exclude_points):
            while True:
                point = (random.randint(1, grid_size-2), random.randint(1, grid_size-2))
                if point not in exclude_points:
                    return point

        # Generate random start and goal points
        start_point = get_random_point(walls)
        goal_point = get_random_point(walls + [start_point])

        # Generate random pickup points
        pickup_points = []
        for _ in range(num_pickup_points):
            pickup_point = get_random_point(walls + [start_point, goal_point] + pickup_points)
            pickup_points.append(pickup_point)

        # Generate random additional walls
        additional_walls = []
        for _ in range(num_additional_walls):
            wall_point = get_random_point(walls + [start_point, goal_point] + pickup_points + additional_walls)
            additional_walls.append(wall_point)
            grid[wall_point[0], wall_point[1]] = 1

        # Combine all walls
        all_walls = walls + additional_walls

        # Prepare data
        data = {
            "grid_size": grid_size,
            "start_point": start_point,
            "goal_point": goal_point,
            "pickup_points": pickup_points,
            "walls": all_walls
        }

        return data

    def load_data(self, data):
        self.grid_size = data['grid_size']
        self.grid_size_entry.delete(0, tk.END)
        self.grid_size_entry.insert(0, str(self.grid_size))
        self.grid = np.zeros((self.grid_size, self.grid_size))
        self.start_point = tuple(data['start_point'])
        self.goal_point = tuple(data['goal_point'])
        self.pickup_points = [tuple(p) for p in data['pickup_points']]
        self.walls = [tuple(w) for w in data['walls']]
        for wall in self.walls:
            self.grid[wall[0], wall[1]] = 1
        self.draw_grid()

    # Run the pathfinding algorithm and draw the route
    def run_pathfinding(self):
        for wall in self.walls:
            self.grid[wall[0], wall[1]] = 1

        print("Grid: \n", self.grid)
        print("Start: ", self.start_point)
        print("Goal: ", self.goal_point)
        print("PickupPoint: ", self.pickup_points)
        
        # Assume shorttestPath returns (route, cost)
        cost, route = shorttestPath(self.grid, self.start_point, self.goal_point, self.pickup_points, self.log)
        print("Route", route)
        if route:
            self.draw_route(route)
            self.cost_label.config(text=f"Cost: {round(cost, 2)}")
            self.log(f"Cost: {round(cost, 2)}")
        else:
            messagebox.showinfo("Result", "No path found")
            self.cost_label.config(text="Cost: N/A")
            self.log("No path found")

    # Draw the route on the canvas
    def draw_route(self, route):
        cell_size = 500 // self.grid_size
        visited = {}
        dot_size = cell_size // 3  # Kích thước của chấm nhỏ, bạn có thể điều chỉnh cho phù hợp

        for (y, x) in route:
            if (y, x) in visited:
                visited[(y, x)] += 1
            else:
                visited[(y, x)] = 1

            color = "red" if visited[(y, x)] > 1 else "black"
            dot_x = x * cell_size + cell_size // 2
            dot_y = y * cell_size + cell_size // 2

            # Vẽ chấm
            self.canvas.create_oval(
                dot_x - dot_size // 2, dot_y - dot_size // 2,
                dot_x + dot_size // 2, dot_y + dot_size // 2,
                fill=color, outline=color
            )

            # Hiển thị số lần đã đi qua điểm đó
            self.canvas.create_text(dot_x, dot_y, text=str(visited[(y, x)]), fill="white")

            self.canvas.update()
            self.root.after(100)  # Pause for 100 milliseconds to simulate animation

    def clear_all_points(self):
        self.start_point = None
        self.goal_point = None
        self.pickup_points = []
        self.walls = []
        self.grid = np.zeros((self.grid_size, self.grid_size))
        self.create_boundaries()
        self.draw_grid()
        self.cost_label.config(text="Cost: N/A")
        self.log("Cleared all points")

    # Clear a specific point on the grid
    def clear_specific_point(self, y, x):
        if (y, x) == self.start_point:
            self.start_point = None
        elif (y, x) == self.goal_point:
            self.goal_point = None
        elif (y, x) in self.pickup_points:
            self.pickup_points.remove((y, x))
        elif (y, x) in self.walls:
            self.walls.remove((y, x))
            self.grid[y, x] = 0
        self.log(f"Cleared point ({y}, {x})")

    # Log messages in the log Text widget
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)

    def save_current_map(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            data = {
                "grid_size": self.grid_size,
                "start_point": self.start_point,
                "goal_point": self.goal_point,
                "pickup_points": self.pickup_points,
                "walls": self.walls
            }
            with open(filename, 'w') as f:
                json.dump(data, f)
            self.log(f"Saved current map to {filename}")
        else:
            self.log("Save cancelled")
