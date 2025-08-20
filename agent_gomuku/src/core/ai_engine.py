import time
import numpy as np
from typing import List, Tuple, Optional, Dict
from .game_board import GameBoard, Stone
from .heuristic import HeuristicEvaluator

class AIEngine:
    """Advanced AI engine using Minimax with Alpha-Beta pruning and sophisticated heuristics."""
    
    def __init__(self, max_depth: int = 10, time_limit: float = 0.5):
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.heuristic = HeuristicEvaluator()
        self.nodes_evaluated = 0
        self.start_time = 0
        self.transposition_table = {}
        
    def get_best_move(self, board: GameBoard, player: Stone) -> Tuple[int, int]:
        """Get the best move for the AI player within the time limit."""
        self.start_time = time.time()
        self.nodes_evaluated = 0
        self.transposition_table.clear()
        
        # Get candidate moves to reduce search space
        candidate_moves = self.get_candidate_moves(board, player)
        
        if not candidate_moves:
            # Fallback to all valid moves if no candidates
            candidate_moves = board.get_valid_moves()
        
        if not candidate_moves:
            return None
        
        # Sort moves by immediate threat level for better alpha-beta pruning
        candidate_moves = self.sort_moves_by_threat(board, candidate_moves, player)
        
        best_move = candidate_moves[0]
        best_score = float('-inf') if player == Stone.BLACK else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Iterative deepening to maximize search depth within time limit
        for depth in range(1, self.max_depth + 1):
            if time.time() - self.start_time > self.time_limit:
                break
                
            current_best_move = candidate_moves[0]
            current_best_score = float('-inf') if player == Stone.BLACK else float('inf')
            
            for move in candidate_moves:
                if time.time() - self.start_time > self.time_limit:
                    break
                    
                # Make the move
                test_board = self.make_test_move(board, move, player)
                
                # Evaluate the position
                if player == Stone.BLACK:
                    score = self.minimax(test_board, depth - 1, alpha, beta, False, Stone.WHITE)
                    if score > current_best_score:
                        current_best_score = score
                        current_best_move = move
                    alpha = max(alpha, score)
                else:
                    score = self.minimax(test_board, depth - 1, alpha, beta, True, Stone.BLACK)
                    if score < current_best_score:
                        current_best_score = score
                        current_best_move = move
                    beta = min(beta, score)
                
                if alpha >= beta:
                    break  # Beta cutoff
            
            # Update best move if we completed this depth
            if time.time() - self.start_time <= self.time_limit:
                best_move = current_best_move
                best_score = current_best_score
        
        return best_move
    
    def minimax(self, board: GameBoard, depth: int, alpha: float, beta: float, 
                maximizing: bool, current_player: Stone) -> float:
        """Minimax algorithm with Alpha-Beta pruning."""
        self.nodes_evaluated += 1
        
        # Check time limit
        if time.time() - self.start_time > self.time_limit:
            return 0
        
        # Check for terminal states
        if board.is_game_over() or depth == 0:
            return self.heuristic.evaluate_position(board, current_player)
        
        # Check transposition table
        board_hash = self.get_board_hash(board)
        if board_hash in self.transposition_table:
            stored_depth, stored_score = self.transposition_table[board_hash]
            if stored_depth >= depth:
                return stored_score
        
        # Get candidate moves for current position
        candidate_moves = self.get_candidate_moves(board, current_player)
        
        if maximizing:
            max_eval = float('-inf')
            for move in candidate_moves:
                test_board = self.make_test_move(board, move, current_player)
                eval_score = self.minimax(test_board, depth - 1, alpha, beta, False, 
                                        Stone.WHITE if current_player == Stone.BLACK else Stone.BLACK)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            eval_score = max_eval
        else:
            min_eval = float('inf')
            for move in candidate_moves:
                test_board = self.make_test_move(board, move, current_player)
                eval_score = self.minimax(test_board, depth - 1, alpha, beta, True,
                                        Stone.WHITE if current_player == Stone.BLACK else Stone.BLACK)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            eval_score = min_eval
        
        # Store in transposition table
        self.transposition_table[board_hash] = (depth, eval_score)
        
        return eval_score
    
    def get_candidate_moves(self, board: GameBoard, player: Stone) -> List[Tuple[int, int]]:
        """Get candidate moves to reduce search space."""
        valid_moves = board.get_valid_moves()
        if len(valid_moves) <= 20:  # If few moves, consider all
            return valid_moves
        
        # Focus on moves near existing stones
        candidate_moves = []
        board_state = board.get_board_state()
        
        for row, col in valid_moves:
            # Check if move is near existing stones (within 2 squares)
            is_near_stones = False
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    r, c = row + dr, col + dc
                    if (0 <= r < board.size and 0 <= c < board.size and 
                        board_state[r, c] != Stone.EMPTY.value):
                        is_near_stones = True
                        break
                if is_near_stones:
                    break
            
            if is_near_stones:
                candidate_moves.append((row, col))
        
        # If no moves near stones, add some strategic positions
        if not candidate_moves:
            # Add center and corner moves
            center = board.size // 2
            candidate_moves.extend([(center, center), (0, 0), (0, board.size-1), 
                                  (board.size-1, 0), (board.size-1, board.size-1)])
        
        return candidate_moves[:min(20, len(candidate_moves))]  # Limit to 20 moves
    
    def sort_moves_by_threat(self, board: GameBoard, moves: List[Tuple[int, int]], 
                            player: Stone) -> List[Tuple[int, int]]:
        """Sort moves by immediate threat level for better alpha-beta pruning."""
        move_scores = []
        
        for move in moves:
            score = 0
            test_board = self.make_test_move(board, move, player)
            
            # Check for immediate wins
            if test_board.is_game_over():
                score = 10000
            
            # Check for captures
            captures = test_board.get_captures(player)
            score += captures * 100
            
            # Check for creating threats
            score += self.evaluate_move_threat(test_board, move, player)
            
            move_scores.append((move, score))
        
        # Sort by score (descending for BLACK, ascending for WHITE)
        if player == Stone.BLACK:
            move_scores.sort(key=lambda x: x[1], reverse=True)
        else:
            move_scores.sort(key=lambda x: x[1])
        
        return [move for move, score in move_scores]
    
    def evaluate_move_threat(self, board: GameBoard, move: Tuple[int, int], 
                           player: Stone) -> int:
        """Evaluate the threat level of a move."""
        score = 0
        row, col = move
        
        # Check for creating free threes
        if not board.would_create_double_three(row, col):
            # This is a simplified check - in full implementation, you'd analyze
            # the actual threat patterns created
            score += 50
        
        return score
    
    def make_test_move(self, board: GameBoard, move: Tuple[int, int], 
                      player: Stone) -> GameBoard:
        """Create a test board with a move made."""
        test_board = GameBoard(board.size)
        test_board.board = board.get_board_state().copy()
        test_board.current_player = player
        test_board.captures = board.captures.copy()
        test_board.game_over = board.game_over
        test_board.winner = board.winner
        
        # Make the move
        test_board.make_move(move[0], move[1])
        
        return test_board
    
    def get_board_hash(self, board: GameBoard) -> str:
        """Generate a hash for the board state for transposition table."""
        return str(board.board.tobytes())
    
    def get_search_stats(self) -> Dict:
        """Get statistics about the last search."""
        elapsed_time = time.time() - self.start_time
        return {
            'nodes_evaluated': self.nodes_evaluated,
            'elapsed_time': elapsed_time,
            'nodes_per_second': self.nodes_evaluated / elapsed_time if elapsed_time > 0 else 0
        }

