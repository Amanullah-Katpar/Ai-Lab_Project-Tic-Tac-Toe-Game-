"""
main.py
Entry point for the AI Tic Tac Toe game.
Run this file to launch the GUI:
    python main.py
"""

import tkinter as tk
from ui import TicTacToeUI


def main():
    root = tk.Tk()
    TicTacToeUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
