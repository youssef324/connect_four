# 🟡🔴 Connect 4 Game (Tkinter GUI) 🟡🔴

A Python implementation of the classic Connect 4 game with a graphical user interface using Tkinter. The game supports Human vs Human, Human vs AI, and AI vs AI modes, with three AI difficulty levels (Easy, Medium, Hard).

---

## ✨ Features

- 🎨 **Graphical Interface:** Built with Tkinter for a smooth and interactive experience.
- 👥 **Multiple Game Modes:**  
  - 🧑‍🤝‍🧑 Human vs Human  
  - 🧑 vs 🤖 Human vs AI (selectable difficulty)  
  - 🤖 vs 🤖 AI vs AI (selectable difficulty for both AIs)
- 🧠 **AI Difficulty Levels:**  
  - 🟢 Easy: Random moves  
  - 🟡 Medium: Blocks immediate wins and prefers center columns  
  - 🔴 Hard: Uses Minimax with alpha-beta pruning
- 🏆 **Score Tracking:** Keeps track of wins and draws.
- 🔄 **Restart/New Game:** Easily restart or start a new game from the menu.
- 🌈 **Colorful Board:** Customizable colors for players and board.

---

## 🛠 Requirements

- Python 3.7+
- [numpy](https://pypi.org/project/numpy/)

No external graphics libraries are required (no pygame, no cairo, no cairosvg).

---

## 🚀 Installation

1. **Clone the repository or copy the code:**
    ```bash
    git clone https://github.com/youssef324/connect4-tkinter.git
    cd connect4-tkinter
    ```

2. **Install dependencies:**
    ```bash
    pip install numpy
    ```

---

## ▶️ Usage

1. **Run the game:**
    ```bash
    python test.py
    ```

2. **How to Play:**
    - Choose your game mode from the main menu.
    - For Human players, click on the column where you want to drop your piece.
    - For AI, select the difficulty and watch the AI play.
    - Use the Restart or New Game buttons to play again.

---

## 📁 File Structure

- `test.py` - Main source code for the Connect 4 game and GUI.

---

## 👤 Author

- **youssef324**

---

## 📄 License

This project is for educational purposes.
