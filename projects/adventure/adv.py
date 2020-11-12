from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def direction_inverse(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    else:
        return 'e'

def weird_inverse(direction):
    if direction == 's':
        return 'e'
    elif direction == 'e':
        return 's'
    elif direction == 'w':
        return 's'

moves = Stack()
my_visited_rooms = set()
rooms = {}
rooms_list = []
most_recent = None

def traverse(player, rooms, most_recent):
    room = player.current_room.id
    exits = player.current_room.get_exits()
    my_visited_rooms.add(room)

    for direction in exits:

        try:
            rooms[room][direction]
            pass

        except KeyError:

            rooms_list.append(room)

            next_room = player.current_room.get_room_in_direction(direction)

            # South and west is the hard combo, do that first
            if most_recent == 's' and 'w' in exits:
                next_room = player.current_room.get_room_in_direction('w')
                direction = 'w'

            # West then north was another trouble area
            elif most_recent == 'w' and 'n' in exits:
                next_room = player.current_room.get_room_in_direction('n')
                direction = 'n'

            # If our last move was to the south/east/west, keep going that way
            elif most_recent == 's' or most_recent == 'e' or most_recent == 'w':
                next_room = player.current_room.get_room_in_direction(most_recent)

                # If that doesn't work, try going the other "weird" direction
                if next_room == None:
                    test = weird_inverse(most_recent)
                    next_room = player.current_room.get_room_in_direction(test)

                    if next_room == None:
                        next_room = player.current_room.get_room_in_direction(direction)

                    elif next_room.id in my_visited_rooms:
                        if 'n' in exits:
                            direction = 'n'
                            next_room = player.current_room.get_room_in_direction('n')
                        elif 's' in exits:
                            direction = 's'
                            next_room = player.current_room.get_room_in_direction('s')

                    else:
                        direction = test

                # If we're heading south and want to go east
                elif next_room.id in my_visited_rooms:
                    test = weird_inverse(most_recent)
                    next_room = player.current_room.get_room_in_direction(test)
                    if next_room != None:
                        direction = test

                    # If both don't work, revert back to the original plan
                    else:
                        next_room = player.current_room.get_room_in_direction(direction)

                else:
                    # If next_room != None
                    # And next_room not in my_visited_rooms
                    direction = most_recent

            # If we just went north, try going west, then try going east
            elif most_recent == 'n':
                next_room = player.current_room.get_room_in_direction('w')
                if next_room != None and next_room not in my_visited_rooms:
                    direction = 'w'
                else:
                    next_room = player.current_room.get_room_in_direction('e')
                    if next_room != None:
                        direction = 'e'
                    else:
                        next_room = player.current_room.get_room_in_direction(direction)

            # Easiest move, let's go forward
            if next_room.id not in my_visited_rooms:
                player.travel(direction)
                moves.push(direction)
                traversal_path.append(direction)
                most_recent = direction

                try:
                    rooms[room]
                    rooms[room].update({direction : next_room.id})
                except KeyError:
                    rooms[room] = {direction : next_room.id}

                return traverse(player, rooms, most_recent)

            # Go backwards
            elif next_room.id in my_visited_rooms and len(world.rooms) > len(my_visited_rooms) and moves.size() > 0:
                last_move = moves.pop()
                reverse = direction_inverse(last_move)
                player.travel(reverse)
                traversal_path.append(reverse)
                most_recent = reverse

                try:
                    rooms[room]
                    rooms[room].update({reverse : player.current_room.id})
                except KeyError:
                    rooms[room] = {reverse : player.current_room.id}

                return traverse(player, rooms, most_recent)

            else:
                direction = 'e'
                player.travel(direction)
                moves.push(direction)
                traversal_path.append(direction)
                most_recent = direction

                try:
                    rooms[room]
                    rooms[room].update({direction : next_room.id})
                except KeyError:
                    rooms[room] = {direction : next_room.id}

                direction = 's'
                player.travel(direction)
                moves.push(direction)
                traversal_path.append(direction)
                most_recent = direction

                try:
                    rooms[room]
                    rooms[room].update({direction : next_room.id})
                except KeyError:
                    rooms[room] = {direction : next_room.id}

                return traverse(player, rooms, most_recent)

            # else:
            #     return "You are ending up here"

def weird_spot(player, rooms):

    from_zero = ['e', 'n', 'n', 'w', 'n', 'n', 'e', 'n']

    for step in from_zero:
        room = player.current_room.id
        exits = player.current_room.get_exits()
        my_visited_rooms.add(room)
        rooms_list.append(room)

        direction = step
        next_room = player.current_room.get_room_in_direction(direction)

        player.travel(direction)
        moves.push(direction)
        traversal_path.append(direction)
        most_recent = direction

        try:
            rooms[room]
            rooms[room].update({direction : next_room.id})
        except KeyError:
            rooms[room] = {direction : next_room.id}

    return traverse(player, rooms, most_recent)

print(traverse(player, rooms, most_recent))
print(weird_spot(player, rooms))

print(rooms_list)
print(len(traversal_path))

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
