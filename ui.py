"""
ui.py
Tkinter GUI for the Tic Tac Toe game.

Two screens:
  1. Setup screen — choose mode (Human vs AI or Human vs Human),
     pick your symbol, pick who goes first, choose AI difficulty.
  2. Game screen — the 3x3 board, status, scoreboard, controls.

The game logic and AI modules are symbol-agnostic; this layer
decides which symbol belongs to which kind of player.
"""

import tkinter as tk
from tkinter import font as tkfont
import random

from game import TicTacToe, X, O, EMPTY, opponent
from ai import best_move


# -------- Color palette (dark theme) --------
BG_MAIN      = "#1e1e2e"   # background
BG_PANEL     = "#181825"   # darker panel
BG_CELL      = "#313244"   # empty cell
BG_CELL_HOV  = "#45475a"   # cell on hover
BG_WIN       = "#a6e3a1"   # winning cell highlight
FG_TEXT      = "#cdd6f4"   # primary text
FG_MUTED     = "#7f849c"   # secondary text
FG_X         = "#89b4fa"   # X color - blue
FG_O         = "#f38ba8"   # O color - pink
FG_ACCENT    = "#fab387"   # accent (titles, scores)
BG_SELECTED  = "#fab387"   # selected toggle background


# -------- Game modes --------
MODE_PVE = "Human vs AI"
MODE_PVP = "Human vs Human"


