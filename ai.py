"""
ai.py
The AI brain. Uses the Minimax algorithm with alpha-beta pruning
to find the optimal move. Tic Tac Toe is small enough that the
AI can search the full game tree, making it unbeatable.

The AI can play as either X or O — the symbol it plays is passed in.
"""

from game import opponent


# Scoring constants for terminal states.
# Depth is subtracted (for the maximizer) so the AI prefers faster wins
# and slower losses, leading to more "natural" play.
WIN_SCORE = 10
LOSS_SCORE = -10
DRAW_SCORE = 0


def evaluate(game, ai_symbol):
    """Score a terminal position from the AI's perspective."""
    w = game.winner()
    if w == ai_symbol:
        return WIN_SCORE
    if w == opponent(ai_symbol):
        return LOSS_SCORE
    return DRAW_SCORE   # Draw or non-terminal (caller should check is_over)


def minimax(game, depth, is_maximizing, alpha, beta, ai_symbol):
    """
    Recursive minimax with alpha-beta pruning.

    - `is_maximizing` = True means it's the AI's turn (trying to maximize score).
    - `is_maximizing` = False means it's the opponent's turn (trying to minimize).
    - `alpha` and `beta` are the best scores currently guaranteed for the
      maximizer and minimizer respectively. They let us prune branches
      that cannot possibly affect the final decision.
    - `ai_symbol` is whichever of X / O the AI is playing as.

    The depth adjustment makes the AI prefer the fastest win and the
    longest possible loss, so it doesn't dawdle when it has already won.
    """
    if game.is_over():
        score = evaluate(game, ai_symbol)
        if score > 0:
            return score - depth   # prefer quicker wins
        if score < 0:
            return score + depth   # prefer slower losses
        return 0

    human_symbol = opponent(ai_symbol)

    if is_maximizing:
        best = float("-inf")
        for move in game.available_moves():
            game.make_move(move, ai_symbol)
            value = minimax(game, depth + 1, False, alpha, beta, ai_symbol)
            game.undo_move(move)
            best = max(best, value)
            alpha = max(alpha, best)
            if beta <= alpha:
                break   # beta cutoff: minimizer wouldn't allow this path
        return best
    else:
        best = float("inf")
        for move in game.available_moves():
            game.make_move(move, human_symbol)
            value = minimax(game, depth + 1, True, alpha, beta, ai_symbol)
            game.undo_move(move)
            best = min(best, value)
            beta = min(beta, best)
            if beta <= alpha:
                break   # alpha cutoff: maximizer wouldn't allow this path
        return best


def best_move(game, ai_symbol):
    """
    Find the optimal move for the AI on the current board.
    Returns a cell index 0..8.
    """
    best_score = float("-inf")
    chosen = None

    for move in game.available_moves():
        game.make_move(move, ai_symbol)
        score = minimax(game, 0, False, float("-inf"), float("inf"), ai_symbol)
        game.undo_move(move)

        if score > best_score:
            best_score = score
            chosen = move

    return chosen
