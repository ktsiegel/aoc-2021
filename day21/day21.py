from copy import deepcopy

def move_forward(spot, steps):
    return (spot-1 + steps) % 10 + 1

def get_non_winning_score(scores):
    for p in scores.keys():
        if scores[p] < 1000:
            return scores[p]
    return None

def play(game):
    dice_rolls = 0
    scores = dict()
    for [player, _] in game:
        scores[player] = 0

    dice_roll = 1

    while True:
        for i in range(len(game)):
            [player, spot] = game[i]
            player_total_roll = 0
            for j in range(3):
                player_total_roll += dice_roll
                dice_roll += 1
            new_spot = move_forward(spot, player_total_roll)
            game[i][1] = new_spot
            scores[player] += new_spot
            if scores[player] >= 1000:
                return get_non_winning_score(scores), dice_roll-1

def play_and_score(game):
    (losing_player_points, num_dice_rolls) = play(game)
    return losing_player_points * num_dice_rolls

def main():
    assert move_forward(4, 6) == 10
    assert move_forward(8, 15) == 3
    assert move_forward(10, 24) == 4

    # player 1 in pos 4, player 2 in pos 8
    assert play_and_score([[1,4], [2,8]]) == 739785

    # player 1 in pos 9, player 2 in pos 10
    print(play_and_score([[1, 9], [2, 10]]))



if __name__ == "__main__":
	main()
