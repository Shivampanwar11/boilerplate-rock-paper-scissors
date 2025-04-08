# RPS.py

opponent_history = []
my_history = []
round_count = 0

# Mapping of what beats what
beats = {'R': 'P', 'P': 'S', 'S': 'R'}

def player(prev_play):
    global opponent_history, my_history, round_count

    if prev_play:
        opponent_history.append(prev_play)

    round_count += 1

    if round_count == 1:
        my_history.append("R")
        return "R"

    # Counter Quincy (always R)
    if all(move == "R" for move in opponent_history):
        move = "P"
        my_history.append(move)
        return move

    # Pattern detection: use last 3 moves to predict next
    guess = predict_with_sequence(opponent_history)

    # If prediction fails, fall back to frequency
    if not guess:
        if round_count < 100:
            guess = most_frequent(opponent_history[-5:])
        else:
            guess = most_frequent(opponent_history)

    counter = beats.get(guess, "R")
    my_history.append(counter)
    return counter

def most_frequent(moves):
    if not moves:
        return "R"
    return max(set(moves), key=moves.count)

def predict_with_sequence(history):
    if len(history) < 3:
        return None

    last_seq = ''.join(history[-3:])
    patterns = {}

    for i in range(len(history) - 3):
        seq = ''.join(history[i:i+3])
        next_move = history[i+3]
        if seq == last_seq:
            if next_move in patterns:
                patterns[next_move] += 1
            else:
                patterns[next_move] = 1

    if not patterns:
        return None

    return max(patterns, key=patterns.get)
