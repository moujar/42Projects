import numpy as np
from typing import List, Tuple, Dict
from .game_board import GameBoard, Stone

class HeuristicEvaluator:
    """Advanced heuristic evaluator for Gomoku positions."""
    
    def __init__(self):
        # Pattern scores based on the thesis
        self.pattern_scores = {
            'five_in_row': 10000,
            'live_four': 5000,
            'dead_four': 1000,
            'live_three': 500,
            'dead_three': 100,
            'live_two': 50,
            'dead_two': 10,
            'single_stone': 1
        }
        
        # Capture bonus
        self.capture_bonus = 200
        
    def evaluate_position(self, board: GameBoard, current_player: Stone) -> float:
        """Evaluate the current board position."""
        if board.is_game_over():
            if board.get_winner() == Stone.BLACK:
                return 10000
            elif board.get_winner() == Stone.WHITE:
                return -10000
            else:
                return 0
        
        # Base score from captures
        capture_score = (board.get_captures(Stone.BLACK) - board.get_captures(Stone.WHITE)) * self.capture_bonus
        
        # Pattern analysis score
        pattern_score = self.analyze_patterns(board)
        
        # Position control score
        position_score = self.evaluate_position_control(board)
        
        # Mobility score
        mobility_score = self.evaluate_mobility(board)
        
        # Combine scores
        total_score = capture_score + pattern_score + position_score + mobility_score
        
        # Adjust for current player perspective
        if current_player == Stone.WHITE:
            total_score = -total_score
        
        return total_score
    
    def analyze_patterns(self, board: GameBoard) -> float:
        """Analyze stone patterns on the board."""
        board_state = board.get_board_state()
        black_score = 0
        white_score = 0
        
        # Analyze in all directions
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for row in range(board.size):
            for col in range(board.size):
                if board_state[row, col] != Stone.EMPTY.value:
                    player = Stone.BLACK if board_state[row, col] == Stone.BLACK.value else Stone.WHITE
                    
                    for dr, dc in directions:
                        pattern_score = self.analyze_line_pattern(board_state, row, col, dr, dc, player)
                        
                        if player == Stone.BLACK:
                            black_score += pattern_score
                        else:
                            white_score += pattern_score
        
        return black_score - white_score
    
    def analyze_line_pattern(self, board_state: np.ndarray, row: int, col: int, 
                           dr: int, dc: int, player: Stone) -> float:
        """Analyze the pattern in a specific direction from a position."""
        player_value = player.value
        score = 0
        
        # Look for consecutive stones
        consecutive = 1
        blocked_left = False
        blocked_right = False
        
        # Count consecutive stones to the left
        r, c = row - dr, col - dc
        while 0 <= r < board_state.shape[0] and 0 <= c < board_state.shape[1]:
            if board_state[r, c] == player_value:
                consecutive += 1
                r -= dr
                c -= dc
            else:
                blocked_left = (board_state[r, c] != Stone.EMPTY.value)
                break
        
        # Count consecutive stones to the right
        r, c = row + dr, col + dc
        while 0 <= r < board_state.shape[0] and 0 <= c < board_state.shape[1]:
            if board_state[r, c] == player_value:
                consecutive += 1
                r += dr
                c += dc
            else:
                blocked_right = (board_state[r, c] != Stone.EMPTY.value)
                break
        
        # Score based on pattern type
        if consecutive >= 5:
            score = self.pattern_scores['five_in_row']
        elif consecutive == 4:
            if not blocked_left and not blocked_right:
                score = self.pattern_scores['live_four']
            elif not blocked_left or not blocked_right:
                score = self.pattern_scores['dead_four']
            else:
                score = self.pattern_scores['dead_four'] // 2
        elif consecutive == 3:
            if not blocked_left and not blocked_right:
                score = self.pattern_scores['live_three']
            elif not blocked_left or not blocked_right:
                score = self.pattern_scores['dead_three']
            else:
                score = self.pattern_scores['dead_three'] // 2
        elif consecutive == 2:
            if not blocked_left and not blocked_right:
                score = self.pattern_scores['live_two']
            elif not blocked_left or not blocked_right:
                score = self.pattern_scores['dead_two']
            else:
                score = self.pattern_scores['dead_two'] // 2
        else:
            score = self.pattern_scores['single_stone']
        
        return score
    
    def evaluate_position_control(self, board: GameBoard) -> float:
        """Evaluate control of key board positions."""
        board_state = board.get_board_state()
        black_control = 0
        white_control = 0
        
        # Center control is valuable
        center = board.size // 2
        center_radius = 3
        
        for row in range(max(0, center - center_radius), min(board.size, center + center_radius + 1)):
            for col in range(max(0, center - center_radius), min(board.size, center + center_radius + 1)):
                if board_state[row, col] == Stone.BLACK.value:
                    # Closer to center = more valuable
                    distance = abs(row - center) + abs(col - center)
                    black_control += max(0, center_radius - distance)
                elif board_state[row, col] == Stone.WHITE.value:
                    distance = abs(row - center) + abs(col - center)
                    white_control += max(0, center_radius - distance)
        
        # Corner control
        corners = [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]
        for row, col in corners:
            if board_state[row, col] == Stone.BLACK.value:
                black_control += 10
            elif board_state[row, col] == Stone.WHITE.value:
                white_control += 10
        
        return (black_control - white_control) * 5
    
    def evaluate_mobility(self, board: GameBoard) -> float:
        """Evaluate the mobility (number of valid moves) for each player."""
        # Count valid moves for each player
        black_moves = 0
        white_moves = 0
        
        # This is a simplified approach - in practice, you'd need to check
        # which moves are actually valid for each player
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row, col] == Stone.EMPTY.value:
                    # Check if this move would be valid for either player
                    if board.is_valid_move(row, col):
                        black_moves += 1
                    
                    # Temporarily switch players to check white moves
                    original_player = board.current_player
                    board.current_player = Stone.WHITE
                    if board.is_valid_move(row, col):
                        white_moves += 1
                    board.current_player = original_player
        
        return (black_moves - white_moves) * 2
    
    def get_pattern_analysis(self, board: GameBoard) -> Dict:
        """Get detailed pattern analysis for debugging."""
        board_state = board.get_board_state()
        analysis = {
            'black_patterns': {},
            'white_patterns': {},
            'total_score': 0
        }
        
        # Count patterns for each player
        for pattern in self.pattern_scores.keys():
            analysis['black_patterns'][pattern] = 0
            analysis['white_patterns'][pattern] = 0
        
        # Analyze patterns (simplified)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for row in range(board.size):
            for col in range(board.size):
                if board_state[row, col] != Stone.EMPTY.value:
                    player = Stone.BLACK if board_state[row, col] == Stone.BLACK.value else Stone.WHITE
                    
                    for dr, dc in directions:
                        pattern_type = self.get_pattern_type(board_state, row, col, dr, dc, player)
                        if pattern_type:
                            if player == Stone.BLACK:
                                analysis['black_patterns'][pattern_type] += 1
                            else:
                                analysis['white_patterns'][pattern_type] += 1
        
        return analysis
    
    def get_pattern_type(self, board_state: np.ndarray, row: int, col: int, 
                        dr: int, dc: int, player: Stone) -> str:
        """Get the type of pattern in a specific direction."""
        player_value = player.value
        consecutive = 1
        
        # Count consecutive stones
        r, c = row - dr, col - dc
        while 0 <= r < board_state.shape[0] and 0 <= c < board_state.shape[1]:
            if board_state[r, c] == player_value:
                consecutive += 1
                r -= dr
                c -= dc
            else:
                break
        
        r, c = row + dr, col + dc
        while 0 <= r < board_state.shape[0] and 0 <= c < board_state.shape[1]:
            if board_state[r, c] == player_value:
                consecutive += 1
                r += dr
                c += dc
            else:
                break
        
        if consecutive >= 5:
            return 'five_in_row'
        elif consecutive == 4:
            return 'live_four'
        elif consecutive == 3:
            return 'live_three'
        elif consecutive == 2:
            return 'live_two'
        else:
            return 'single_stone'

