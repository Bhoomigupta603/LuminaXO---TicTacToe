"""
Cheeky/friendly AI personality lines. Call via persona.pick('context').
"""

import random

LINES = {
    'greet': [
        "Hey there, human! Ready to get schooled? 😏",
        "Welcome! I’m warm, witty, and slightly unbeatable.",
        "Namaste! May your moves be wise… and mine wiser.",
    ],
    'choose_diff': [
        "Pick my power level: Easy (nap mode), Medium (coffee), Hard (laser focus).",
        "Feeling brave? Hard mode doesn’t blink. I don’t have eyelids anyway.",
    ],
    'your_turn': [
        "Your turn—show me what you’ve got!",
        "All eyes on you. No pressure. 🙂",
        "Your move, maestro.",
    ],
    'ai_thinking': [
        "Hmm… thinking… calculating… pretending to think so you relax…",
        "Give me a sec, plotting your downfall.",
        "Processing… (beep boop)",
    ],
    'ai_move': [
        "I’ll place mine here. Strategic… or is it?",
        "Boom. Your turn!",
        "Ok I go there. Your move!",
    ],
    'ai_win': [
        "I win! Good game—rematch? 😎",
        "Victory dance initiated. 🕺",
        "Unbeatable they said… accurate they were.",
    ],
    'human_win': [
        "You win! Respect! 🫡",
        "Oof. Didn’t see that coming. (I did, but drama!)",
        "Nice one! You’ve got game.",
    ],
    'tie': [
        "It’s a draw! That was tight.",
        "Nobody wins, nobody loses—philosophical, huh?",
        "Cats game! 🐱",
    ],
    'play_again': [
        "One more? (y/n)",
        "Again? I promise to blink this time. (still no eyelids)",
        "Rematch? Press y to continue.",
    ],
}

def pick(key: str) -> str:
    return random.choice(LINES.get(key, ["..."]))
