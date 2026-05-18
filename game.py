"""
game.py
Core game state and rules for Tic Tac Toe.
Keeps board state, validates moves, detects winners.

Note: this module is symbol-agnostic. It only knows about 'X', 'O',
and empty cells. The notion of "human" vs "AI" lives in the UI layer,
which can map either symbol to either kind of player.
"""

# Symbol constants
X = "X"
O = "O"
EMPTY = " "


def opponent(player):
    """Return the other symbol."""
    return O if player == X else X


class TicTacToe:
    """Represents a single game of Tic Tac Toe."""

    # All 8 ways to win: 3 rows, 3 columns, 2 diagonals
    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6),              # diagonals
    ]

    def __init__(self, starting_player=X):
        # Board is a flat list of 9 cells indexed 0..8
        # Layout:  0 | 1 | 2
        #          ---------
        #          3 | 4 | 5
        #          ---------
        #          6 | 7 | 8
        self.board = [EMPTY] * 9
        self.current_player = starting_player

    def reset(self, starting_player=X):
        """Start a fresh game."""
        self.board = [EMPTY] * 9
        self.current_player = starting_player

    def swap_player(self):
        """Switch turn between X and O."""
        self.current_player = opponent(self.current_player)

    def available_moves(self):
        """Return indices of all empty cells."""
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def make_move(self, index, player):
        """Place a mark on the board. Returns True if successful."""
        if self.board[index] == EMPTY:
            self.board[index] = player
            return True
        return False

    def undo_move(self, index):
        """Remove a mark from the board (used by Minimax search)."""
        self.board[index] = EMPTY

    def winner(self):
        """
        Return the winner ('X' or 'O'), 'Draw' if board is full with no winner,
        or None if the game is still ongoing.
        """
        for a, b, c in self.WIN_LINES:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if EMPTY not in self.board:
            return "Draw"
        return None

    def winning_line(self):
        """Return the indices of the winning line, or None if no winner yet."""
        for a, b, c in self.WIN_LINES:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return (a, b, c)
        return None

    def is_over(self):
        """True if the game has ended (win or draw)."""
        return self.winner() is not None
