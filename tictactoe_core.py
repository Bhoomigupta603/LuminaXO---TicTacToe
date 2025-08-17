"""
Core game logic for Tic-Tac-Toe:
- board helpers
- win/draw detection
- AI move selectors for Easy / Medium / Hard (Minimax + alpha-beta)
This file is UI-agnostic (no prints).
"""

from __future__ import annotations
import random
from typing import List, Optional, Tuple

# Board is a list of 9: indices 0..8
# Symbols are 'X' or 'O' or ' ' (empty)
LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

def new_board() -> List[str]:
    return [' '] * 9

def available_moves(board: List[str]) -> List[int]:
    return [i for i, v in enumerate(board) if v == ' ']

def make_move(board: List[str], idx: int, sym: str) -> None:
    board[idx] = sym

def undo_move(board: List[str], idx: int) -> None:
    board[idx] = ' '

def winner_line(board: List[str]) -> Tuple[Optional[str], Optional[Tuple[int,int,int]]]:
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)
    return None, None

def is_draw(board: List[str]) -> bool:
    w, _ = winner_line(board)
    return w is None and all(v != ' ' for v in board)

# ---------- Heuristics for Medium difficulty ----------

def find_winning_move(board: List[str], sym: str) -> Optional[int]:
    for i in available_moves(board):
        make_move(board, i, sym)
        w, _ = winner_line(board)
        undo_move(board, i)
        if w == sym:
            return i
    return None

def best_heuristic_move(board: List[str], ai: str, human: str) -> Optional[int]:
    # 1) Win if possible
    m = find_winning_move(board, ai)
    if m is not None:
        return m
    # 2) Block if needed
    m = find_winning_move(board, human)
    if m is not None:
        return m
    # 3) Take center
    if board[4] == ' ':
        return 4
    # 4) Corners are strong
    corners = [i for i in (0, 2, 6, 8) if board[i] == ' ']
    if corners:
        return random.choice(corners)
    # 5) Sides last
    sides = [i for i in (1, 3, 5, 7) if board[i] == ' ']
    if sides:
        return random.choice(sides)
    return None

# ---------- Minimax (Hard) ----------

def minimax(board: List[str], ai: str, human: str, is_max: bool,
            depth: int, alpha: int, beta: int) -> int:
    w, _ = winner_line(board)
    if w == ai:
        return 10 - depth
    if w == human:
        return depth - 10
    if is_draw(board):
        return 0

    if is_max:
        best = -999
        for i in available_moves(board):
            make_move(board, i, ai)
            score = minimax(board, ai, human, False, depth + 1, alpha, beta)
            undo_move(board, i)
            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if beta <= alpha:
                break
        return best
    else:
        best = 999
        for i in available_moves(board):
            make_move(board, i, human)
            score = minimax(board, ai, human, True, depth + 1, alpha, beta)
            undo_move(board, i)
            if score < best:
                best = score
            if best < beta:
                beta = best
            if beta <= alpha:
                break
        return best

def best_minimax_move(board: List[str], ai: str, human: str) -> int:
    best_score = -999
    best_moves = []
    for i in available_moves(board):
        make_move(board, i, ai)
        score = minimax(board, ai, human, False, 0, -999, 999)
        undo_move(board, i)
        if score > best_score:
            best_score = score
            best_moves = [i]
        elif score == best_score:
            best_moves.append(i)
    # If multiple best moves, randomize among them so it feels less robotic
    return random.choice(best_moves)

# ---------- Public AI API ----------

def choose_ai_move(board: List[str], difficulty: str, ai: str, human: str) -> int:
    diff = difficulty.lower()
    moves = available_moves(board)
    if not moves:
        raise ValueError("No moves available")

    if diff == 'easy':
        return random.choice(moves)

    if diff == 'medium':
        # 50% chance pick best heuristic, 50% random to keep it human-like
        if random.random() < 0.5:
            choice = best_heuristic_move(board, ai, human)
            if choice is not None:
                return choice
        # fallback random
        return random.choice(moves)

    if diff == 'hard':
        return best_minimax_move(board, ai, human)

    # default fallback
    return random.choice(moves)
