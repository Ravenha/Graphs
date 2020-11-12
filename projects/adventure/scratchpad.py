while len(world.rooms) > len(my_visited_rooms):

    for move in traversal_path:
        player.travel(move)
        my_visited_rooms.add(player.current_room)
        room = player.current_room.id
        exits = player.current_room.get_exits()

        for direction in exits:
            try:
                rooms[room]
            except KeyError:
                rooms[room] = {}
                next_room = player.current_room.get_room_in_direction(direction)
                rooms[room].update({direction : next_room.id})

            if direction not in rooms[room]:
                next_room = player.current_room.get_room_in_direction(direction)
                if next_room is not None:
                    player.travel(direction)
                    moves.push(direction)
                    traversal_path.append(direction)
                    most_recent = direction

                    try:
                        rooms[room]
                        rooms[room].update({direction : next_room.id})
                    except KeyError:
                        rooms[room] = {direction : next_room.id}

                    print('You made it to this spot!')

                    traverse(player, rooms, most_recent)


def cleanup(player, rooms):
    for step in traversal_path:
        player.travel(step)
        traversal_path.append(step)

        room = player.current_room.id
        exits = player.current_room.get_exits()

        unused = []

        for exit in exits:
            try:
                rooms[room][exit]
            except KeyError:
                unused.append(exit)

        if len(unused) == 0:
            pass
        else:
            player.travel(unused[0])
            moves.push(unused[0])
            traversal_path.append(unused[0])

            last_move = moves.pop()
            reverse = direction_inverse(last_move)
            player.travel(reverse)
            traversal_path.append(reverse)


def get_eight(player, rooms):
    steps = ['s', 'w', 'e', 'n']

    for step in steps:
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



# Trying to get the missing 3 without messing everything else up
if (room == 234 or room == 0) and (most_recent == 'e' and 's' in exits):
    next_room = player.current_room.get_room_in_direction('s')
    if next_room not in my_visited_rooms:
        direction = 's'
    elif next_room in my_visited_rooms:
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


elif most_recent == 'e':
    if 's' in exits:
        next_room = player.current_room.get_room_in_direction('s')
        if next_room not in my_visited_rooms:
            direction = 's'

        else:
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

    else:
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
