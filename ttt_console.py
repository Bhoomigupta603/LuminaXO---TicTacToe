"""
Console Edition:
- Colorful board (BLUE for Player, RED for AI, GREEN highlights on win)
- 3 difficulty levels (easy, medium, hard)
- AI personality lines + optional voice (pyttsx3)
- Replay and scoreboard
"""

import time
import random
from typing import Optional, Tuple

from colorama import init as colorama_init, Fore, Style
from tictactoe_core import (
    new_board, available_moves, make_move, undo_move,
    winner_line, is_draw, choose_ai_move
)
from ai_persona import pick
from tts_helper import speak_async

colorama_init(autoreset=True)

# ------- Appearance -------

BLUE = Fore.CYAN  # player
RED = Fore.LIGHTRED_EX  # ai
GREEN = Fore.LIGHTGREEN_EX
DIM = Style.DIM
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

def symbol_color(sym: str, is_player: bool) -> str:
    if sym == ' ':
        return ' '
    col = BLUE if is_player else RED
    return f"{BOLD}{col}{sym}{RESET}"

def render_board(board, player_sym: str, ai_sym: str,
                 highlight: Optional[Tuple[int,int,int]]=None) -> str:
    """Return a colored string for the board."""
    rows = []
    for r in range(3):
        cells = []
        for c in range(3):
            i = r*3 + c
            v = board[i]
            if highlight and i in highlight and v != ' ':
                colored = f"{BOLD}{GREEN}{v}{RESET}"
            else:
                if v == ' ':
                    # show cell index (1..9) as hint
                    hint = f"{DIM}{i+1}{RESET}"
                    colored = hint
                elif v == player_sym:
                    colored = symbol_color(v, True)
                else:
                    colored = symbol_color(v, False)
            cells.append(f" {colored} ")
        rows.append("│".join(cells))
    sep = f"{DIM}───┼───┼───{RESET}"
    return f"\n{rows[0]}\n{sep}\n{rows[1]}\n{sep}\n{rows[2]}\n"

# ------- Input helpers -------

def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(f"{prompt} ").strip().lower()
        if ans in ('y','yes'): return True
        if ans in ('n','no'): return False
        print("Please type y or n.")

def ask_choice(prompt: str, choices: list) -> str:
    chset = {c.lower(): c for c in choices}
    while True:
        ans = input(f"{prompt} ").strip().lower()
        if ans in chset:
            return chset[ans]
        print(f"Choose one of: {', '.join(choices)}")

def ask_move(board) -> int:
    while True:
        raw = input("Enter your move (1-9 as shown on the board): ").strip()
        if not raw.isdigit():
            print("Please enter a number 1-9.")
            continue
        idx = int(raw) - 1
        if idx < 0 or idx > 8:
            print("Out of range. Use 1-9.")
            continue
        if board[idx] != ' ':
            print("That spot is taken. Try another.")
            continue
        return idx

# ------- Game loop -------

def play_round(difficulty: str, voice: bool, scores: dict) -> None:
    board = new_board()
    print(BOLD + pick('greet') + RESET)
    player_sym = ask_choice("Choose your symbol (X/O): ", ["X", "O"]).upper()
    ai_sym = 'O' if player_sym == 'X' else 'X'
    player_starts = ask_yes_no("Do you want to go first? (y/n)")
    if voice:
        speak_async("Game on!")

    # Round loop
    turn_player = player_starts
    print(pick('choose_diff'))
    print(f"Difficulty: {difficulty.capitalize()}\n")

    while True:
        print(render_board(board, player_sym, ai_sym))
        w, line = winner_line(board)
        if w or is_draw(board):
            if w == player_sym:
                print(BOLD + pick('human_win') + RESET)
                if voice: speak_async("You win! Nice one.")
                scores['wins'] += 1
            elif w == ai_sym:
                # show final board with highlight
                print(render_board(board, player_sym, ai_sym, highlight=line))
                print(BOLD + pick('ai_win') + RESET)
                if voice: speak_async("I win! Rematch?")
                scores['losses'] += 1
            else:
                print(BOLD + pick('tie') + RESET)
                if voice: speak_async("It's a draw!")
                scores['ties'] += 1
            print_score(scores)
            break

        if turn_player:
            print(BOLD + pick('your_turn') + RESET)
            if voice: speak_async("Your turn.")
            move = ask_move(board)
            make_move(board, move, player_sym)
        else:
            print(BOLD + "AI thinking…" + RESET, DIM + f"({pick('ai_thinking')})" + RESET)
            if voice: speak_async("Thinking...")
            time.sleep(random.uniform(0.35, 0.85))  # tiny delay for vibe
            move = choose_ai_move(board, difficulty, ai_sym, player_sym)
            make_move(board, move, ai_sym)
            print(DIM + pick('ai_move') + RESET)

        turn_player = not turn_player

def print_score(scores: dict):
    print(f"\n{BOLD}Scoreboard{RESET}: Wins {scores['wins']} | Losses {scores['losses']} | Ties {scores['ties']}\n")

def main():
    print(f"{BOLD}Tic-Tac-Toe AI (Console Edition){RESET}")
    diff_map = {'1':'easy','2':'medium','3':'hard'}
    voice = ask_yes_no("Enable voice feedback (TTS)? (y/n)")
    scores = {'wins':0, 'losses':0, 'ties':0}
    while True:
        print("\nChoose difficulty: 1) Easy  2) Medium  3) Hard")
        choice = input("Enter 1/2/3: ").strip()
        difficulty = diff_map.get(choice, 'medium')
        play_round(difficulty, voice, scores)
        print_score(scores)
        if not ask_yes_no(pick('play_again')):
            if voice: speak_async("Thanks for playing. Goodbye!")
            print("\nGoodbye! 👋\n")
            break

if __name__ == "__main__":
    main()
