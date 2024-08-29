import tkinter as tk
import random
from queue import Queue, LifoQueue, PriorityQueue

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle with Auto-Solving")
        
        self.size = 3  # 3x3 puzzle
        self.goal_state = list(range(1, self.size * self.size)) + [None]
        self.tiles = self.goal_state[:]
        self.grid_buttons = []
        self.is_paused = False
        self.current_solution = None  # To store the current solution
        self.current_step_index = 0  # To store the current step in the solution
        
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
        """Refresh the puzzle by reshuffling the tiles."""
        self.shuffle_tiles()

    def toggle_pause(self):
        """Toggle between pausing and resuming the auto-solver."""
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
            # Swap tiles
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

    def find_neighbors(self, state):
        size = self.size
        empty_index = state.index(None)
        empty_row, empty_col = divmod(empty_index, size)

        neighbors = []
        for d_row, d_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = empty_row + d_row, empty_col + d_col
            if 0 <= new_row < size and 0 <= new_col < size:
                new_state = state[:]
                new_index = new_row * size + new_col
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                neighbors.append(new_state)
        
        return neighbors

    # BFS Algorithm
    def solve_bfs(self):
        initial_state = self.tiles[:]
        if self.is_solved():
            return

        frontier = Queue()
        frontier.put((initial_state, []))
        explored = set()

        while not frontier.empty():
            state, path = frontier.get()

            if state == self.goal_state:
                self.current_solution = path
                self.play_solution(path)
                return

            explored.add(tuple(state))

            for neighbor in self.find_neighbors(state):
                if tuple(neighbor) not in explored:
                    frontier.put((neighbor, path + [neighbor]))
                    explored.add(tuple(neighbor))

    # DFS Algorithm
    def solve_dfs(self):
        initial_state = self.tiles[:]
        if self.is_solved():
            return

        frontier = LifoQueue()
        frontier.put((initial_state, []))
        explored = set()

        while not frontier.empty():
            state, path = frontier.get()

            if state == self.goal_state:
                self.current_solution = path
                self.play_solution(path)
                return

            explored.add(tuple(state))

            for neighbor in self.find_neighbors(state):
                if tuple(neighbor) not in explored:
                    frontier.put((neighbor, path + [neighbor]))
                    explored.add(tuple(neighbor))

    # A* Algorithm with Manhattan Distance Heuristic
    def solve_astar(self):
        initial_state = self.tiles[:]
        if self.is_solved():
            return

        def manhattan_distance(state):
            distance = 0
            for i, tile in enumerate(state):
                if tile is None:  # Skip the empty tile
                    continue
                correct_row, correct_col = divmod(tile - 1, self.size)
                current_row, current_col = divmod(i, self.size)
                distance += abs(correct_row - current_row) + abs(correct_col - current_col)
            return distance

        # PriorityQueue stores tuples of (priority, g(n), state, path)
        frontier = PriorityQueue()
        frontier.put((manhattan_distance(initial_state), 0, initial_state, []))
        explored = set()

        while not frontier.empty():
            _, cost_so_far, state, path = frontier.get()

            if state == self.goal_state:
                self.play_solution(path)
                return

            explored.add(tuple(state))

            for neighbor in self.find_neighbors(state):
                if tuple(neighbor) not in explored:
                    # Calculate g(n) (cost so far) and f(n) (total cost: g(n) + h(n))
                    new_cost = cost_so_far + 1
                    priority = new_cost + manhattan_distance(neighbor)
                    frontier.put((priority, new_cost, neighbor, path + [neighbor]))
                    explored.add(tuple(neighbor))


    def play_solution(self, solution, step_index=0):
        """Play the solution step by step, considering pause functionality."""
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

if __name__ == "__main__":
    root = tk.Tk()
    puzzle = SlidingPuzzle(root)
    root.mainloop()
