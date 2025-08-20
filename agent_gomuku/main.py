
import sys
import pygame
import time
from typing import Tuple, Optional

# --- Constants and Board Setup ---
BOARD_SIZE = 19
EMPTY, P1, P2 = 0, 1, 2  # P1 is human, P2 is AI

# Pygame constants
WINDOW_SIZE = 1000  # Increased to accommodate left panel
BOARD_MARGIN = 50
CELL_SIZE = (WINDOW_SIZE - 2 * BOARD_MARGIN - 200) // BOARD_SIZE  # Adjust for left panel
BOARD_OFFSET_X = 250  # Start board further right to make room for left panel
BOARD_OFFSET_Y = (WINDOW_SIZE - BOARD_SIZE * CELL_SIZE) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)

class GomokuGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Gomoku Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 72)
        
        self.reset_game()
        
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = self.create_board()
        self.game_over = False
        self.current_player = P1  # Human starts
        self.start_time = time.time()
        self.last_move_time = time.time()
        self.move_times = []  # Track time per move
        self.human_move_times = []  # Track human move times
        self.ai_move_times = []  # Track AI move times
        self.winner = None
        self.show_popup = False
        self.popup_start_time = 0
        self.ai_thinking_start = 0
        self.is_ai_thinking = False
        self.human_move_start = time.time()  # Start timing human's first move
        
    def create_board(self):
        """Creates an empty Gomoku board."""
        return [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    
    def get_cell_from_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convert screen position to board coordinates."""
        x, y = pos
        if (BOARD_OFFSET_X <= x <= BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE and 
            BOARD_OFFSET_Y <= y <= BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE):
            col = (x - BOARD_OFFSET_X) // CELL_SIZE
            row = (y - BOARD_OFFSET_Y) // CELL_SIZE
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return row, col
        return None
    
    def is_valid_move(self, r: int, c: int) -> bool:
        """Checks if a move is within the board and on an empty cell."""
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == EMPTY
    
    def draw_left_panel(self):
        """Draw the left panel with game information."""
        # Panel background
        panel_width = 200
        pygame.draw.rect(self.screen, LIGHT_BLUE, (0, 0, panel_width, WINDOW_SIZE))
        pygame.draw.rect(self.screen, BLACK, (0, 0, panel_width, WINDOW_SIZE), 2)
        
        # Title
        title_text = "GOMOKU"
        title_surface = self.large_font.render(title_text, True, BLACK)
        title_rect = title_surface.get_rect(center=(panel_width // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Game timer
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        timer_text = f"Game Time:"
        timer_label = self.font.render(timer_text, True, BLACK)
        self.screen.blit(timer_label, (20, 120))
        
        timer_value = f"{minutes:02d}:{seconds:02d}"
        timer_surface = self.large_font.render(timer_value, True, BLACK)
        timer_rect = timer_surface.get_rect(center=(panel_width // 2, 170))
        self.screen.blit(timer_surface, timer_rect)
        
        # Human move time
        if self.current_player == P1 and not self.game_over:
            human_time = time.time() - self.human_move_start
            human_text = f"Your Move:"
            human_label = self.font.render(human_text, True, BLACK)
            self.screen.blit(human_label, (20, 220))
            
            human_value = f"{human_time:.1f}s"
            human_surface = self.large_font.render(human_value, True, GREEN)
            human_rect = human_surface.get_rect(center=(panel_width // 2, 270))
            self.screen.blit(human_surface, human_rect)
        elif self.human_move_times:
            # Show last human move time
            last_human = self.human_move_times[-1]
            human_text = f"Last Human:"
            human_label = self.font.render(human_text, True, BLACK)
            self.screen.blit(human_label, (20, 220))
            
            human_value = f"{last_human:.1f}s"
            human_surface = self.large_font.render(human_value, True, GREEN)
            human_rect = human_surface.get_rect(center=(panel_width // 2, 270))
            self.screen.blit(human_surface, human_rect)
        
        # AI thinking time
        if self.is_ai_thinking:
            thinking_time = time.time() - self.ai_thinking_start
            thinking_text = f"AI Thinking:"
            thinking_label = self.font.render(thinking_text, True, BLACK)
            self.screen.blit(thinking_label, (20, 320))
            
            thinking_value = f"{thinking_time:.1f}s"
            thinking_surface = self.large_font.render(thinking_value, True, RED)
            thinking_rect = thinking_surface.get_rect(center=(panel_width // 2, 370))
            self.screen.blit(thinking_surface, thinking_rect)
        elif self.ai_move_times:
            # Show last AI move time
            last_ai = self.ai_move_times[-1]
            thinking_text = f"Last AI Move:"
            thinking_label = self.font.render(thinking_text, True, BLACK)
            self.screen.blit(thinking_label, (20, 320))
            
            thinking_value = f"{last_ai:.1f}s"
            thinking_surface = self.large_font.render(thinking_value, True, BLUE)
            thinking_rect = thinking_surface.get_rect(center=(panel_width // 2, 370))
            self.screen.blit(thinking_surface, thinking_rect)
        
        # Current player
        if not self.game_over:
            if self.current_player == P1:
                player_text = "Your Turn"
                player_color = BLACK
            else:
                player_text = "AI Turn"
                player_color = RED
        else:
            player_text = "Game Over"
            player_color = DARK_GRAY
            
        player_label = self.font.render("Current Player:", True, BLACK)
        self.screen.blit(player_label, (20, 420))
        
        player_surface = self.font.render(player_text, True, player_color)
        player_rect = player_surface.get_rect(center=(panel_width // 2, 460))
        self.screen.blit(player_surface, player_rect)
        
        # Move count
        move_count = sum(1 for row in self.board for cell in row if cell != EMPTY)
        move_text = f"Total Moves: {move_count}"
        move_surface = self.small_font.render(move_text, True, BLACK)
        self.screen.blit(move_surface, (20, 500))
        
        # Average times
        if self.human_move_times:
            avg_human = sum(self.human_move_times) / len(self.human_move_times)
            avg_human_text = f"Avg Human: {avg_human:.1f}s"
            avg_human_surface = self.small_font.render(avg_human_text, True, GREEN)
            self.screen.blit(avg_human_surface, (20, 520))
        
        if self.ai_move_times:
            avg_ai = sum(self.ai_move_times) / len(self.ai_move_times)
            avg_ai_text = f"Avg AI: {avg_ai:.1f}s"
            avg_ai_surface = self.small_font.render(avg_ai_text, True, BLUE)
            self.screen.blit(avg_ai_surface, (20, 540))
        
        # Game status
        if self.game_over:
            if self.winner == P1:
                status_text = "🎉 You Won!"
                status_color = GREEN
            elif self.winner == P2:
                status_text = "🤖 AI Won!"
                status_color = RED
            else:
                status_text = "It's a Draw!"
                status_color = BLUE
                
            status_surface = self.font.render(status_text, True, status_color)
            status_rect = status_surface.get_rect(center=(panel_width // 2, 580))
            self.screen.blit(status_surface, status_rect)
            
            restart_text = "Click to restart"
            restart_surface = self.small_font.render(restart_text, True, BLACK)
            restart_rect = restart_surface.get_rect(center=(panel_width // 2, 610))
            self.screen.blit(restart_surface, restart_rect)
    
    def draw_board(self):
        """Draw the game board."""
        # Draw board background
        pygame.draw.rect(self.screen, GRAY, 
                        (BOARD_OFFSET_X - 5, BOARD_OFFSET_Y - 5, 
                         BOARD_SIZE * CELL_SIZE + 10, BOARD_SIZE * CELL_SIZE + 10))
        
        # Draw grid lines
        for i in range(BOARD_SIZE + 1):
            # Vertical lines
            x = BOARD_OFFSET_X + i * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (x, BOARD_OFFSET_Y), 
                           (x, BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE))
            # Horizontal lines
            y = BOARD_OFFSET_Y + i * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (BOARD_OFFSET_X, y), 
                           (BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE, y))
        
        # Draw stones
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] != EMPTY:
                    x = BOARD_OFFSET_X + c * CELL_SIZE + CELL_SIZE // 2
                    y = BOARD_OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2
                    color = BLACK if self.board[r][c] == P1 else WHITE
                    pygame.draw.circle(self.screen, color, (x, y), CELL_SIZE // 2 - 2)
                    if self.board[r][c] == P2:  # AI stones get a border
                        pygame.draw.circle(self.screen, BLACK, (x, y), CELL_SIZE // 2 - 2, 2)
    
    def draw_popup(self):
        """Draw the winner popup message."""
        if not self.show_popup:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Popup background
        popup_width = 400
        popup_height = 200
        popup_x = (WINDOW_SIZE - popup_width) // 2
        popup_y = (WINDOW_SIZE - popup_height) // 2
        
        pygame.draw.rect(self.screen, WHITE, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 3)
        
        # Winner text
        if self.winner == P1:
            winner_text = "🎉 YOU WIN! 🎉"
            color = GREEN
        elif self.winner == P2:
            winner_text = "🤖 AI WINS! 🤖"
            color = RED
        else:
            winner_text = "It's a Draw!"
            color = BLUE
        
        winner_surface = self.large_font.render(winner_text, True, color)
        winner_rect = winner_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 30))
        self.screen.blit(winner_surface, winner_rect)
        
        # Restart message
        restart_text = "Click anywhere to restart"
        restart_surface = self.font.render(restart_text, True, BLACK)
        restart_rect = restart_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 30))
        self.screen.blit(restart_surface, restart_rect)
    
    def check_win(self, player: int) -> bool:
        """Checks if the given player has won."""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                # Check for 5 in a row in all four directions
                if c <= BOARD_SIZE - 5 and all(self.board[r][c+i] == player for i in range(5)):
                    return True
                if r <= BOARD_SIZE - 5 and all(self.board[r+i][c] == player for i in range(5)):
                    return True
                if r <= BOARD_SIZE - 5 and c <= BOARD_SIZE - 5 and all(self.board[r+i][c+i] == player for i in range(5)):
                    return True
                if r <= BOARD_SIZE - 5 and c >= 4 and all(self.board[r+i][c-i] == player for i in range(5)):
                    return True
        return False
    
    def check_draw(self) -> bool:
        """Check if the game is a draw (board is full)."""
        return all(self.board[r][c] != EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
    
    def handle_win_condition(self, player: int):
        """Handle win condition and show popup."""
        self.game_over = True
        self.winner = player
        self.show_popup = True
        self.popup_start_time = time.time()
        self.is_ai_thinking = False
        print(f"Game Over! {'You win!' if player == P1 else 'AI wins!'}")
    
    def evaluate_sequence(self, sequence, player: int) -> int:
        """Evaluates a single line (row, col, or diagonal) of 5 cells."""
        opponent = P1 if player == P2 else P2
        player_stones = sequence.count(player)
        empty_cells = sequence.count(EMPTY)
        opponent_stones = sequence.count(opponent)

        if player_stones == 5:
            return 100000  # Win
        if player_stones == 4 and empty_cells == 1:
            return 5000    # Open four
        if player_stones == 3 and empty_cells == 2:
            return 1000    # Open three
        if opponent_stones == 4 and empty_cells == 1:
            return -8000   # Opponent's open four (urgent block)
        if opponent_stones == 3 and empty_cells == 2:
            return -1500   # Opponent's open three
        return 0
    
    def evaluate_board(self) -> int:
        """Scores the entire board based on patterns."""
        score = 0
        # Evaluate rows, columns, and diagonals
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                # Horizontal
                if c <= BOARD_SIZE - 5:
                    sequence = [self.board[r][c+i] for i in range(5)]
                    score += self.evaluate_sequence(sequence, P2)
                    score -= self.evaluate_sequence(sequence, P1)
                # Vertical
                if r <= BOARD_SIZE - 5:
                    sequence = [self.board[r+i][c] for i in range(5)]
                    score += self.evaluate_sequence(sequence, P2)
                    score -= self.evaluate_sequence(sequence, P1)
                # Diagonal (top-left to bottom-right)
                if r <= BOARD_SIZE - 5 and c <= BOARD_SIZE - 5:
                    sequence = [self.board[r+i][c+i] for i in range(5)]
                    score += self.evaluate_sequence(sequence, P2)
                    score -= self.evaluate_sequence(sequence, P1)
                # Diagonal (top-right to bottom-left)
                if r <= BOARD_SIZE - 5 and c >= 4:
                    sequence = [self.board[r+i][c-i] for i in range(5)]
                    score += self.evaluate_sequence(sequence, P2)
                    score -= self.evaluate_sequence(sequence, P1)
        return score
    
    def get_candidate_moves(self):
        """Generates a list of potential moves to search (near existing stones)."""
        candidates = set()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] != EMPTY:
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if self.is_valid_move(nr, nc):
                                candidates.add((nr, nc))
        return list(candidates) if candidates else [(BOARD_SIZE//2, BOARD_SIZE//2)]
    
    def minimax_ab(self, board, depth: int, alpha: int, beta: int, is_maximizing: bool) -> int:
        """Minimax algorithm with Alpha-Beta Pruning."""
        if self.check_win(P2):
            return 100000
        if self.check_win(P1):
            return -100000
        if depth == 0:
            return self.evaluate_board()

        moves = self.get_candidate_moves()

        if is_maximizing:
            max_eval = -sys.maxsize
            for r, c in moves:
                board[r][c] = P2
                eval_score = self.minimax_ab(board, depth - 1, alpha, beta, False)
                board[r][c] = EMPTY
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = sys.maxsize
            for r, c in moves:
                board[r][c] = P1
                eval_score = self.minimax_ab(board, depth - 1, alpha, beta, True)
                board[r][c] = EMPTY
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
    
    def find_best_move(self, depth: int) -> Tuple[int, int]:
        """Finds the best move for the AI using the optimized algorithm."""
        best_score = -sys.maxsize
        best_move = (-1, -1)
        moves = self.get_candidate_moves()

        for r, c in moves:
            self.board[r][c] = P2
            score = self.minimax_ab(self.board, depth - 1, -sys.maxsize, sys.maxsize, False)
            self.board[r][c] = EMPTY
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move
    
    def make_ai_move(self):
        """AI makes a move."""
        self.is_ai_thinking = False
        start_time = time.time()
        ai_row, ai_col = self.find_best_move(2)  # Depth 2 for reasonable speed
        if ai_row != -1:
            self.board[ai_row][ai_col] = P2
            move_time = time.time() - start_time
            self.ai_move_times.append(move_time)
            self.move_times.append(move_time)
            print(f"🤖 AI played at ({ai_row}, {ai_col}) in {move_time:.2f}s")
        self.current_player = P1
        # Start timing human's next move
        self.human_move_start = time.time()
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_popup:
                        # Clicked on popup - restart game
                        self.reset_game()
                    elif not self.game_over and self.current_player == P1:  # Human's turn
                        pos = pygame.mouse.get_pos()
                        cell = self.get_cell_from_pos(pos)
                        if cell:
                            row, col = cell
                            if self.is_valid_move(row, col):
                                # Calculate human move time
                                human_move_time = time.time() - self.human_move_start
                                self.human_move_times.append(human_move_time)
                                print(f"👤 You played at ({row}, {col}) in {human_move_time:.2f}s")
                                
                                self.board[row][col] = P1
                                self.current_player = P2
                                
                                # Check for human win
                                if self.check_win(P1):
                                    self.handle_win_condition(P1)
                                    continue
                                
                                # Check for draw
                                if self.check_draw():
                                    self.game_over = True
                                    self.winner = None
                                    self.show_popup = True
                                    self.popup_start_time = time.time()
                                    print("It's a draw!")
                                    continue
                                
                                # Start AI thinking
                                self.is_ai_thinking = True
                                self.ai_thinking_start = time.time()
                                
                                # AI's turn
                                self.make_ai_move()
                                
                                # Check for AI win
                                if self.check_win(P2):
                                    self.handle_win_condition(P2)
                                    continue
                                
                                # Check for draw after AI move
                                if self.check_draw():
                                    self.game_over = True
                                    self.winner = None
                                    self.show_popup = True
                                    self.popup_start_time = time.time()
                                    print("It's a draw!")
            
            # Draw everything
            self.screen.fill(WHITE)
            self.draw_left_panel()
            self.draw_board()
            self.draw_popup()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

def main():
    game = GomokuGame()
    game.run()

if __name__ == "__main__":
    main()