from queue import Queue, LifoQueue, PriorityQueue
from .utils import find_neighbors_static

def bfs_search(initial_state, goal_state, size):
    frontier = Queue()
    frontier.put((initial_state, []))
    explored = set()

    while not frontier.empty():
        state, path = frontier.get()

        if state == goal_state:
            return path

        explored.add(tuple(state))

        for neighbor in find_neighbors_static(state, size):
            if tuple(neighbor) not in explored:
                frontier.put((neighbor, path + [neighbor]))
                explored.add(tuple(neighbor))

    return None  # No solution found

def dfs_search(initial_state, goal_state, size):
    frontier = LifoQueue()
    frontier.put((initial_state, []))
    explored = set()

    while not frontier.empty():
        state, path = frontier.get()

        if state == goal_state:
            return path

        explored.add(tuple(state))

        for neighbor in find_neighbors_static(state, size):
            if tuple(neighbor) not in explored:
                frontier.put((neighbor, path + [neighbor]))
                explored.add(tuple(neighbor))

    return None  # No solution found

def a_star_search(initial_state, goal_state, size):
    def manhattan_distance(state):
        distance = 0
        for i, tile in enumerate(state):
            if tile is None:  # Skip the empty tile (represented by None)
                continue
            correct_row, correct_col = divmod(tile - 1, size)
            current_row, current_col = divmod(i, size)
            distance += abs(correct_row - current_row) + abs(correct_col - current_col)
        return distance

    def find_neighbors_static(state, size):
        # Implement the logic for finding neighbors (valid moves) in the sliding puzzle
        neighbors = []
        empty_index = state.index(None)  # Find the index of the empty tile (None)
        row, col = divmod(empty_index, size)

        # Define the possible moves (up, down, left, right)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in moves:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < size and 0 <= new_col < size:  # Check if move is within bounds
                new_index = new_row * size + new_col
                new_state = state[:]
                # Swap the empty tile with the adjacent tile
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                neighbors.append(new_state)

        return neighbors

    frontier = PriorityQueue()
    frontier.put((manhattan_distance(initial_state), 0, initial_state, []))
    explored = set()

    while not frontier.empty():
        _, cost_so_far, state, path = frontier.get()

        if state == goal_state:
            return path + [goal_state]  # Return final path including goal state

        explored.add(tuple(state))  # Mark state as explored

        for neighbor in find_neighbors_static(state, size):
            if tuple(neighbor) not in explored:
                new_cost = cost_so_far + 1
                priority = new_cost + manhattan_distance(neighbor)
                frontier.put((priority, new_cost, neighbor, path + [neighbor]))

    return None
