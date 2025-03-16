# hyper-pong

Pong made in python

![hyper-pong Game](https://i.imgur.com/placeholder.png)

## Description

hyper-pong is a two-player arcade game where players control paddles to hit a ball back and forth. The game includes sound effects, background music, and colorful graphics. Score points by getting the ball past your opponent's paddle!

## Features

- Two-player local gameplay
- Sound effects and background music
- Colorful graphics with distinct paddles
- Score tracking
- Game state management (menu, gameplay, end screen)

## Installation

### Requirements

- Python 3.11 or later (recommended, tested with Python 3.11)
- pygame
- imageio

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/hyper-pong.git
   cd hyper-pong
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pygame imageio
   ```

## How to Play

### Starting the Game

Run the game using:
```bash
python simple_pong.py
```

### Controls

- **Player 1 (Pink Paddle - Left):**
  - **W:** Move Up
  - **S:** Move Down

- **Player 2 (Blue Paddle - Right):**
  - **Up Arrow:** Move Up
  - **Down Arrow:** Move Down

- **Game Controls:**
  - **SPACE:** Start a new game
  - **ESC:** Return to menu
  - **Close Window:** Quit game

### Rules

1. The game is played to 5 points
2. Score a point when the ball passes your opponent's paddle
3. The ball speeds up during rallies
4. The first player to reach 5 points wins

## Project Structure

```
hyper-pong/
├── simple_pong.py       # Main game file
├── assets/              # Game assets
│   ├── audio/           # Audio files
│   │   ├── music/       # Background music
│   │   └── sfx/         # Sound effects
│   └── images/          # Game images
├── venv/                # Virtual environment (not tracked in git)
└── README.md            # This file
```

## Credits

- Sound effects: Audio assets used under permissive licenses
- Original Pong concept by Atari
- Developed by Daniel Semmelmann

## License

This project is licensed under the MIT License - see the LICENSE file for details.
