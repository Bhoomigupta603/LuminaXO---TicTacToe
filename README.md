# LuminaXO 

**LuminaXO** is a modern, neon-glow Tic-Tac-Toe game built with Python and Flask. It features a vibrant glass-style UI, glowing moves, AI voice guidance, and responsive gameplay to impress users.  

---

## Features

- Neon glow interface for X, O, and winning lines.  
- Frosted glass UI panels with vibrant colors.  
- Optional voice guidance for moves and messages.  
- Customizable settings: symbol, difficulty, and voice.  
- Responsive, animated layout with hover and glow effects.  
- Real-time score tracking for Wins, Losses, and Ties.  

---

## Technologies Used

- **Python 3.10+**  
- **Flask** for backend and routing  
- **HTML5, CSS3, JavaScript (ES6)** for frontend  
- **Voice Support:** `tts_helper.py` using pyttsx3  
- **Game Logic:** `tictactoe_core.py`  
- **AI Persona:** `ai_persona.py`  

---

## Project Structure

LuminaXO/
├─ app.py # Main Flask application
├─ ai_persona.py # AI messages and persona
├─ tictactoe_core.py # Game logic and AI moves
├─ tts_helper.py # Text-to-speech helper
├─ ttt_console.py # Optional console version
├─ ttt_gui.py # Optional GUI version
├─ requirements.txt # Python dependencies
├─ templates/
│ └─ index.html # Main web page
├─ static/
│ ├─ CSS/
│ │ └─ style.css # Styles and glass/neon effects
│ └─ JS/
│ └─ script.js # Frontend logic and voice control
├─ .venv/ # Python virtual environment
└─ pycache/ # Python cache files

---

## Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/LuminaXO.git
cd LuminaXO

2. Create and activate a virtual environment:
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

2. Install dependencies:

pip install -r requirements.txt

3. Run the Flask app:
python app.py

4. Open your browser and go to:
http://127.0.0.1:5000

- How to Play
1. Open the web app in a browser.
2. Select your symbol (X or O) and AI difficulty.
3. Enable or disable voice guidance.
4. Click a cell to make your move. The AI responds instantly.
5. Winning moves glow, and the score updates in real-time.
6. Use New Game or Replay to restart.

- Demo
Watch the Demo Video

![LuminaXO Demo](src="https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7362832720852369408?compact=1")

- Future Enhancements
Online multiplayer support
Mobile-friendly gestures
Multiple AI personalities and voices
Online leaderboard

