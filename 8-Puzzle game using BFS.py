import numpy as np
from collections import deque

#Finds the position of the empty tile (0).
def find_empty(state):
    for i in range(3):      #row index
        for j in range(3):  #column index
            if state[i][j] == 0:
                return i, j

#Generates child states by moving the empty tile.
def generate_children(state):
    children = []
    i, j = find_empty(state)
    moves = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    for x, y in moves:
        if 0 <= x < 3 and 0 <= y < 3:
            new_state = state.copy()
            new_state[i][j], new_state[x][y] = new_state[x][y], new_state[i][j]
            children.append(new_state)
    return children

#Checks if the current state is the goal state.
def is_goal(state, goal):
    return np.array_equal(state, goal)

#Solves the 8-puzzle using breadth-first search.
def breadth_first_search(initial, goal):
    queue = deque([(initial, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        if is_goal(state, goal):
            return path
        if str(state) not in visited:
            visited.add(str(state))
            for child in generate_children(state):
                queue.append((child, path + [child]))
    return None

#Initialize the initial and goal state
initial = np.array([[3, 0, 7], [2, 8, 1], [6, 4, 5]])
goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

'''
#User input the initial state
def get_initial_state():
    """Gets the initial state from user input."""
    initial = []
    print("Enter the initial state:")
    for _ in range(3):
        row = list(map(int, input().split()))
        initial.append(row)
    return np.array(initial)

#User input the goal state
def get_goal_state():
    """Gets the goal state from user input."""
    goal = []
    print("Enter the goal state:")
    for _ in range(3):
        row = list(map(int, input().split()))
        goal.append(row)
    return np.array(goal)

initial = get_initial_state()
goal = get_goal_state()
'''

#Result
solution = breadth_first_search(initial, goal)
if solution:
    for state in solution:
        for row in state:
            print(' '.join(map(str, row)))
        print()
else:
    print("\n\nNo solution found.")

print (breadth_first_search)
