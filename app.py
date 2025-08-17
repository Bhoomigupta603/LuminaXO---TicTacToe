# ttt_flask.py
from flask import Flask, render_template, jsonify, request, session
from tictactoe_core import new_board, make_move, winner_line, is_draw, choose_ai_move
from ai_persona import pick
import random

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "replace_this_with_a_strong_secret_in_prod"  # change for real deployment

# Utility helpers to store/load session state
def init_session():
    session['board'] = new_board()
    session['player_sym'] = 'X'
    session['ai_sym'] = 'O'
    session['player_turn'] = True
    session['difficulty'] = 'medium'
    session.setdefault('scores', {'wins': 0, 'losses': 0, 'ties': 0})
    session['game_over'] = False
    session['message'] = pick('greet')

def session_board():
    return list(session.get('board', new_board()))

def save_board(b):
    session['board'] = list(b)

def game_state_payload():
    """Return JSON-friendly state for the frontend."""
    b = session_board()
    w, line = winner_line(b)
    payload = {
        'board': b,
        'player_sym': session.get('player_sym', 'X'),
        'ai_sym': session.get('ai_sym', 'O'),
        'player_turn': session.get('player_turn', True),
        'difficulty': session.get('difficulty', 'medium'),
        'scores': session.get('scores', {'wins':0,'losses':0,'ties':0}),
        'game_over': session.get('game_over', False),
        'message': session.get('message', ''),
        'winner': w if w else None,
        'winning_line': list(line) if line else None,
    }
    return payload

# Route: UI page
@app.route("/")
def index():
    if 'board' not in session:
        init_session()
    return render_template("index.html")

# Route: new game
@app.route("/api/new", methods=["POST"])
def api_new():
    payload = request.json or {}
    # optional: accept difficulty and symbol
    difficulty = payload.get('difficulty', 'medium')
    player_sym = payload.get('player_sym', 'X')
    player_starts = payload.get('player_starts', True)

    init_session()
    session['difficulty'] = difficulty
    session['player_sym'] = player_sym
    session['ai_sym'] = 'O' if player_sym == 'X' else 'X'
    session['player_turn'] = bool(player_starts)
    session['game_over'] = False
    session['message'] = pick('greet')
    save_board(new_board())
    return jsonify(game_state_payload())

# Route: make a player move
@app.route("/api/move", methods=["POST"])
def api_move():
    if 'board' not in session:
        init_session()

    if session.get('game_over', False):
        return jsonify(game_state_payload())

    data = request.json or {}
    try:
        idx = int(data.get('index'))
    except Exception:
        return jsonify({"error": "invalid index"}), 400

    b = session_board()
    # validate
    if idx < 0 or idx > 8 or b[idx] != ' ':
        return jsonify({"error": "invalid move", "state": game_state_payload()}), 400

    player = session.get('player_sym', 'X')
    ai = session.get('ai_sym', 'O')
    make_move(b, idx, player)
    save_board(b)

    # check end after player's move
    w, line = winner_line(b)
    if w:
        session['game_over'] = True
        if w == player:
            session['scores']['wins'] += 1
            session['message'] = "🎉 Congratulations! You win!"
        else:
            session['scores']['losses'] += 1
            session['message'] = "🤖 AI wins! Better luck next time."
        save_board(b)
        return jsonify(game_state_payload())

    if is_draw(b):
        session['game_over'] = True
        session['scores']['ties'] += 1
        session['message'] = "😅 It's a draw!"
        save_board(b)
        return jsonify(game_state_payload())

    # AI move (if game not over)
    session['player_turn'] = False
    session['message'] = pick('ai_thinking')
    save_board(b)

    # choose AI move
    try:
        ai_move = choose_ai_move(b, session.get('difficulty', 'medium'), ai, player)
    except Exception:
        # fallback random
        empties = [i for i, v in enumerate(b) if v == ' ']
        ai_move = random.choice(empties) if empties else None

    if ai_move is not None:
        make_move(b, ai_move, ai)
        save_board(b)

    # check end after AI move
    w2, line2 = winner_line(b)
    if w2:
        session['game_over'] = True
        if w2 == player:
            session['scores']['wins'] += 1
            session['message'] = "🎉 Congratulations! You win!"
        else:
            session['scores']['losses'] += 1
            session['message'] = "🤖 AI wins! Better luck next time."
        save_board(b)
        session['player_turn'] = False
        return jsonify(game_state_payload())

    if is_draw(b):
        session['game_over'] = True
        session['scores']['ties'] += 1
        session['message'] = "😅 It's a draw!"
        save_board(b)
        return jsonify(game_state_payload())

    # normal continue
    session['player_turn'] = True
    session['message'] = pick('your_turn')
    save_board(b)
    return jsonify(game_state_payload())

# Route: update settings (difficulty/symbol)
@app.route("/api/settings", methods=["POST"])
def api_settings():
    data = request.json or {}
    diff = data.get('difficulty')
    sym = data.get('player_sym')
    if diff:
        session['difficulty'] = diff
    if sym:
        session['player_sym'] = sym
        session['ai_sym'] = 'O' if sym == 'X' else 'X'
    return jsonify({"ok": True, **game_state_payload()})

# Route: scoreboard reset
@app.route("/api/reset_scores", methods=["POST"])
def api_reset_scores():
    session['scores'] = {'wins':0, 'losses':0, 'ties':0}
    return jsonify(game_state_payload())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
