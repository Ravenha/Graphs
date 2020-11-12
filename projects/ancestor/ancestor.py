from util import Stack, Queue

def get_neighbors(node, ancestors):
    cache = {}

    for ancestor in ancestors:
        if ancestor[0] in cache:
            cache[ancestor[0]].append(ancestor[1])
        else:
            cache[ancestor[0]] = []
            cache[ancestor[0]].append(ancestor[1])

    parents = []

    for parent in cache:
        children = cache[parent]
        for child in children:
            if child == node:
                parents.append(parent)

    if len(parents) == 0:
        return -1

    return parents

def earliest_ancestor(ancestors, starting_node):
    # Create a queue with our first node
    q = Queue()
    q.enqueue([starting_node])

    # Empty set for tracking what we've visited
    visited = set()

    # Create a dictionary where we'll track path lengths and paths
    paths = {}

    # As long as something is in the queue
    while q.size() > 0:
        # Grab the first thing in the queue
        path = q.dequeue()
        # Make sure it's just an integer
        current_node = path[-1]

        # As long as we haven't addressed this node before
        if current_node not in visited:
            # Add it to visited
            visited.add(current_node)

            # Get all parents of the node
            parents = get_neighbors(current_node, ancestors)

            # If it has no parents, return -1
            if parents == -1:
                return -1

            # For each parent
            for parent in parents:
                # Start a new path
                new_path = path.copy()
                # Add the parent to the path
                new_path.append(parent)
                # Get the parent's parents
                grandparents = get_neighbors(parent, ancestors)

                # If there are no "grandparents"
                if grandparents == -1:
                    # Make sure to account for duplicate path lengths
                    # Then add new_path to the paths dict
                    if len(new_path) in paths:
                        paths[len(new_path)].append(new_path)
                    else:
                        paths[len(new_path)] = []
                        paths[len(new_path)].append(new_path)
                # If there is a grandparent
                else:
                    # Add the grandparent to the new_path
                    new_path.append(grandparents[0])
                    # Add new_path to paths dict
                    paths[len(new_path)] = new_path

            # Get the largest path length
            greatest_index = max([length for length in paths])

            # If two ancestors had the same length of path
            if type(paths[greatest_index][0]) is not int and len(paths[greatest_index][0]) > 1:
                # Get both of the ancestors
                ancestors = []
                for ancestor in paths[greatest_index][0]:
                    ancestors.append(ancestor)
                # And return the smallest one
                return min(ancestors)
            # If it's just an integer, not a list
            elif type(paths[greatest_index][0]) is int:
                # Return the last integer
                return paths[greatest_index][-1]
            # Otherwise, return the last item in the single list
            else:
                return paths[greatest_index][0][-1]

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(test_ancestors, 6))
