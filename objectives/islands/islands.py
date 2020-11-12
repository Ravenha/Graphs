def get_neighbors(node, islands):
    row, col = node

    neighbors = []

    step_north = step_south = step_west = step_east = None

    if row > 0:
        step_north = row - 1

    if row < (len(islands) - 1):
        step_south = row + 1

    if col > 0:
        step_west = col - 1

    if col < (len(islands) - 1):
        step_east = col + 1

    if step_north is not None and islands[step_north][col] == 1:
        coordinate = (step_north, col)
        neighbors.append(coordinate)

    if step_south is not None and islands[step_south][col] == 1:
        coordinate = (step_south, col)
        neighbors.append(coordinate)

    if step_west is not None and islands[row][step_west] == 1:
        coordinate = (row, step_west)
        neighbors.append(coordinate)

    if step_east is not None and islands[row][step_east] == 1:
        coordinate = (row, step_east)
        neighbors.append(coordinate)

    return neighbors

def dft_recursive(node, visited, islands):
    if node not in visited:
        visited.add(node)

        neighbors = get_neighbors(node, islands)

        for neighbor in neighbors:
            dft_recursive(neighbor, visited, islands)

def islands_counter(islands):
    total_islands = 0
    visited = set()
    # iterate over the matrix
    for row in range(len(islands)):
        for col in range(len(islands)):
            node = (row, col)
            # When we hit a 1
            if islands[row][col] == 1 and node not in visited:
                ## Increment an islands counter
                total_islands += 1
                ## run DFT on it
                dft_recursive(node, visited, islands)

    return total_islands


islands = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]

print(islands_counter(islands))
