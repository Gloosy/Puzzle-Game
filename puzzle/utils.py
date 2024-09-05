def find_neighbors_static(state, size):
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
