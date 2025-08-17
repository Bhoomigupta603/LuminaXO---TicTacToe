# modified code:
"""
Tkinter GUI Edition (Enhanced):
- Buttons as cells
- Color coding: BLUE (Player), RED (AI), GREEN (winning line)
- Difficulty dropdown, New Game button, scoreboard, dynamic messages
- Optional TTS (toggle in top-right)
- Polished UI and improved end-game messages
"""

import tkinter as tk
from tkinter import ttk
import random, time

from tictactoe_core import (
    new_board, make_move, available_moves, winner_line, is_draw, choose_ai_move
)
from ai_persona import pick
from tts_helper import speak_async

# ---- Colors (Tkinter uses hex) ----
COLOR_BG = "#0f1220"
COLOR_PANEL = "#171b2e"
COLOR_TEXT = "#e6e6e6"
COLOR_BLUE = "#00bcd4"   # player
COLOR_RED = "#ff6b6b"    # ai
COLOR_GREEN = "#4caf50"  # winning
COLOR_DIM = "#8f9bb3"

class TTTApp:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe AI")
        root.configure(bg=COLOR_BG)
        root.resizable(False, False)

        # State
        self.player_sym = 'X'
        self.ai_sym = 'O'
        self.difficulty = tk.StringVar(value="medium")
        self.voice_on = tk.BooleanVar(value=False)
        self.scores = {'wins':0, 'losses':0, 'ties':0}
        self.board = new_board()
        self.player_turn = True
        self.game_over = False

        self._build_ui()
        self._new_game(reset_scores=False)

    def _build_ui(self):
        # Top bar
        top = tk.Frame(self.root, bg=COLOR_BG)
        top.pack(padx=16, pady=10, fill="x")

        ttk.Style().configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT)
        ttk.Style().configure("TButton", padding=4)

        self.title_lbl = tk.Label(top, text="Tic-Tac-Toe AI", font=("Segoe UI", 18, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        self.title_lbl.pack(side="left")

        # Difficulty
        diff_frame = tk.Frame(top, bg=COLOR_BG)
        diff_frame.pack(side="left", padx=20)
        tk.Label(diff_frame, text="Difficulty:", bg=COLOR_BG, fg=COLOR_DIM).pack(side="left")
        diff_menu = ttk.Combobox(diff_frame, values=["easy", "medium", "hard"],
                                 textvariable=self.difficulty, width=8, state="readonly")
        diff_menu.pack(side="left", padx=6)

        # Symbol toggle
        sym_frame = tk.Frame(top, bg=COLOR_BG)
        sym_frame.pack(side="left", padx=20)
        tk.Label(sym_frame, text="You:", bg=COLOR_BG, fg=COLOR_DIM).pack(side="left")
        self.sym_var = tk.StringVar(value="X")
        sym_menu = ttk.Combobox(sym_frame, values=["X", "O"], textvariable=self.sym_var, width=3, state="readonly")
        sym_menu.pack(side="left", padx=6)

        # Voice
        tk.Checkbutton(top, text="Voice", variable=self.voice_on, bg=COLOR_BG, fg=COLOR_TEXT,
                       activebackground=COLOR_BG, selectcolor=COLOR_BG,
                       highlightthickness=0).pack(side="right")

        # New game
        ttk.Button(top, text="New Game", command=lambda: self._new_game(reset_scores=False)).pack(side="right", padx=10)

        # Scoreboard
        self.score_lbl = tk.Label(self.root, text="", bg=COLOR_BG, fg=COLOR_TEXT, font=("Consolas", 12))
        self.score_lbl.pack()

        # Message
        self.msg_lbl = tk.Label(self.root, text="", bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 13, "bold"))
        self.msg_lbl.pack(pady=(2, 10))

        # Board grid
        board_frame = tk.Frame(self.root, bg=COLOR_PANEL, bd=2, relief="ridge")
        board_frame.pack(padx=16, pady=10)

        self.buttons = []
        for r in range(3):
            row = []
            for c in range(3):
                i = r*3 + c
                btn = tk.Button(board_frame, text=str(i+1), width=6, height=3,
                                font=("Segoe UI", 20, "bold"),
                                bg=COLOR_PANEL, fg=COLOR_DIM,
                                activebackground="#2a2f4a", activeforeground="#ffffff",
                                bd=0, highlightthickness=0,
                                command=lambda idx=i: self.on_cell(idx))
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                row.append(btn)
            self.buttons.extend(row)

        # Replay / Reset scores
        bottom = tk.Frame(self.root, bg=COLOR_BG)
        bottom.pack(pady=(6, 12))
        ttk.Button(bottom, text="Replay", command=lambda: self._new_game(reset_scores=False)).pack(side="left", padx=6)
        ttk.Button(bottom, text="Reset Scores", command=lambda: self._reset_scores()).pack(side="left", padx=6)

        self._update_score()

    def _reset_scores(self):
        self.scores = {'wins':0, 'losses':0, 'ties':0}
        self._update_score()

    def _update_score(self):
        self.score_lbl.config(text=f"Wins {self.scores['wins']} | Losses {self.scores['losses']} | Ties {self.scores['ties']}")

    def _new_game(self, reset_scores=False):
        self.board = new_board()
        self.game_over = False
        self._clear_highlights()
        # update symbols
        self.player_sym = self.sym_var.get()
        self.ai_sym = 'O' if self.player_sym == 'X' else 'X'
        # set who starts
        self.player_turn = True
        # reset button appearances
        for i, b in enumerate(self.buttons):
            b.config(text=str(i+1), fg=COLOR_DIM, state="normal", bg=COLOR_PANEL)
        self._set_msg(pick("greet"))
        if self.voice_on.get(): speak_async("Game on. Your turn.")
        self._turn_label()

    def _turn_label(self, thinking=False):
        if self.game_over:
            return
        if thinking:
            self._set_msg("AI thinking… " + pick('ai_thinking'))
        else:
            if self.player_turn:
                self._set_msg("Your turn — make a move.")
            else:
                self._set_msg("AI turn…")

    def _set_msg(self, text: str):
        self.msg_lbl.config(text=text)

    def on_cell(self, idx: int):
        if self.game_over or not self.player_turn:
            return
        if self.board[idx] != ' ':
            return
        # human move
        self.board[idx] = self.player_sym
        self._paint_cell(idx, self.player_sym)
        self._check_end_or_continue()

        if not self.game_over:
            # AI move after a tiny delay to feel interactive
            self.player_turn = False
            self._turn_label(thinking=True)
            self.root.after(550, self._ai_move)

    def _ai_move(self):
        if self.game_over:
            return
        try:
            move = choose_ai_move(self.board, self.difficulty.get(), self.ai_sym, self.player_sym)
        except Exception:
            return
        self.board[move] = self.ai_sym
        self._paint_cell(move, self.ai_sym)
        if self.voice_on.get(): speak_async("I move.")
        self._check_end_or_continue()
        if not self.game_over:
            self.player_turn = True
            self._turn_label()

    def _paint_cell(self, idx: int, sym: str):
        btn = self.buttons[idx]
        btn.config(text=sym, fg=(COLOR_BLUE if sym == self.player_sym else COLOR_RED))

    def _clear_highlights(self):
        for b in self.buttons:
            b.config(bg=COLOR_PANEL)

    def _check_end_or_continue(self):
        w, line = winner_line(self.board)
        if w:
            self.game_over = True
            self._highlight_line(line)
            for b in self.buttons:
                b.config(state="disabled")
            if w == self.player_sym:
                self._set_msg("🎉 Congratulations! You win!")
                self.scores['wins'] += 1
                if self.voice_on.get(): speak_async("Congratulations! You win!")
            else:
                self._set_msg("🤖 AI wins! Better luck next time.")
                self.scores['losses'] += 1
                if self.voice_on.get(): speak_async("I win! Better luck next time.")
            self._update_score()
            return
        if is_draw(self.board):
            self.game_over = True
            self._set_msg("😅 It's a draw!")
            self.scores['ties'] += 1
            self._update_score()
            if self.voice_on.get(): speak_async("It's a draw.")
            for b in self.buttons:
                b.config(state="disabled")
            return

    def _highlight_line(self, line):
        for i in line:
            self.buttons[i].config(bg=COLOR_GREEN)

def main():
    root = tk.Tk()
    app = TTTApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
