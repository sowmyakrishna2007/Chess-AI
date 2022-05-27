pieces = {"p": 1, "n": 3, "k":0, "q": 9, "r": 5, "b": 3, "-":0}
import random
checkmate = 5000
stalemate = 0
def gen_random(valid_moves):

    return random.choice(valid_moves)

def minmax(player_valid_moves, game_state):
    random.shuffle(player_valid_moves)
    min_score = checkmate
    min_move = None
    for player_move in player_valid_moves:
        game_state.move(player_move)
        opponent_valid_moves = game_state.valid_moves()
        max_score = -checkmate
        for opponent_move in opponent_valid_moves:
            game_state.move(opponent_move)
            opponent_score = score(game_state.board, game_state)
            if opponent_score > max_score:
                max_score = opponent_score
            game_state.undo()
        if max_score < min_score:
            min_score = max_score
            min_move = player_move
        game_state.undo()
    return min_move



def score(board, game_state):
    if game_state.checkmate_status:
        if game_state.white_move:

            return checkmate
        else:
            return -checkmate
    elif game_state.stalemate_status:
        return stalemate
    score = 0
    for row in board:
        for sq in row:
            if sq[1] == "w":
                score += pieces[sq[0]]
            else:
                score -= pieces[sq[0]]
    return score
