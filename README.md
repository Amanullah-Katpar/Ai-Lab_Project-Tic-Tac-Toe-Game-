# AI-Based Tic Tac Toe Game

A Python implementation of the classic Tic Tac Toe game featuring an unbeatable AI opponent powered by the **Minimax algorithm** with alpha-beta pruning. The game is built with a polished Tkinter GUI and supports both Human vs AI and Human vs Human modes.

> **Project 18 — Domain:** AI Game Logic  ·  **Concepts:** Minimax Algorithm

---

## Features

- **Human vs AI gameplay** — play against an intelligent computer opponent
- **Human vs Human mode** — play against a friend on the same machine
- **Three difficulty levels** — Easy (random), Medium (mixed), Hard (unbeatable)
- **Choose your symbol** — play as either X or O
- **Pick who goes first** — fully configurable starting player
- **Intelligent moves** — AI uses the Minimax algorithm with alpha-beta pruning for optimal decision-making
- **Polished GUI** — dark-themed, modern interface built entirely with Tkinter (no external dependencies)
- **Live scoreboard** — tracks wins, losses, and draws across multiple rounds
- **Winning highlights** — winning lines light up green when the game ends
- **Resizable window** — supports maximizing and arbitrary resizing

---

## Project Structure

The code is split into four files with clean separation of concerns:

```
tic_tac_toe/
├── main.py     # Entry point — launches the GUI
├── game.py     # Core game state and rules (symbol-agnostic)
├── ai.py       # Minimax algorithm with alpha-beta pruning
└── ui.py       # Tkinter GUI (setup screen + game screen)
```

| File | Responsibility |
|------|----------------|
| `main.py` | Creates the Tk root window and starts the application loop. |
| `game.py` | Manages the board state, validates moves, detects winners and draws. |
| `ai.py` | Implements the Minimax algorithm. Decides the optimal move for the AI. |
| `ui.py` | Builds the setup screen (configuration) and the game screen (board, scoreboard, controls). |

---

## Requirements

- **Python 3.7 or later**
- **Tkinter** — included by default with standard Python installations on Windows and macOS

No third-party packages are required. The entire game uses only Python's standard library.

To verify Python is installed, open a terminal and run:

```bash
python --version
```

---

## How to Run

1. Place all four `.py` files in the same folder.
2. Open a terminal in that folder.
3. Run:

   ```bash
   python main.py
   ```

The setup window will open. Configure your preferences and click **Start Game**.

---

## How to Play

### Setup Screen

When you launch the game, you'll see a configuration screen with the following options:

- **Mode** — Choose between *Human vs AI* or *Human vs Human*
- **Your symbol** — Pick X or O (only shown in Human vs AI mode)
- **Goes first** — Choose whether X or O makes the first move
- **AI difficulty** — Select Easy, Medium, or Hard (only shown in Human vs AI mode)

Click **Start Game** when ready.

### Game Screen

- Click any empty cell to place your mark.
- In Human vs AI mode, the AI moves automatically after your turn.
- In Human vs Human mode, players take alternating turns on the same screen.
- When the game ends, winning cells are highlighted in green.
- Use **↻ Play Again** to start a new round with the same settings.
- Use **🏠 Home** to return to the setup screen and change configuration.

### Winning Conditions

A player wins by placing three of their marks in:
- Any horizontal row
- Any vertical column
- Either of the two diagonals

If all nine cells are filled with no winner, the game is a draw.

---

## How the AI Works

The AI uses the **Minimax algorithm**, a classic decision-making technique used in two-player turn-based games.

### Core Idea

The algorithm assumes both players play optimally:
- The **AI (maximizer)** tries to achieve the highest possible score
- The **opponent (minimizer)** tries to achieve the lowest possible score
- The algorithm alternates between these perspectives as it explores future moves

Before making each move, the AI simulates **every possible continuation of the game**, scores each terminal outcome, and picks the move that leads to the best guaranteed result.

### Scoring

Terminal positions are scored as follows:

| Outcome | Score |
|---------|-------|
| AI wins | +10 |
| Human wins | −10 |
| Draw | 0 |

The score is also adjusted by search depth so the AI prefers **faster wins** and **slower losses**, leading to more natural-looking play.

### Optimizations

- **Alpha-beta pruning** — Skips branches of the game tree that cannot affect the final decision, speeding up the search significantly.
- **Symbol-agnostic design** — The AI module accepts the AI's symbol (X or O) as a parameter, so it can play either side.

### Why the AI is Unbeatable on Hard

Tic Tac Toe has only around 255,000 possible game states — a tiny number for a computer. The AI on Hard difficulty searches the entire game tree on every move, so it always knows the optimal play. The best a human can do is force a draw.

This is why Easy and Medium modes exist:

| Difficulty | Behavior |
|------------|----------|
| **Easy** | AI plays a completely random legal move |
| **Medium** | AI plays optimally 50% of the time, randomly 50% of the time |
| **Hard** | AI plays the optimal Minimax move every turn (unbeatable) |

---

## Board Representation

Internally, the board is stored as a flat list of 9 cells indexed 0 through 8:

```
 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8
```

The 8 winning lines (3 rows, 3 columns, 2 diagonals) are stored as a list of index triples, which keeps win-detection logic short and uniform.

---

## Concepts Demonstrated

This project demonstrates several important concepts in computer science and AI:

- **Minimax algorithm** — Recursive decision-making for two-player zero-sum games
- **Alpha-beta pruning** — Optimization technique to reduce search space
- **Recursion** — The AI explores future states by recursively calling itself
- **Game tree search** — Exhaustive exploration of all possible game continuations
- **Separation of concerns** — Game logic, AI logic, and UI are in separate modules
- **Event-driven GUI programming** — Tkinter callbacks and state management
- **State management** — Tracking turn order, scores, and game configuration

---

## Possible Extensions

Ideas for further development:

- Add an "Undo last move" button
- Alternate which player starts each round automatically
- Add sound effects for moves and game-end events
- Implement a 4×4 or 5×5 board variant with depth-limited minimax
- Add an online multiplayer mode using sockets
- Save game history to a file and display past results
- Add animations for placing marks and revealing wins

---

## License

This project is provided for educational purposes. Feel free to study, modify, and extend it.
