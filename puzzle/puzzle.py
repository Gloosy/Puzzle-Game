import tkinter as tk
import random
from .algorithms import bfs_search, dfs_search, a_star_search
from .utils import find_neighbors_static

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle with Auto-Solving")
        
        self.size = 3  # 3x3 puzzle
        self.goal_state = list(range(1, self.size * self.size)) + [None]
        self.tiles = self.goal_state[:]
        self.grid_buttons = []
        self.is_paused = False
        self.current_solution = None
        self.current_step_index = 0
        
        self.create_grid()
        self.shuffle_tiles()

        # Buttons for Auto-Solving and Control
        self.bfs_button = tk.Button(self.root, text="Solve with BFS", command=self.solve_bfs)
        self.bfs_button.grid(row=self.size, column=0)

        self.dfs_button = tk.Button(self.root, text="Solve with DFS", command=self.solve_dfs)
        self.dfs_button.grid(row=self.size, column=1)

        self.astar_button = tk.Button(self.root, text="Solve with A*", command=self.solve_astar)
        self.astar_button.grid(row=self.size, column=2)

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_puzzle)
        self.refresh_button.grid(row=self.size + 1, column=0)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=self.size + 1, column=1)

    def create_grid(self):
        frame = tk.Frame(self.root)
        frame.grid()
        
        for row in range(self.size):
            row_buttons = []
            for col in range(self.size):
                btn = tk.Button(frame, text="", font=("Helvetica", 24), width=4, height=2)
                btn.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(btn)
            self.grid_buttons.append(row_buttons)

        self.update_grid()

    def shuffle_tiles(self):
        random.shuffle(self.tiles)
        while not self.is_solvable():
            random.shuffle(self.tiles)
        self.update_grid()

    def refresh_puzzle(self):
        self.shuffle_tiles()

    def toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="Pause")
            self.play_solution(self.current_solution, self.current_step_index)  # Resume solving
        else:
            self.is_paused = True
            self.pause_button.config(text="Resume")

    def update_grid(self):
        for row in range(self.size):
            for col in range(self.size):
                tile_value = self.tiles[row * self.size + col]
                if tile_value is None:
                    self.grid_buttons[row][col].config(text="", bg="lightgray")
                else:
                    self.grid_buttons[row][col].config(text=str(tile_value), bg="lightblue")

    def move_tile(self, row, col):
        empty_index = self.tiles.index(None)
        empty_row, empty_col = divmod(empty_index, self.size)
        
        if abs(empty_row - row) + abs(empty_col - col) == 1:
            self.tiles[empty_index], self.tiles[row * self.size + col] = self.tiles[row * self.size + col], self.tiles[empty_index]
            self.update_grid()

    def is_solvable(self):
        inversions = 0
        tile_values = [t for t in self.tiles if t is not None]
        for i in range(len(tile_values)):
            for j in range(i + 1, len(tile_values)):
                if tile_values[i] > tile_values[j]:
                    inversions += 1
        return inversions % 2 == 0

    def is_solved(self):
        return self.tiles == self.goal_state

    def solve_bfs(self):
        initial_state = self.tiles[:]
        if self.is_solved():
            return
        
        solution = bfs_search(initial_state, self.goal_state, self.size)
        if solution:
            self.play_solution(solution)

    def solve_dfs(self):
        initial_state = self.tiles[:]
        if self.is_solved():
            return

        solution = dfs_search(initial_state, self.goal_state, self.size)
        if solution:
            self.play_solution(solution)

    def solve_astar(self):
        initial_state = self.tiles[:]
        if self.is_solved():
            return
        solution = a_star_search(initial_state, self.goal_state, self.size)
        if solution:
            self.play_solution(solution)
        else:
            print("No solution found.")
            
    def play_solution(self, solution, step_index=0):
        self.current_solution = solution
        self.current_step_index = step_index
        
        if not solution or self.is_paused:
            return

        def play_step(step_index):
            if step_index < len(solution) and not self.is_paused:
                self.tiles = solution[step_index]
                self.update_grid()
                self.root.after(200, lambda: play_step(step_index + 1))

        play_step(step_index)
