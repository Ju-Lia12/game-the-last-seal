# OpenCode Agent Instructions

## Architecture & Boundaries
- **Framework:** Python with `pygame`.
- **Entrypoint:** App execution begins in `main.py`, which instantiates the `Game` class from `code/game.py`.
- **Code Organization:**
  - `code/`: Contains all game logic (`game.py`, `menu.py`, `level.py`, `entity.py`, `player.py`, `enemy.py`).
  - `asset/`: Contains all graphics (PNGs) and audio files (MP3s).
- **Asset Loading:** Asset paths are hardcoded relative to the repository root (e.g., `./asset/battlebackground1.png`). Always execute commands and run the game from the root directory to avoid path resolution errors.

## Workflow & Execution
- **Environment:** A Python virtual environment is available at `.venv`. Activate it before running commands or installing dependencies (e.g., `.\.venv\Scripts\Activate.ps1` in PowerShell).
- **Run the Game:** Execute `python main.py` from the repository root.
- **Dependencies:** Listed in `requirements.txt`. Currently only requires `pygame==2.6.1`.
- **Testing:** There is no automated test suite. Verify code changes by running the game interactively. 

## Quirks & Conventions
- **Screen Resolution:** The game window size is hardcoded to `1920x1080` in `code/game.py`. Do not resize the window programmatically; the codebase relies on scaling/providing images to match this fixed resolution.
- **Debugging:** There are some `# TODO` comments (e.g., removing test player/enemy lines in `level.py`). Pay attention to these if doing cleanup.
