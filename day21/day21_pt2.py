from copy import deepcopy
import time

def generate_poss():
    poss = dict()
    for i in range(1,4):
        for j in range(1,4):
            for k in range(1,4):
                roll = i + j + k
                if roll in poss:
                    poss[roll] += 1
                else:
                    poss[roll] = 1
    return poss

POSS_ROLLS_AND_FREQ = generate_poss()

def move_forward(spot, steps):
    return (spot-1 + steps) % 10 + 1

def play_and_score(p1_start, p2_start, winning_score):
    # each world represented by p1_points, p1_pos, p2_points, p2_pos, p1_is_next
    # worlds maps a unique world to the number of instances of it
    worlds = {(0, p1_start, 0, p2_start, True): 1}
    p1_win_count = 0
    p2_win_count = 0
    while len(worlds) > 0:
        world, count = worlds.popitem()
        (p1_points, p1_pos, p2_points, p2_pos, p1_is_next) = world
        for poss_roll, freq in POSS_ROLLS_AND_FREQ.items():
            num_worlds_with_play = count * freq
            if p1_is_next:
                p1_updated_pos = move_forward(p1_pos, poss_roll)
                p1_updated_points = p1_points + p1_updated_pos
                new_world = (p1_updated_points, p1_updated_pos, p2_points, p2_pos, False)
            else:
                p2_updated_pos = move_forward(p2_pos, poss_roll)
                p2_updated_points = p2_points + p2_updated_pos
                new_world = (p1_points, p1_pos, p2_updated_points, p2_updated_pos, True)
            if new_world[0] >= winning_score:
                # p1 wins
                p1_win_count += num_worlds_with_play
            elif new_world[2] >= winning_score:
                # p2 wins
                p2_win_count += num_worlds_with_play
            else:
                # keep going
                if new_world in worlds:
                    worlds[new_world] += num_worlds_with_play
                else:
                    worlds[new_world] = num_worlds_with_play
    return max(p1_win_count, p2_win_count)

def main():
    assert move_forward(4, 6) == 10
    assert move_forward(8, 15) == 3
    assert move_forward(10, 24) == 4

    # player 1 in pos 4, player 2 in pos 8
    assert play_and_score(4, 8, 21) == 444356092776315

    # player 1 in pos 9, player 2 in pos 10
    start = time.perf_counter()
    print(play_and_score(9, 10, 21))
    print(time.perf_counter() - start)

if __name__ == "__main__":
	main()
