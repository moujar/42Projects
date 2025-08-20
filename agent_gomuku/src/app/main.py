#!/usr/bin/env python3
"""
Gomoku - Advanced AI Implementation
Main application entry point

This program implements the Gomoku project requirements with:
- 19x19 board with all specified rules (captures, double-threes, etc.)
- Advanced AI using Minimax with Alpha-Beta pruning
- Sophisticated heuristics for pattern recognition
- Both game modes: Player vs AI and Player vs Player
- Graphical interface with timers and move suggestions
- Performance optimization to achieve 10+ search depth
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from .gui import GomokuGUI

def main():
    """Main function to launch the Gomoku game."""
    try:
        print("Starting Gomoku...")
        print("Game Features:")
        print("- 19x19 board with Gomoku rules")
        print("- Advanced AI with Minimax + Alpha-Beta pruning")
        print("- Both game modes: AI vs Human, Human vs Human")
        print("- Move suggestions and timing display")
        print("- All required rules: captures, double-threes, endgame captures")
        print()
        print("Controls:")
        print("- Mouse: Place stones")
        print("- R: Reset game")
        print("- M: Toggle game mode")
        print("- S: Show move suggestion (Human vs Human mode)")
        print("- ESC: Quit")
        print()
        
        # Launch the GUI
        gui = GomokuGUI()
        gui.run()
        
    except Exception as e:
        print(f"Error starting Gomoku: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

