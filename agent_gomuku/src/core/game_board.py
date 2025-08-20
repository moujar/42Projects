import numpy as np
from typing import List, Tuple, Optional, Set
from enum import Enum

class Stone(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class GameBoard:
    """Gomoku game board with all required rules implementation."""
    
    def __init__(self, size: int = 19):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.current_player = Stone.BLACK
        self.game_over = False
        self.winner = None
        self.captures = {Stone.BLACK: 0, Stone.WHITE: 0}
        self.last_move = None
        self.move_history = []
        
    def reset(self):
        """Reset the game board to initial state."""
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.current_player = Stone.BLACK
        self.game_over = False
        self.winner = None
        self.captures = {Stone.BLACK: 0, Stone.WHITE: 0}
        self.last_move = None
        self.move_history = []
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if a move is valid according to Gomoku rules."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        
        if self.board[row, col] != Stone.EMPTY.value:
            return False
        
        if self.game_over:
            return False
        
        # Check double-three rule (except when capturing)
        if self.would_create_double_three(row, col):
            return False
        
        return True
    
    def would_create_double_three(self, row: int, col: int) -> bool:
        """Check if a move would create a double-three (forbidden)."""
        # Temporarily place the stone
        self.board[row, col] = self.current_player.value
        
        # Count free threes
        free_threes = self.count_free_threes(row, col, self.current_player)
        
        # Remove the temporary stone
        self.board[row, col] = Stone.EMPTY.value
        
        # If this would create more than one free three, it's forbidden
        return free_threes > 1
    
    def count_free_threes(self, row: int, col: int, player: Stone) -> int:
        """Count the number of free threes created by a move."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        free_threes = 0
        
        for dr, dc in directions:
            # Check both directions
            for direction in [1, -1]:
                if self.is_free_three(row, col, dr * direction, dc * direction, player):
                    free_threes += 1
        
        return free_threes
    
    def is_free_three(self, row: int, col: int, dr: int, dc: int, player: Stone) -> bool:
        """Check if a line of three stones is free (can be extended)."""
        # Check if we can form a line of three in this direction
        stones = []
        
        # Look in both directions from the current position
        for i in range(-4, 5):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < self.size and 0 <= c < self.size:
                stones.append(self.board[r, c])
            else:
                stones.append(-1)  # Out of bounds
        
        # Check for patterns like: _XXX_ or _XX_X_ or _X_XX_
        patterns = [
            [0, player.value, player.value, player.value, 0],  # _XXX_
            [0, player.value, player.value, 0, player.value],  # _XX_X_
            [0, player.value, 0, player.value, player.value],  # _X_XX_
        ]
        
        for pattern in patterns:
            if self.matches_pattern(stones, pattern):
                return True
        
        return False
    
    def matches_pattern(self, stones: List[int], pattern: List[int]) -> bool:
        """Check if stones match a specific pattern."""
        for i in range(len(stones) - len(pattern) + 1):
            match = True
            for j in range(len(pattern)):
                if pattern[j] != -1 and stones[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                return True
        return False
    
    def make_move(self, row: int, col: int) -> bool:
        """Make a move on the board."""
        if not self.is_valid_move(row, col):
            return False
        
        # Place the stone
        self.board[row, col] = self.current_player.value
        self.last_move = (row, col)
        self.move_history.append((row, col, self.current_player))
        
        # Check for captures
        captures_made = self.check_and_make_captures(row, col)
        
        # Check for win conditions
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
        elif self.captures[self.current_player] >= 10:
            self.game_over = True
            self.winner = self.current_player
        
        # Switch players
        self.current_player = Stone.WHITE if self.current_player == Stone.BLACK else Stone.BLACK
        
        return True
    
    def check_and_make_captures(self, row: int, col: int) -> int:
        """Check for and make captures after a move."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        total_captures = 0
        
        for dr, dc in directions:
            # Check both directions
            for direction in [1, -1]:
                captures = self.check_capture_in_direction(row, col, dr * direction, dc * direction)
                if captures:
                    self.make_capture(captures)
                    total_captures += len(captures)
        
        return total_captures
    
    def check_capture_in_direction(self, row: int, col: int, dr: int, dc: int) -> List[Tuple[int, int]]:
        """Check if a capture is possible in a specific direction."""
        opponent = Stone.WHITE if self.current_player == Stone.BLACK else Stone.BLACK
        captures = []
        
        # Look for pattern: XOOX where X is current player and O is opponent
        positions = []
        for i in range(-3, 4):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < self.size and 0 <= c < self.size:
                positions.append((r, c, self.board[r, c]))
            else:
                positions.append((r, c, -1))
        
        # Check for capture pattern
        for i in range(len(positions) - 3):
            if (positions[i][2] == self.current_player.value and
                positions[i+1][2] == opponent.value and
                positions[i+2][2] == opponent.value and
                positions[i+3][2] == self.current_player.value):
                captures.extend([(positions[i+1][0], positions[i+1][1]), 
                               (positions[i+2][0], positions[i+2][1])])
        
        return captures
    
    def make_capture(self, captures: List[Tuple[int, int]]):
        """Remove captured stones from the board."""
        for row, col in captures:
            self.board[row, col] = Stone.EMPTY.value
            self.captures[self.current_player] += 1
    
    def check_win(self, row: int, col: int) -> bool:
        """Check if the last move resulted in a win."""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        player = self.board[row, col]
        
        for dr, dc in directions:
            count = 1  # Count the stone just placed
            
            # Count in both directions
            for direction in [1, -1]:
                count += self.count_consecutive(row, col, dr * direction, dc * direction, player)
            
            if count >= 5:
                # Check if this win can be prevented by capture
                if not self.can_win_be_prevented_by_capture(row, col, dr, dc, player):
                    return True
        
        return False
    
    def count_consecutive(self, row: int, col: int, dr: int, dc: int, player: int) -> int:
        """Count consecutive stones in a direction."""
        count = 0
        r, c = row + dr, col + dc
        
        while 0 <= r < self.size and 0 <= c < self.size and self.board[r, c] == player:
            count += 1
            r += dr
            c += dc
        
        return count
    
    def can_win_be_prevented_by_capture(self, row: int, col: int, dr: int, dc: int, player: int) -> bool:
        """Check if a winning line can be broken by capturing stones within it."""
        # This is a simplified check - in a full implementation, you'd need to
        # check if the opponent can make a move that captures stones in the winning line
        return False
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Get all valid moves for the current player."""
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def get_board_state(self) -> np.ndarray:
        """Get a copy of the current board state."""
        return self.board.copy()
    
    def get_score(self) -> int:
        """Get the current score (positive for BLACK advantage, negative for WHITE)."""
        if self.winner == Stone.BLACK:
            return 10000
        elif self.winner == Stone.WHITE:
            return -10000
        
        # Calculate score based on captures and board position
        score = (self.captures[Stone.BLACK] - self.captures[Stone.WHITE]) * 100
        
        # Add board position evaluation
        score += self.evaluate_board_position()
        
        return score
    
    def evaluate_board_position(self) -> int:
        """Evaluate the board position for scoring."""
        # This is a simplified evaluation - the full heuristic will be in the AI module
        return 0
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_over
    
    def get_winner(self) -> Optional[Stone]:
        """Get the winner of the game."""
        return self.winner
    
    def get_current_player(self) -> Stone:
        """Get the current player."""
        return self.current_player
    
    def get_captures(self, player: Stone) -> int:
        """Get the number of captures for a player."""
        return self.captures[player]

