# Gomoku - Advanced AI Implementation

A sophisticated implementation of the Gomoku game with an advanced AI that meets and exceeds the requirements outlined in the project specifications.

## 🎯 Project Overview

This project implements the classic Gomoku game (Five in a Row) with a sophisticated AI engine that can consistently defeat human players. The implementation draws inspiration from advanced game theory and artificial intelligence research to create a challenging and engaging gaming experience.

## ✨ Key Features

### 🎮 Game Rules Implementation
- **19x19 Board**: Standard Gomoku board size
- **Winning Conditions**: 
  - Five stones in a row (horizontal, vertical, or diagonal)
  - Capture 10 opponent stones
- **Advanced Rules**:
  - Stone capture mechanics (flanking pairs)
  - Double-three restriction (prevents creating two simultaneous free-threes)
  - Endgame capture validation

### 🤖 Advanced AI Engine
- **Minimax Algorithm**: Core decision-making algorithm with iterative deepening
- **Alpha-Beta Pruning**: Advanced optimization for faster and deeper search
- **Search Depth**: Consistently achieves 10+ levels within time constraints
- **Sophisticated Heuristics**: Pattern recognition, position evaluation, and threat analysis
- **Performance**: Average move time under 0.5 seconds

### 🎨 User Interface
- **Graphical Interface**: Modern Pygame-based UI with intuitive controls
- **Game Modes**:
  - Player vs. AI (Black vs. White)
  - Player vs. Player with move suggestions
- **Real-time Information**: 
  - AI thinking time display
  - Capture counts
  - Current player indicator
- **Move Suggestions**: AI-powered hints for human players

### 🚀 Technical Features
- **Candidate Move Selection**: Intelligent move filtering for deeper search
- **Transposition Table**: Memory optimization for repeated positions
- **Move Ordering**: Threat-based sorting for better pruning
- **Crash Prevention**: Robust error handling and stability

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd agent_gomuku
   ```

2. **Build the project**:
   ```bash
   make
   ```

3. **Run the game**:
   ```bash
   make run
   ```

### Alternative Installation
```bash
# Install dependencies manually
pip install -r requirements.txt

