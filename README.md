## Key Features:

**Game Mechanics:**
- Classic Snake gameplay - eat food to grow longer
- Collision detection for walls and self-collision
- Score tracking with high score persistence
- Smooth movement and responsive controls

**Enhanced Design:**
- Clean object-oriented structure with separate classes for Snake, Food, and Game
- State management system (Menu, Playing, Game Over)
- Visual improvements with colored snake head and grid overlay
- Multiple control schemes (Arrow keys or WASD)

**User Experience:**
- Start screen with instructions
- Game over screen with restart options
- Real-time score and length display
- High score tracking
- Easy navigation between game states

## How to Run:

1. Make sure you have pygame installed: `pip install pygame`
2. Save the code to a `.py` file
3. Run it with Python: `python snake_game.py`

## Controls:
- **Menu/Game Over:** SPACE to start/restart, ESC to quit/return to menu
- **Playing:** Arrow keys or WASD to move, ESC to return to menu

The game maintains the core Snake gameplay while providing a much more polished experience with better code organization, visual feedback, and user interface. The snake grows each time it eats food, and the game ends when you hit the walls or your own body!