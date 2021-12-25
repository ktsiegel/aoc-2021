from copy import deepcopy
import heapq as hq
from json import dumps

# hallway indices are as follows
#############
#01x3x5x7x9*# * indicates 10
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
#  0 1 2 3 # room indexes

ROOM_TO_AMPHIPOD_DEST_MAP = {0:'A',1:'B',2:'C',3:'D'}
ROOM_CAPACITY = 4

def room_to_hallway(room_idx):
    return room_idx * 2 + 2 # hallway index of spot directly outside of room

def amphipod_multiple(amphipod):
    if amphipod == 'A':
        return 1
    elif amphipod == 'B':
        return 10
    elif amphipod == 'C':
        return 100
    else:
        assert amphipod == 'D'
        return 1000

def calc_move_out_of_room_energy(amphipod, room_idx, occupancy_of_room_before_move, hallway_dest):
    # move into hallway directly outside of room
    move_count = ROOM_CAPACITY + 1 - occupancy_of_room_before_move
    move_count += abs(room_to_hallway(room_idx) - hallway_dest)
    return move_count * amphipod_multiple(amphipod)

def calc_move_into_room_energy(amphipod, room_idx, occupancy_of_room_before_move, hallway_src):
    # move into hallway directly outside of room
    move_count = abs(room_to_hallway(room_idx) - hallway_src) + (ROOM_CAPACITY - occupancy_of_room_before_move)
    return move_count * amphipod_multiple(amphipod)

def has_alien_amphipod(room, room_idx):
    home_amphipod = ROOM_TO_AMPHIPOD_DEST_MAP[room_idx]
    for a in room:
        if a != home_amphipod:
            return True
    return False

def all_amphipods_are_home(rooms):
    for r in range(len(rooms)):
        room = rooms[r]
        if len(room) < ROOM_CAPACITY:
            return False
        if has_alien_amphipod(room, r):
            return False
    return True

def is_hallway_path(spot):
    return spot == 'x' or spot == ''

def solve(initial_rooms):
    viable_worlds = []
    searched = set()
    # On each step, either an amphipod moves out of a room or it moves into a valid room
    initial_hallway = ['', '', 'x', '', 'x', '', 'x', '', 'x', '', '']
    viable_worlds.append([0, initial_rooms, initial_hallway]) # points, energy spent, room occupancy, hallway spots
    while len(viable_worlds) > 0:
        w = hq.heappop(viable_worlds)
        [energy, rooms, hallway] = w
        wdump = dumps([rooms, hallway])
        if wdump in searched:
            continue
        searched.add(wdump)
        if all_amphipods_are_home(rooms):
            return energy
        # option 1: move an amphipod out of a room. there are <= 4 possibilities of source
        # and <= 7 possibilities of dest
        for r in range(len(rooms)):
            if len(rooms[r]) == 0:
                # room has no amphipods
                continue
            hallway_idx = room_to_hallway(r)
            left_a = hallway_idx
            right_a = hallway_idx
            while left_a >= 0 and is_hallway_path(hallway[left_a]):
                left_a -= 1
            while right_a < len(hallway) and is_hallway_path(hallway[right_a]):
                right_a += 1
            for h in range(left_a + 1, right_a):
                if hallway[h] != '':
                    continue
                new_rooms = deepcopy(rooms)
                new_hallway = deepcopy(hallway)
                # only move the amphipod in the room nearest the entrance
                moving_amphipod = new_rooms[r].pop(0)
                new_hallway[h] = moving_amphipod
                hq.heappush(viable_worlds, [energy + calc_move_out_of_room_energy(moving_amphipod, r, len(rooms[r]), h), new_rooms, new_hallway])
        # option 2: move an amphipod out of the hallway into a room. There are <=4 possibilities, one for each room.
        for r in range(len(rooms)):
            room = rooms[r]
            assert len(room) <= ROOM_CAPACITY
            if len(room) == ROOM_CAPACITY:
                # room is full
                continue
            if has_alien_amphipod(room, r):
                # room has an alien amphipod, so can't fill the room with the right amphipods
                continue
            # check if either of the nearest two amphipods on either side of the hallway spot outside the room
            # can fill the room (aka is a home amphipod)
            home_amphipod = ROOM_TO_AMPHIPOD_DEST_MAP[r]
            hallway_idx = room_to_hallway(r)
            left_a = hallway_idx
            right_a = hallway_idx
            while left_a >= 0 and is_hallway_path(hallway[left_a]):
                left_a -= 1
            while right_a < len(hallway) and is_hallway_path(hallway[right_a]):
                right_a += 1
            if left_a >= 0 and hallway[left_a] == home_amphipod:
                # can move this amphipod into the room
                new_rooms = deepcopy(rooms)
                new_hallway = deepcopy(hallway)
                new_rooms[r].insert(0, home_amphipod)
                new_hallway[left_a] = ''
                hq.heappush(viable_worlds, [energy + calc_move_into_room_energy(home_amphipod, r, len(rooms[r]), left_a), new_rooms, new_hallway])
            if right_a < len(hallway) and hallway[right_a] == home_amphipod:
                # can move this amphipod into the room
                new_rooms = deepcopy(rooms)
                new_hallway = deepcopy(hallway)
                new_rooms[r].insert(0, home_amphipod)
                new_hallway[right_a] = ''
                hq.heappush(viable_worlds, [energy + calc_move_into_room_energy(home_amphipod, r, len(rooms[r]), right_a), new_rooms, new_hallway])

def main():
    # the list of rooms and occupants, with the top amphipod (nearest the entrance) listed first
    example = [['B','D','D','A'],['C','C','B','D'],['B','B','A','C'],['D','A','C','A']]
    # print(solve(example))

    problem = [['C','D','D','D'],['C','C','B','D'],['A','B','A','B'],['B','A','C','A']]
    print(solve(problem))


if __name__ == "__main__":
	main()





