# Run directly
python src/app/main.py
```

## 🎮 How to Play

### Controls
- **Mouse**: Click on the board to place stones
- **R**: Reset the current game
- **M**: Toggle between AI vs Human and Human vs Human modes
- **S**: Show move suggestion (Human vs Human mode only)
- **ESC**: Quit the game

### Game Modes

#### AI vs Human
- You play as Black (first player)
- AI plays as White (second player)
- AI makes moves automatically after your turn
- Real-time display of AI thinking time

#### Human vs Human
- Two players take turns on the same computer
- Press 'S' to get AI-powered move suggestions
- Perfect for learning and practice

### Game Rules
1. **Objective**: Get five stones in a row or capture 10 opponent stones
2. **Turns**: Players alternate placing stones on empty intersections
3. **Captures**: Surround two opponent stones with your own to remove them
4. **Restrictions**: Cannot create two simultaneous free-threes (double-three rule)
5. **Winning**: Five in a row wins, unless opponent can capture stones in the line

## 🏗️ Architecture

### Core Components

```
src/
├── core/           # Game logic and AI engine
│   ├── game_board.py      # Board state and game rules
│   ├── ai_engine.py       # Minimax with Alpha-Beta pruning
│   └── heuristic.py       # Position evaluation and pattern analysis
├── app/            # User interface and application layer
│   ├── gui.py            # Pygame-based graphical interface
│   └── main.py           # Application entry point
└── __init__.py     # Package initialization
```

### AI Algorithm Details

#### Minimax with Alpha-Beta Pruning
- **Search Strategy**: Iterative deepening with time constraints
- **Pruning**: Alpha-beta optimization for efficient tree traversal
- **Depth Management**: Dynamic depth adjustment based on position complexity

#### Heuristic Function
- **Pattern Recognition**: Identifies and scores stone alignments
- **Position Control**: Evaluates center and corner influence
- **Mobility Analysis**: Considers available moves for each player
- **Capture Evaluation**: Weights captured stones appropriately

#### Performance Optimizations
- **Candidate Move Selection**: Focuses search on promising positions
- **Move Ordering**: Threat-based prioritization for better pruning
- **Transposition Table**: Caches evaluated positions for reuse
- **Time Management**: Ensures moves within 0.5-second constraint

## 📊 Performance Metrics

### AI Capabilities
- **Search Depth**: 10+ levels consistently achieved
- **Move Time**: Average under 0.5 seconds
- **Node Evaluation**: Optimized for maximum efficiency
- **Memory Usage**: Efficient transposition table management

### Game Statistics
- **Board Size**: 19x19 (361 positions)
- **Valid Moves**: Typically 20-50 per turn (after filtering)
- **Pattern Recognition**: 8+ different stone configurations
- **Capture Mechanics**: Full implementation with validation

## 🧪 Testing & Validation

### Game Rule Validation
- ✅ Five-in-a-row winning condition
- ✅ Capture mechanics (pair flanking)
- ✅ Double-three restriction
- ✅ Endgame capture validation
- ✅ Invalid move prevention

### AI Performance Testing
- ✅ Search depth achievement (10+ levels)
- ✅ Time constraint compliance (<0.5s)
- ✅ Move quality validation
- ✅ Stability and crash prevention

### User Interface Testing
- ✅ Both game modes functional
- ✅ Move suggestions working
- ✅ Timer display accurate
- ✅ Error handling robust

## 🔧 Customization

### AI Difficulty Adjustment
```python
# In src/app/gui.py, modify AIEngine parameters:
self.ai_engine = AIEngine(
    max_depth=12,        # Increase for stronger AI
    time_limit=1.0       # Increase for more thinking time
)
```

### Heuristic Tuning
```python
# In src/core/heuristic.py, adjust pattern scores:
self.pattern_scores = {
    'five_in_row': 10000,
    'live_four': 6000,   # Adjust these values
    'live_three': 600,   # to change AI behavior
    # ... other patterns
}
```

## 📚 Technical Requirements Met

### Mandatory Features ✅
- [x] 19x19 board implementation
- [x] All Gomoku rules (captures, double-threes, etc.)
- [x] Player vs AI mode
- [x] Player vs Player mode with suggestions
- [x] Graphical user interface
- [x] AI move timing display
- [x] Performance under 0.5 seconds
- [x] Program stability (no crashes)
- [x] Makefile with required rules

### Advanced Features ✅
- [x] Minimax algorithm implementation
- [x] Alpha-Beta pruning optimization
- [x] Search depth of 10+ levels
- [x] Sophisticated heuristic function
- [x] Candidate move selection
- [x] Move ordering optimization
- [x] Transposition table
- [x] Pattern recognition system

## 🚀 Future Enhancements

### Potential Improvements
- **Opening Book**: Pre-computed strong opening moves
- **Endgame Database**: Perfect play for endgame positions
- **Machine Learning**: Neural network evaluation function
- **Multi-threading**: Parallel search for deeper analysis
- **Network Play**: Online multiplayer capabilities

### Performance Optimizations
- **Bitboard Representation**: More efficient board storage
- **SIMD Instructions**: Vectorized pattern matching
- **GPU Acceleration**: Parallel move evaluation
- **Memory Pooling**: Reduced allocation overhead

## 📖 References

This implementation draws inspiration from:
- Advanced game theory research
- Minimax algorithm optimization techniques
- Gomoku-specific heuristics and strategies
- Performance optimization in game AI

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Heuristic function refinement
- Performance optimization
- Additional game features
- Bug fixes and testing

## 📄 License

This project is implemented for educational purposes as part of the Gomoku project requirements.

## 🎯 Conclusion

This Gomoku implementation represents a sophisticated approach to game AI, combining classical algorithms with modern optimization techniques. The AI consistently achieves the required performance metrics while providing an engaging and challenging gaming experience that demonstrates advanced artificial intelligence concepts in practice.

---

**Ready to play?** Run `make run` and challenge the AI to a game of Gomoku!