class TicTacToeUI:
    """Main application controller. Handles both screens."""

    def __init__(self, root):
        self.root = root

        # Game configuration (set on the setup screen, used on the game screen)
        self.mode = MODE_PVE
        self.human_symbol = X         # in PvE mode, the symbol the human plays
        self.starting_symbol = X      # which symbol moves first this round
        self.difficulty = "Hard"

        # Game state (created when starting a game)
        self.game = None
        self.buttons = []
        self.scores = {"left": 0, "right": 0, "draw": 0}
        self.locked = False

        self._configure_window()
        self._build_fonts()

        # Top-level container; screens are swapped in and out of this frame.
        self.container = tk.Frame(self.root, bg=BG_MAIN)
        self.container.pack(fill="both", expand=True)

        self._show_setup_screen()

    # ---------------- window setup ----------------

    def _configure_window(self):
        self.root.title("AI Tic Tac Toe — Minimax")
        self.root.configure(bg=BG_MAIN)

        # Allow free resizing and maximizing.
        # The minsize prevents the window from being squashed unusably small.
        self.root.resizable(True, True)
        self.root.minsize(440, 560)

        # Default window size, centered on screen.
        # Kept compact so everything fits even on smaller laptop displays.
        w, h = 500, 660
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_fonts(self):
        self.font_title  = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.font_status = tkfont.Font(family="Segoe UI", size=12)
        self.font_cell   = tkfont.Font(family="Segoe UI", size=36, weight="bold")
        self.font_score  = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.font_small  = tkfont.Font(family="Segoe UI", size=10)
        self.font_label  = tkfont.Font(family="Segoe UI", size=11, weight="bold")

    # ---------------- screen swapping ----------------

    def _clear_container(self):
        for child in self.container.winfo_children():
            child.destroy()

    # ================================================================
    #                        SETUP SCREEN
    # ================================================================

    def _show_setup_screen(self):
        self._clear_container()

        # State for the form (initialised from current config)
        self._setup_mode = tk.StringVar(value=self.mode)
        self._setup_symbol = tk.StringVar(value=self.human_symbol)
        self._setup_first = tk.StringVar(value=self.starting_symbol)
        self._setup_difficulty = tk.StringVar(value=self.difficulty)

        # Title
        tk.Label(self.container, text="TIC  TAC  TOE",
                 bg=BG_MAIN, fg=FG_ACCENT, font=self.font_title
                 ).pack(pady=(28, 4))
        tk.Label(self.container, text="Game Setup",
                 bg=BG_MAIN, fg=FG_MUTED, font=self.font_small
                 ).pack(pady=(0, 22))

        # Mode chooser
        self._build_toggle_row(
            "Mode",
            self._setup_mode,
            [MODE_PVE, MODE_PVP],
            on_change=self._on_mode_change,
        )

        # Symbol chooser (only shown in PvE mode)
        self._symbol_row = self._build_toggle_row(
            "Your symbol",
            self._setup_symbol,
            [X, O],
        )

        # Who goes first
        self._build_toggle_row(
            "Goes first",
            self._setup_first,
            [X, O],
        )

        # Difficulty (only in PvE mode)
        self._difficulty_row = self._build_toggle_row(
            "AI difficulty",
            self._setup_difficulty,
            ["Easy", "Medium", "Hard"],
        )

        # Initial visibility based on mode
        self._on_mode_change()

        # Start button
        start_btn = tk.Button(
            self.container,
            text="Start Game",
            bg=FG_ACCENT, fg=BG_MAIN,
            activebackground="#f9c89a", activeforeground=BG_MAIN,
            relief="flat", bd=0, cursor="hand2",
            font=self.font_score, padx=30, pady=10,
            command=self._start_game,
        )
        start_btn.pack(pady=(28, 0))

        tk.Label(self.container,
                 text="Powered by the Minimax Algorithm",
                 bg=BG_MAIN, fg=FG_MUTED, font=self.font_small
                 ).pack(side="bottom", pady=18)

    def _build_toggle_row(self, label, variable, options, on_change=None):
        """
        Build a labeled row of toggle buttons. Returns the row frame so
        it can be hidden/shown later.
        """
        row = tk.Frame(self.container, bg=BG_MAIN)
        row.pack(pady=10)

        tk.Label(row, text=label, bg=BG_MAIN, fg=FG_MUTED,
                 font=self.font_label, width=14, anchor="e"
                 ).pack(side="left", padx=(0, 12))

        # Track buttons so we can restyle them when selection changes
        button_refs = {}

        def select(value):
            variable.set(value)
            for v, b in button_refs.items():
                if v == value:
                    b.config(bg=BG_SELECTED, fg=BG_MAIN)
                else:
                    b.config(bg=BG_PANEL, fg=FG_TEXT)
            if on_change:
                on_change()

        for opt in options:
            is_selected = (variable.get() == opt)
            btn = tk.Button(
                row, text=opt,
                bg=BG_SELECTED if is_selected else BG_PANEL,
                fg=BG_MAIN if is_selected else FG_TEXT,
                activebackground=BG_CELL_HOV, activeforeground=FG_TEXT,
                relief="flat", bd=0, cursor="hand2",
                font=self.font_small, padx=14, pady=6,
                command=lambda v=opt: select(v),
            )
            btn.pack(side="left", padx=3)
            button_refs[opt] = btn

        return row

    def _on_mode_change(self):
        """Show/hide rows that only apply to PvE mode."""
        if self._setup_mode.get() == MODE_PVP:
            self._symbol_row.pack_forget()
            self._difficulty_row.pack_forget()
        else:
            # Re-pack in original order (after the mode row)
            self._symbol_row.pack(pady=10)
            # The "goes first" row is already packed; put difficulty after it
            self._difficulty_row.pack(pady=10)

    def _start_game(self):
        """Read the form and switch to the game screen."""
        self.mode = self._setup_mode.get()
        self.human_symbol = self._setup_symbol.get()
        self.starting_symbol = self._setup_first.get()
        self.difficulty = self._setup_difficulty.get()
        self.scores = {"left": 0, "right": 0, "draw": 0}
        self._show_game_screen()

    # ================================================================
    #                        GAME SCREEN
    # ================================================================

    def _show_game_screen(self):
        self._clear_container()
        self.game = TicTacToe(starting_player=self.starting_symbol)
        self.locked = False
        self.buttons = []

        # Title
        tk.Label(self.container, text="TIC  TAC  TOE",
                 bg=BG_MAIN, fg=FG_ACCENT, font=self.font_title
                 ).pack(pady=(14, 2))

        # Subtitle shows the current matchup
        if self.mode == MODE_PVE:
            ai_sym = opponent(self.human_symbol)
            subtitle = f"You: {self.human_symbol}   ·   AI: {ai_sym}   ·   {self.difficulty}"
        else:
            subtitle = "Two players — take turns"
        tk.Label(self.container, text=subtitle,
                 bg=BG_MAIN, fg=FG_MUTED, font=self.font_small
                 ).pack(pady=(0, 8))

        # Status line
        self.status_label = tk.Label(
            self.container, text="", bg=BG_MAIN, fg=FG_TEXT, font=self.font_status
        )
        self.status_label.pack(pady=(0, 8))

        # Game grid
        grid_frame = tk.Frame(self.container, bg=BG_PANEL, padx=8, pady=8)
        grid_frame.pack()
        for i in range(9):
            btn = tk.Button(
                grid_frame, text="",
                font=self.font_cell,
                width=3, height=1,
                bg=BG_CELL, fg=FG_TEXT,
                activebackground=BG_CELL_HOV,
                relief="flat", bd=0, cursor="hand2",
                command=lambda i=i: self._on_cell_click(i),
            )
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=4, ipadx=10, ipady=4)
            btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self._on_hover(b, False))
            self.buttons.append(btn)

        # Scoreboard
        # In PvE: shows You / Draw / AI
        # In PvP: shows X / Draw / O
        self._build_scoreboard()

        # Controls: New Game (same settings) and Home (back to setup screen)
        controls = tk.Frame(self.container, bg=BG_MAIN)
        controls.pack(pady=(10, 12))

        self.new_game_btn = tk.Button(
            controls, text="↻  Play Again",
            bg=FG_ACCENT, fg=BG_MAIN,
            activebackground="#f9c89a", activeforeground=BG_MAIN,
            relief="flat", bd=0, cursor="hand2",
            font=self.font_score, padx=20, pady=8,
            command=self._reset_game,
        )
        self.new_game_btn.pack(side="left", padx=6)

        self.home_btn = tk.Button(
            controls, text="🏠  Home",
            bg=BG_PANEL, fg=FG_TEXT,
            activebackground=BG_CELL_HOV, activeforeground=FG_TEXT,
            relief="flat", bd=0, cursor="hand2",
            font=self.font_score, padx=20, pady=8,
            command=self._show_setup_screen,
        )
        self.home_btn.pack(side="left", padx=6)

        # Start the first turn (AI may move immediately if it goes first in PvE)
        self._begin_turn()

    def _build_scoreboard(self):
        """
        Build the three score cells.
        In PvE: left=You, right=AI.
        In PvP: left=X player, right=O player.
        """
        score_frame = tk.Frame(self.container, bg=BG_MAIN)
        score_frame.pack(pady=(12, 4))

        if self.mode == MODE_PVE:
            left_label, left_color = "YOU", FG_X if self.human_symbol == X else FG_O
            right_label, right_color = "AI", FG_O if self.human_symbol == X else FG_X
        else:
            left_label, left_color = f"PLAYER {X}", FG_X
            right_label, right_color = f"PLAYER {O}", FG_O

        cells = [
            ("left",  left_label,  left_color),
            ("draw",  "DRAW",      FG_MUTED),
            ("right", right_label, right_color),
        ]

        self.score_labels = {}
        for key, label, color in cells:
            cell = tk.Frame(score_frame, bg=BG_PANEL, padx=14, pady=8)
            cell.pack(side="left", padx=6)
            tk.Label(cell, text=label, bg=BG_PANEL, fg=color,
                     font=self.font_small).pack()
            num = tk.Label(cell, text=str(self.scores[key]),
                           bg=BG_PANEL, fg=FG_TEXT, font=self.font_score)
            num.pack()
            self.score_labels[key] = num

    # ---------------- turn flow ----------------

    def _begin_turn(self):
        """
        Called at the start of each turn. In PvE, if it's the AI's turn,
        the AI moves automatically after a short delay.
        """
        if self.game.is_over():
            return

        if self.mode == MODE_PVE and self.game.current_player != self.human_symbol:
            # AI's turn
            self.locked = True
            self._update_status("AI is thinking…")
            self.root.after(400, self._ai_move)
        else:
            # Human's turn (PvE) or some human's turn (PvP)
            self.locked = False
            self._update_status(self._human_prompt())

    def _human_prompt(self):
        """The status text shown while waiting for a human move."""
        if self.mode == MODE_PVE:
            return f"Your turn ({self.human_symbol})"
        return f"Player {self.game.current_player}'s turn"

    def _on_hover(self, btn, entering):
        if btn["text"] == "" and not self.locked:
            btn.config(bg=BG_CELL_HOV if entering else BG_CELL)

    def _on_cell_click(self, index):
        """Handle a click on a board cell."""
        if self.locked or self.game.board[index] != EMPTY or self.game.is_over():
            return

        # In PvE, the human only plays their own symbol.
        # In PvP, the human plays whichever symbol is up next.
        symbol = self.game.current_player
        self.game.make_move(index, symbol)
        self._render_cell(index, symbol)

        if self._check_end():
            return

        self.game.swap_player()
        self._begin_turn()

    def _ai_move(self):
        """Compute and play the AI's move (PvE mode only)."""
        if self.game.is_over():
            self.locked = False
            return

        ai_sym = opponent(self.human_symbol)
        move = self._choose_ai_move(ai_sym)
        self.game.make_move(move, ai_sym)
        self._render_cell(move, ai_sym)

        if self._check_end():
            return

        self.game.swap_player()
        self._begin_turn()

    def _choose_ai_move(self, ai_sym):
        """
        Pick a move based on difficulty.
        - Easy:   always random
        - Medium: 50% optimal, 50% random
        - Hard:   always optimal (unbeatable)
        """
        moves = self.game.available_moves()
        if self.difficulty == "Easy":
            return random.choice(moves)
        if self.difficulty == "Medium" and random.random() < 0.5:
            return random.choice(moves)
        return best_move(self.game, ai_sym)

    # ---------------- rendering ----------------

    def _render_cell(self, index, symbol):
        btn = self.buttons[index]
        color = FG_X if symbol == X else FG_O
        btn.config(text=symbol, fg=color, bg=BG_CELL,
                   disabledforeground=color, state="disabled")

    def _update_status(self, text):
        self.status_label.config(text=text)

    def _highlight_winning_line(self, line):
        for i in line:
            self.buttons[i].config(bg=BG_WIN, disabledforeground=BG_MAIN)

    def _check_end(self):
        """If the game ended, update UI and scores. Returns True if ended."""
        result = self.game.winner()
        if result is None:
            return False

        for btn in self.buttons:
            btn.config(state="disabled")
        self.locked = True

        if result == "Draw":
            self.scores["draw"] += 1
            self._update_status("It's a draw!")
        else:
            self._highlight_winning_line(self.game.winning_line())
            self._update_status(self._win_message(result))
            # Update score: in PvE we credit human/AI; in PvP we credit X/O.
            if self.mode == MODE_PVE:
                if result == self.human_symbol:
                    self.scores["left"] += 1     # human's column
                else:
                    self.scores["right"] += 1    # AI's column
            else:
                if result == X:
                    self.scores["left"] += 1
                else:
                    self.scores["right"] += 1

        self._refresh_scoreboard()
        return True

    def _win_message(self, winner_symbol):
        if self.mode == MODE_PVE:
            if winner_symbol == self.human_symbol:
                return "You win! 🎉"
            return "AI wins!"
        return f"Player {winner_symbol} wins! 🎉"

    def _refresh_scoreboard(self):
        for key, lbl in self.score_labels.items():
            lbl.config(text=str(self.scores[key]))

    # ---------------- reset ----------------

    def _reset_game(self):
        """Reset the board for another round with the same settings."""
        # Alternate who starts each round? For simplicity we keep the same
        # starting symbol chosen at setup. (Easy to change to alternating.)
        self.game.reset(starting_player=self.starting_symbol)
        for btn in self.buttons:
            btn.config(text="", bg=BG_CELL, fg=FG_TEXT,
                       state="normal", disabledforeground=FG_TEXT)
        self._begin_turn()