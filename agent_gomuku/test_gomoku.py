#!/usr/bin/env python3
"""
Test script for Gomoku implementation
Tests core functionality without requiring GUI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.game_board import GameBoard, Stone
from core.ai_engine import AIEngine
from core.heuristic import HeuristicEvaluator

def test_game_board():
    """Test basic game board functionality."""
    print("Testing Game Board...")
    
    board = GameBoard()
    
    # Test initial state
    assert board.get_current_player() == Stone.BLACK
    assert board.is_game_over() == False
    assert board.get_winner() == None
    assert board.get_captures(Stone.BLACK) == 0
    assert board.get_captures(Stone.WHITE) == 0
    
    # Test valid moves
    valid_moves = board.get_valid_moves()
    assert len(valid_moves) == 361  # 19x19 board
    
    # Test first move
    assert board.make_move(9, 9) == True  # Center move
    assert board.get_current_player() == Stone.WHITE
    assert board.board[9, 9] == Stone.BLACK.value
    
    print("✅ Game Board tests passed")

def test_game_rules():
    """Test Gomoku game rules."""
    print("Testing Game Rules...")
    
    board = GameBoard()
    
    # Test five in a row win
    moves = [(9, 9), (9, 10), (9, 11), (9, 12), (9, 13)]
    for i, (row, col) in enumerate(moves):
        if i < 4:  # First 4 moves
            board.make_move(row, col)
        else:  # 5th move should win
            board.make_move(row, col)
            assert board.is_game_over() == True
            assert board.get_winner() == Stone.BLACK
    
    print("✅ Game Rules tests passed")

def test_ai_engine():
    """Test AI engine functionality."""
    print("Testing AI Engine...")
    
    board = GameBoard()
    ai = AIEngine(max_depth=5, time_limit=1.0)
    
    # Test AI move generation
    move = ai.get_best_move(board, Stone.WHITE)
    assert move is not None
    assert len(move) == 2
    assert 0 <= move[0] < 19
    assert 0 <= move[1] < 19
    
    # Test search statistics
    stats = ai.get_search_stats()
    assert 'nodes_evaluated' in stats
    assert 'elapsed_time' in stats
    
    print("✅ AI Engine tests passed")

def test_heuristic():
    """Test heuristic evaluation."""
    print("Testing Heuristic...")
    
    board = GameBoard()
    heuristic = HeuristicEvaluator()
    
    # Test empty board evaluation
    score = heuristic.evaluate_position(board, Stone.BLACK)
    assert isinstance(score, (int, float))
    
    # Test pattern analysis
    analysis = heuristic.get_pattern_analysis(board)
    assert 'black_patterns' in analysis
    assert 'white_patterns' in analysis
    
    print("✅ Heuristic tests passed")

def test_integration():
    """Test integrated functionality."""
    print("Testing Integration...")
    
    board = GameBoard()
    ai = AIEngine(max_depth=3, time_limit=0.5)
    
    # Play a few moves
    board.make_move(9, 9)  # Black center
    ai_move = ai.get_best_move(board, Stone.WHITE)
    board.make_move(ai_move[0], ai_move[1])  # AI move
    
    # Verify game state
    assert board.get_current_player() == Stone.BLACK
    assert board.is_game_over() == False
    
    print("✅ Integration tests passed")

def main():
    """Run all tests."""
    print("🧪 Running Gomoku Tests...\n")
    
    try:
        test_game_board()
        test_game_rules()
        test_ai_engine()
        test_heuristic()
        test_integration()
        
        print("\n🎉 All tests passed! Gomoku implementation is working correctly.")
        print("\nTo play the game, run:")
        print("  make run")
        print("  or")
        print("  python src/app/main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

