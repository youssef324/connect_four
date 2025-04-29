import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import random
import time
from typing import List, Tuple, Optional

class Connect4:
    def __init__(self, rows=6, cols=7): #init is a contructor .. ya3ni bybtdy m3 el code 
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.last_move = None

    def reset(self): # function rest NPM model that works to find relationships
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.last_move = None

    def drop_piece(self, col: int) -> bool:
        """Attempt to drop a piece in the specified column.
        Returns True if successful, False if column is full."""
        if col < 0 or col >= self.cols:
            return False
            
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.last_move = (row, col)
                
                if self.check_win(row, col):
                    self.game_over = True
                    self.winner = self.current_player
                elif np.all(self.board != 0):
                    self.game_over = True
                
                self.current_player = 3 - self.current_player
                return True
        return False

    def check_win(self, row: int, col: int) -> bool:
        """Check if the last move resulted in a win."""
        player = self.board[row][col]
        
        # Check horizontal
        count = 1
        c = col - 1
        while c >= 0 and self.board[row][c] == player:
            count += 1
            c -= 1
        c = col + 1
        while c < self.cols and self.board[row][c] == player:
            count += 1
            c += 1
        if count >= 4:
            return True
        
        # Check vertical
        count = 1
        r = row + 1
        while r < self.rows and self.board[r][col] == player:
            count += 1
            r += 1
        if count >= 4:
            return True
        
        # Check diagonal (top-left to bottom-right)
        count = 1
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0 and self.board[r][c] == player:
            count += 1
            r -= 1
            c -= 1
        r, c = row + 1, col + 1
        while r < self.rows and c < self.cols and self.board[r][c] == player:
            count += 1
            r += 1
            c += 1
        if count >= 4:
            return True
        
        # Check diagonal (top-right to bottom-left)
        count = 1
        r, c = row - 1, col + 1
        while r >= 0 and c < self.cols and self.board[r][c] == player:
            count += 1
            r -= 1
            c += 1
        r, c = row + 1, col - 1
        while r < self.rows and c >= 0 and self.board[r][c] == player:
            count += 1
            r += 1
            c -= 1
        if count >= 4:
            return True
        
        return False

    def get_valid_moves(self) -> List[int]:
        """Returns a list of valid column indices where a piece can be dropped."""
        return [col for col in range(self.cols) if self.board[0][col] == 0]

    def is_valid_move(self, col: int) -> bool:
        """Check if a move is valid."""
        return col in self.get_valid_moves()

    def print_board(self):
        """Print the board to the terminal."""
        print("\n" + "-" * (self.cols * 4 + 1))
        for row in self.board:
            print("|", end="")
            for cell in row:
                print(f" {' ' if cell == 0 else 'X' if cell == 1 else 'O'} |", end="")
            print("\n" + "-" * (self.cols * 4 + 1))
        print(f"Current Player: {self.current_player} ({'X' if self.current_player == 1 else 'O'})")
        if self.last_move:
            print(f"Last move: row {self.last_move[0]}, col {self.last_move[1]}")


