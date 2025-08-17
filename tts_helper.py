"""
Tiny wrapper around pyttsx3 so we can speak without freezing the UI.
You can disable voice at runtime from callers.
"""

import threading
import pyttsx3

_engine = None
_engine_lock = threading.Lock()

def _ensure_engine():
    global _engine
    if _engine is None:
        with _engine_lock:
            if _engine is None:
                _engine = pyttsx3.init()
                # Optional: tweak voice rate/volume
                _engine.setProperty('rate', 175)
                _engine.setProperty('volume', 1.0)

def speak_async(text: str):
    """Say text in a background thread (non-blocking)."""
    if not text:
        return
    _ensure_engine()
    def _run():
        try:
            _engine.say(text)
            _engine.runAndWait()
        except Exception:
            pass  # fail silently if audio backend not available
    t = threading.Thread(target=_run, daemon=True)
    t.start()
