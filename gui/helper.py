import tkinter as tk

# Tạo ra giao diện
def create_widgets(app):
    # Create a frame for the log
    app.log_frame = tk.Frame(app.root, width=300)
    app.log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    app.log_text = tk.Text(app.log_frame, state=tk.DISABLED, wrap=tk.WORD)
    app.log_text.pack(fill=tk.BOTH, expand=True)

    # Create a frame for the main widgets on the right
    app.main_frame = tk.Frame(app.root)
    app.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Top frame for IO functions and input parameters
    top_frame = tk.Frame(app.main_frame)
    top_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')

    app.grid_size_label = tk.Label(top_frame, text="Grid Size:")
    app.grid_size_label.grid(row=0, column=0)
    app.grid_size_entry = tk.Entry(top_frame, width=5)
    app.grid_size_entry.grid(row=0, column=1)
    app.grid_size_entry.insert(0, str(app.grid_size))

    app.pickup_label = tk.Label(top_frame, text="Pickup Points:")
    app.pickup_label.grid(row=1, column=0)
    app.pickup_entry = tk.Entry(top_frame, width=5)
    app.pickup_entry.grid(row=1, column=1)
    app.pickup_entry.insert(0, "3")

    app.walls_label = tk.Label(top_frame, text="Additional Walls:")
    app.walls_label.grid(row=2, column=0)
    app.walls_entry = tk.Entry(top_frame, width=5)
    app.walls_entry.grid(row=2, column=1)
    app.walls_entry.insert(0, "10")

    app.set_grid_button = tk.Button(top_frame, text="Set Grid Size", command=app.set_grid_size)
    app.set_grid_button.grid(row=0, column=2, padx=5)

    app.save_button = tk.Button(top_frame, text="Save Current Map", command=app.save_current_map)
    app.save_button.grid(row=0, column=3, padx=5)

    app.load_button = tk.Button(top_frame, text="Load Input Data", command=app.load_from_file)
    app.load_button.grid(row=1, column=3, padx=5)

    app.random_button = tk.Button(top_frame, text="Generate Random Data", command=app.generate_random_data)
    app.random_button.grid(row=2, column=3, padx=5)

    # Middle frame for the canvas
    app.canvas_frame = tk.Frame(app.main_frame)
    app.canvas_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    app.canvas = tk.Canvas(app.canvas_frame, width=500, height=500)
    app.canvas.pack()
    app.canvas.bind("<Button-1>", app.on_canvas_click)

    # Right frame for action buttons
    right_frame = tk.Frame(app.main_frame)
    right_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    app.start_button = tk.Button(right_frame, text="Set Start Point", command=app.set_start_point)
    app.start_button.grid(row=0, column=0, pady=5)

    app.goal_button = tk.Button(right_frame, text="Set Goal Point", command=app.set_goal_point)
    app.goal_button.grid(row=1, column=0, pady=5)

    app.pickup_button = tk.Button(right_frame, text="Add Pickup Point", command=app.add_pickup_point)
    app.pickup_button.grid(row=2, column=0, pady=5)

    app.wall_button = tk.Button(right_frame, text="Add Wall", command=app.add_wall)
    app.wall_button.grid(row=3, column=0, pady=5)

    app.clear_point_button = tk.Button(right_frame, text="Clear Point", command=app.clear_point)
    app.clear_point_button.grid(row=4, column=0, pady=5)

    app.clear_button = tk.Button(right_frame, text="Clear All Points", command=app.clear_all_points)
    app.clear_button.grid(row=5, column=0, pady=5)
    
    app.clearlog_button = tk.Button(right_frame, text="Clear Log", command=app.clear_log)
    app.clearlog_button.grid(row=6, column=0, padx=5)

    app.toggle_coordinates_button = tk.Button(right_frame, text="Toggle Coordinates", command=app.toggle_coordinates)
    app.toggle_coordinates_button.grid(row=7, column=0, pady=5)

    app.cost_label = tk.Label(right_frame, text="Cost: N/A")
    app.cost_label.grid(row=8, column=0, pady=5)

    # Bottom frame for run buttons
    bottom_frame = tk.Frame(app.main_frame)
    bottom_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')

    app.run_button = tk.Button(bottom_frame, text="Run Pathfinding (With Logging)", command=app.run_pathfinding)
    app.run_button.grid(row=0, column=0, pady=5)

    app.run_button_without_logging = tk.Button(bottom_frame, text="Run Pathfinding (No Logging)", command=app.run_pathfinding_without_logging)
    app.run_button_without_logging.grid(row=0, column=2, pady=5)
    
    app.run_button_debug = tk.Button(bottom_frame, text="Run Pathfinding (Debug)", command=app.run_pathfinding_debug)
    app.run_button_debug.grid(row=0, column=4, pady=5)