class AIPlayer:
    def __init__(self, player_num: int, difficulty: str = "medium"):
        self.player_num = player_num
        self.difficulty = difficulty
        self.nodes_visited = 0
        
    def get_move(self, game: Connect4) -> int:
        """Get the AI's move based on the current game state."""
        valid_moves = game.get_valid_moves()
        self.nodes_visited = 0
        
        if self.difficulty == "easy":
            return random.choice(valid_moves)
        elif self.difficulty == "medium":
            return self.medium_ai_move(game, valid_moves)
        else:  # hard
            return self.minimax_move(game, valid_moves)
    
    def medium_ai_move(self, game: Connect4, valid_moves: List[int]) -> int:
        # Check for immediate win
        for col in valid_moves:
            temp_game = Connect4(game.rows, game.cols)
            temp_game.board = np.copy(game.board)
            temp_game.current_player = game.current_player
            if temp_game.drop_piece(col) and temp_game.winner == self.player_num:
                return col
        
        # Check if opponent can win next move and block
        opponent = 3 - self.player_num
        for col in valid_moves:
            temp_game = Connect4(game.rows, game.cols)
            temp_game.board = np.copy(game.board)
            temp_game.current_player = opponent
            if temp_game.drop_piece(col) and temp_game.winner == opponent:
                return col
        
        # Otherwise, choose randomly but prefer center columns
        weights = [1, 2, 3, 4, 3, 2, 1]
        weighted_moves = []
        for col in valid_moves:
            weighted_moves.extend([col] * weights[col])
        return random.choice(weighted_moves)
    
    def minimax_move(self, game: Connect4, valid_moves: List[int], depth: int = 4) -> int:
        """Use minimax algorithm with alpha-beta pruning to determine best move."""  ## minmax with alphabeta
        best_score = -float('inf')
        best_move = random.choice(valid_moves)
        
        print(f"\nAI {self.player_num} ({self.difficulty}) is thinking...")
        print(f"Valid moves: {valid_moves}")
        
        for col in valid_moves:
            temp_game = Connect4(game.rows, game.cols)
            temp_game.board = np.copy(game.board)
            temp_game.current_player = game.current_player
            temp_game.drop_piece(col)
            
            score = self.minimax(temp_game, depth-1, -float('inf'), float('inf'), False)
            print(f"Column {col} score: {score}")
            
            if score > best_score:
                best_score = score
                best_move = col
        
        print(f"AI chose column {best_move} with score {best_score}")
        print(f"Nodes visited: {self.nodes_visited}")
        return best_move
    
    def minimax(self, game: Connect4, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        """Minimax algorithm with alpha-beta pruning."""
        self.nodes_visited += 1
        
        if depth == 0 or game.game_over:
            return self.evaluate_board(game)
        
        valid_moves = game.get_valid_moves()
        
        if maximizing_player:
            value = -float('inf')
            for col in valid_moves:
                temp_game = Connect4(game.rows, game.cols)
                temp_game.board = np.copy(game.board)
                temp_game.current_player = game.current_player
                temp_game.drop_piece(col)
                
                value = max(value, self.minimax(temp_game, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for col in valid_moves:
                temp_game = Connect4(game.rows, game.cols)
                temp_game.board = np.copy(game.board)
                temp_game.current_player = 3 - game.current_player
                temp_game.drop_piece(col)
                
                value = min(value, self.minimax(temp_game, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
    
    def evaluate_board(self, game: Connect4) -> float:
        """Evaluate the board position for the AI player."""
        if game.winner == self.player_num:
            return 1000
        elif game.winner == 3 - self.player_num:
            return -1000
        elif game.game_over:
            return 0
        
        score = 0
        center_col = game.cols // 2
        center_array = [game.board[row][center_col] for row in range(game.rows)]
        center_count = center_array.count(self.player_num)
        score += center_count * 3
        
        # Evaluate horizontal opportunities
        for row in range(game.rows):
            for col in range(game.cols - 3):
                window = game.board[row, col:col+4]
                score += self.evaluate_window(window)
        
        # Evaluate vertical opportunities
        for col in range(game.cols):
            for row in range(game.rows - 3):
                window = [game.board[row+i][col] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Evaluate diagonal (top-left to bottom-right) opportunities
        for row in range(game.rows - 3):
            for col in range(game.cols - 3):
                window = [game.board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Evaluate diagonal (top-right to bottom-left) opportunities
        for row in range(game.rows - 3):
            for col in range(3, game.cols):
                window = [game.board[row+i][col-i] for i in range(4)]
                score += self.evaluate_window(window)
        
        return score
    
    def evaluate_window(self, window: List[int]) -> float:
        """Evaluate a window of 4 positions for potential."""
        score = 0
        opponent = 3 - self.player_num
        
        if list(window).count(self.player_num) == 4:
            score += 100
        elif list(window).count(self.player_num) == 3 and list(window).count(0) == 1:
            score += 5
        elif list(window).count(self.player_num) == 2 and list(window).count(0) == 2:
            score += 2
        
        if list(window).count(opponent) == 3 and list(window).count(0) == 1:
            score -= 4
        
        return score


class HumanPlayer:
    def __init__(self, player_num: int):
        self.player_num = player_num


class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        
        # Game variables
        self.game = None
        self.player1 = None
        self.player2 = None
        self.ai_thinking = False
        self.scores = {1: 0, 2: 0, "draw": 0}
        
        # Colors
        self.bg_color = "#3498db"
        self.board_color = "#2980b9"
        self.empty_color = "white"
        self.player1_color = "#e74c3c"  # Red
        self.player2_color = "#f1c40f"  # Yellow
        self.highlight_color = "#2ecc71"
        
        # Setup main menu
        self.setup_main_menu()
        
    def setup_main_menu(self):
        """Create the main menu screen."""
        self.clear_window()
        
        # Main container frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Connect 4", font=("Arial", 32, "bold"), 
                             fg="white", bg=self.bg_color)
        title_label.pack(pady=(20, 40))
        
        # Game mode buttons
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        buttons = [
            ("Human vs Human", self.setup_human_vs_human),
            ("Human vs AI", self.setup_human_vs_ai),
            ("AI vs AI", self.setup_ai_vs_ai)
        ]
        
        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, font=("Arial", 14), width=20, 
                          command=command, bg="#2ecc71", fg="white", relief=tk.RAISED, 
                          bd=3, padx=10, pady=5)
            btn.pack(pady=10)
        
        # Exit button
        exit_button = tk.Button(main_frame, text="Exit", font=("Arial", 12), 
                               command=self.root.quit, bg="#e74c3c", fg="white", 
                               relief=tk.RAISED, bd=3, padx=10, pady=5)
        exit_button.pack(pady=20)
    
    def setup_human_vs_human(self):
        """Setup for Human vs Human game."""
        self.player1 = HumanPlayer(1)
        self.player2 = HumanPlayer(2)
        self.start_game()
    
    def setup_human_vs_ai(self):
        """Setup for Human vs AI game."""
        self.clear_window()
        
        # Main container frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="Human vs AI", font=("Arial", 24), 
                fg="white", bg=self.bg_color).pack(pady=20)
        
        # Difficulty selection frame
        difficulty_frame = tk.Frame(main_frame, bg=self.bg_color)
        difficulty_frame.pack(pady=20)
        
        tk.Label(difficulty_frame, text="Select AI Difficulty:", 
                font=("Arial", 14), fg="white", bg=self.bg_color).pack()
        
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        self.ai_difficulty = tk.StringVar(value="medium")
        
        for text, mode in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=text, variable=self.ai_difficulty, 
                              value=mode, font=("Arial", 12), fg="white", bg=self.bg_color, 
                              selectcolor=self.board_color, activebackground=self.bg_color)
            rb.pack(anchor=tk.W, padx=50, pady=5)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # Start button
        start_button = tk.Button(button_frame, text="Start Game", font=("Arial", 14), 
                               command=self.start_human_vs_ai, bg="#2ecc71", fg="white", 
                               relief=tk.RAISED, bd=3, padx=10, pady=5)
        start_button.pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_button = tk.Button(button_frame, text="Back", font=("Arial", 14), 
                              command=self.setup_main_menu, bg="#e74c3c", fg="white", 
                              relief=tk.RAISED, bd=3, padx=10, pady=5)
        back_button.pack(side=tk.LEFT, padx=10)
    
    def start_human_vs_ai(self):
        """Start Human vs AI game with selected difficulty."""
        self.player1 = HumanPlayer(1)
        self.player2 = AIPlayer(2, self.ai_difficulty.get())
        self.start_game()
    
    def setup_ai_vs_ai(self):
        """Setup for AI vs AI game."""
        self.clear_window()
        
        # Main container frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="AI vs AI", font=("Arial", 24), 
                fg="white", bg=self.bg_color).pack(pady=20)
        
        # AI 1 difficulty selection
        ai1_frame = tk.Frame(main_frame, bg=self.bg_color)
        ai1_frame.pack(pady=10)
        
        tk.Label(ai1_frame, text="AI Player 1 Difficulty:", 
                font=("Arial", 14), fg="white", bg=self.bg_color).pack()
        
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        self.ai1_difficulty = tk.StringVar(value="medium")
        
        for text, mode in difficulties:
            rb = tk.Radiobutton(ai1_frame, text=text, variable=self.ai1_difficulty, 
                              value=mode, font=("Arial", 12), fg="white", bg=self.bg_color, 
                              selectcolor=self.board_color, activebackground=self.bg_color)
            rb.pack(anchor=tk.W, padx=50, pady=5)
        
        # AI 2 difficulty selection
        ai2_frame = tk.Frame(main_frame, bg=self.bg_color)
        ai2_frame.pack(pady=10)
        
        tk.Label(ai2_frame, text="AI Player 2 Difficulty:", 
                font=("Arial", 14), fg="white", bg=self.bg_color).pack()
        
        self.ai2_difficulty = tk.StringVar(value="medium")
        
        for text, mode in difficulties:
            rb = tk.Radiobutton(ai2_frame, text=text, variable=self.ai2_difficulty, 
                              value=mode, font=("Arial", 12), fg="white", bg=self.bg_color, 
                              selectcolor=self.board_color, activebackground=self.bg_color)
            rb.pack(anchor=tk.W, padx=50, pady=5)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # Start button
        start_button = tk.Button(button_frame, text="Start Game", font=("Arial", 14), 
                               command=self.start_ai_vs_ai, bg="#2ecc71", fg="white", 
                               relief=tk.RAISED, bd=3, padx=10, pady=5)
        start_button.pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_button = tk.Button(button_frame, text="Back", font=("Arial", 14), 
                              command=self.setup_main_menu, bg="#e74c3c", fg="white", 
                              relief=tk.RAISED, bd=3, padx=10, pady=5)
        back_button.pack(side=tk.LEFT, padx=10)
    
    def start_ai_vs_ai(self):
        """Start AI vs AI game with selected difficulties."""
        self.player1 = AIPlayer(1, self.ai1_difficulty.get())
        self.player2 = AIPlayer(2, self.ai2_difficulty.get())
        self.start_game()
        self.ai_move()  # Start the AI moves
    
    def start_game(self):
        """Initialize and display the game board."""
        self.clear_window()
        self.game = Connect4()
        
        # Main game frame
        game_frame = tk.Frame(self.root, bg=self.bg_color)
        game_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Score display
        score_frame = tk.Frame(game_frame, bg=self.bg_color)
        score_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(score_frame, text=f"Player 1 (Red): {self.scores[1]}", 
                font=("Arial", 12), fg=self.player1_color, bg=self.bg_color).pack(side=tk.LEFT, padx=10)
        
        tk.Label(score_frame, text=f"Draws: {self.scores['draw']}", 
                font=("Arial", 12), fg="white", bg=self.bg_color).pack(side=tk.LEFT, padx=10)
        
        tk.Label(score_frame, text=f"Player 2 (Yellow): {self.scores[2]}", 
                font=("Arial", 12), fg=self.player2_color, bg=self.bg_color).pack(side=tk.LEFT, padx=10)
        
        # Create game board UI
        self.canvas = tk.Canvas(game_frame, width=700, height=600, bg=self.board_color, highlightthickness=0)
        self.canvas.pack(pady=(0, 20))
        
        # Draw the board
        self.draw_board()
        
        # Add column click handlers for human players
        if isinstance(self.player1, HumanPlayer) or isinstance(self.player2, HumanPlayer):
            self.canvas.bind("<Button-1>", self.handle_click)
        
        # Control buttons frame
        control_frame = tk.Frame(game_frame, bg=self.bg_color)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Exit button
        exit_button = tk.Button(control_frame, text="Exit", font=("Arial", 12), 
                              command=self.root.quit, bg="#e74c3c", fg="white", 
                              relief=tk.RAISED, bd=3, padx=10, pady=5)
        exit_button.pack(side=tk.LEFT, padx=10)
        
        # Restart button
        restart_button = tk.Button(control_frame, text="Restart", font=("Arial", 12), 
                                 command=self.restart_game, bg="#3498db", fg="white", 
                                 relief=tk.RAISED, bd=3, padx=10, pady=5)
        restart_button.pack(side=tk.LEFT, padx=10)
        
        # New Game button
        new_game_button = tk.Button(control_frame, text="New Game", font=("Arial", 12), 
                                  command=self.setup_main_menu, bg="#2ecc71", fg="white", 
                                  relief=tk.RAISED, bd=3, padx=10, pady=5)
        new_game_button.pack(side=tk.LEFT, padx=10)
        
        # If it's AI's turn first, make the move
        if isinstance(self.player1, AIPlayer) and self.game.current_player == 1:
            self.ai_move()
    
    def draw_board(self):
        """Draw the Connect 4 board on the canvas."""
        self.canvas.delete("all")
        cell_width = 100
        cell_height = 100
        padding = 5
        
        # Draw slots
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                x1 = col * cell_width + padding
                y1 = row * cell_height + padding
                x2 = (col + 1) * cell_width - padding
                y2 = (row + 1) * cell_height - padding
                
                # Determine color based on board state
                if self.game.board[row][col] == 1:
                    color = self.player1_color
                elif self.game.board[row][col] == 2:
                    color = self.player2_color
                else:
                    color = self.empty_color
                
                # Highlight last move
                outline = self.highlight_color if self.game.last_move and self.game.last_move == (row, col) else self.board_color
                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline, width=2)
        
        # Show current player
        current_player_text = f"Current Turn: {'Player 1 (Red)' if self.game.current_player == 1 else 'Player 2 (Yellow)'}"
        self.canvas.create_text(350, 580, text=current_player_text, font=("Arial", 12, "bold"), fill="white")
        
        # Print board to terminal
        self.game.print_board()
    
    def handle_click(self, event):
        """Handle mouse clicks on the game board."""
        if self.ai_thinking or self.game.game_over:
            return
            
        if (isinstance(self.player1, HumanPlayer) and self.game.current_player == 1) or \
           (isinstance(self.player2, HumanPlayer) and self.game.current_player == 2):
            col = event.x // 100
            self.make_move(col)
    
    def make_move(self, col: int):
        """Attempt to make a move in the specified column."""
        if self.game.is_valid_move(col):
            self.game.drop_piece(col)
            self.draw_board()
            
            if self.game.game_over:
                self.show_game_result()
            elif isinstance(self.player1 if self.game.current_player == 1 else self.player2, AIPlayer):
                self.ai_move()
    
    def ai_move(self):
        """Make an AI move with a small delay for visualization."""
        if self.game.game_over:
            return
            
        self.ai_thinking = True
        current_player = self.player1 if self.game.current_player == 1 else self.player2
        
        # For AI vs AI, add a longer delay so humans can follow
        delay = 1000 if isinstance(self.player1, AIPlayer) and isinstance(self.player2, AIPlayer) else 500
        
        self.root.after(delay, lambda: self.execute_ai_move(current_player))
    
    def execute_ai_move(self, ai_player):
        """Execute the AI's move after the delay."""
        col = ai_player.get_move(self.game)
        self.game.drop_piece(col)
        self.draw_board()
        self.ai_thinking = False
        
        if self.game.game_over:
            self.show_game_result()
        elif isinstance(self.player1 if self.game.current_player == 1 else self.player2, AIPlayer):
            self.ai_move()
    
    def show_game_result(self):
        """Show a message box with the game result and update scores."""
        if self.game.winner:
            winner_text = f"Player {self.game.winner} ({'Red' if self.game.winner == 1 else 'Yellow'}) wins!"
            self.scores[self.game.winner] += 1
        else:
            winner_text = "It's a draw!"
            self.scores["draw"] += 1
        
        messagebox.showinfo("Game Over", winner_text)
        self.update_score_display()
    
    def update_score_display(self):
        """Update the score display on the game board."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and hasattr(widget, '_name') and widget._name == '!frame':
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        if "Player 1" in child.cget("text"):
                            child.config(text=f"Player 1 (Red): {self.scores[1]}")
                        elif "Player 2" in child.cget("text"):
                            child.config(text=f"Player 2 (Yellow): {self.scores[2]}")
                        elif "Draws" in child.cget("text"):
                            child.config(text=f"Draws: {self.scores['draw']}")
    
    def restart_game(self):
        """Restart the game with the same players but reset the board."""
        if self.game:
            self.game.reset()
            self.draw_board()
    
    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    root.configure(bg="#3498db")
    root.resizable(False, False)
    
    # Center the window on screen
    window_width = 800
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = Connect4GUI(root)
    root.mainloop()