# Tetris Game Creation Prompt

Create a complete, fully functional Tetris game using HTML5 Canvas and JavaScript. The game should include all standard Tetris mechanics and features.

## Required Game Components

### 1. Game Board
- 10x20 grid (standard Tetris dimensions)
- Visual grid with block-based rendering
- Dark background with bordered cells

### 2. Tetris Pieces (Tetrominoes)
Include all 7 standard pieces with distinct colors:
- **I-piece** (straight line, 4 blocks) - Cyan
- **O-piece** (square, 2x2) - Yellow  
- **T-piece** (T-shape) - Purple
- **S-piece** (S-shape) - Green
- **Z-piece** (Z-shape) - Red
- **L-piece** (L-shape) - Orange
- **J-piece** (reverse L) - Blue

### 3. Core Mechanics
- **Piece Movement**: Left, right, down with arrow keys
- **Rotation**: Up arrow or specific rotation key
- **Soft Drop**: Hold down arrow for faster descent
- **Hard Drop**: Spacebar for instant drop to bottom
- **Automatic Falling**: Pieces fall automatically at timed intervals
- **Collision Detection**: Prevent invalid moves and placements
- **Line Clearing**: Remove completed horizontal lines
- **New Piece Spawning**: Generate random pieces at top center

### 4. Game Progression
- **Scoring System**: Points for line clears, soft drops, hard drops
- **Level System**: Increase level every 10 lines cleared
- **Speed Increase**: Faster falling speed with each level
- **Line Counter**: Track total lines cleared

### 5. User Interface
- Score display
- Current level indicator
- Lines cleared counter
- Game over screen with final score
- Restart/Play Again functionality
- Control instructions for players

### 6. Controls
- **Arrow Keys**: 
  - Left/Right: Move piece horizontally
  - Down: Soft drop (faster falling)
  - Up: Rotate piece clockwise
- **Spacebar**: Hard drop (instant drop)
- **P Key**: Pause/unpause game

### 7. Visual Design
- Modern, clean interface
- Smooth animations
- Distinct colors for each piece type
- Visual feedback for line clearing
- Attractive background and styling
- Responsive design elements

### 8. Game States
- **Playing**: Normal gameplay
- **Paused**: Game frozen, can resume
- **Game Over**: When pieces reach the top
- **Restart**: Reset all game variables

## Technical Requirements

### HTML Structure
- Canvas element for game rendering
- UI elements for score, level, controls
- Game over modal/overlay
- Responsive layout

### JavaScript Implementation
- Game loop using requestAnimationFrame
- Piece collision detection algorithms
- Line clearing logic
- Random piece generation
- Keyboard event handling
- Game state management

### Styling
- Modern CSS with gradients and effects
- Clean typography
- Hover effects on interactive elements
- Mobile-friendly responsive design

## Scoring System
- **Single line**: 100 × level points
- **Multiple lines**: Bonus multipliers
- **Soft drop**: 1 point per cell
- **Hard drop**: 2 points per cell

## Game Balance
- **Initial drop speed**: 1000ms intervals
- **Speed increase**: Decrease interval by 100ms per level
- **Minimum speed**: 50ms intervals (maximum difficulty)
- **Level progression**: Every 10 lines cleared

## Additional Features (Optional Enhancements)
- Next piece preview
- Hold piece functionality
- Ghost piece (shadow showing drop position)
- Sound effects
- High score persistence
- Multiple difficulty modes
- Touch controls for mobile devices

## Code Organization
Structure the code with clear separation:
- Game initialization
- Piece definitions and logic
- Board management functions
- Collision detection
- Line clearing algorithms
- Rendering functions
- Input handling
- Game loop and timing
- UI updates

The final result should be a complete, playable Tetris game that runs in any modern web browser without external dependencies.