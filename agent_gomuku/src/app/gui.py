import pygame
import sys
import time
from typing import Optional, Tuple
from ..core.game_board import GameBoard, Stone
from ..core.ai_engine import AIEngine

class GomokuGUI:
    """Graphical user interface for the Gomoku game."""
    
    def __init__(self, width: int = 1200, height: int = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Gomoku - AI vs Human")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.BROWN = (139, 69, 19)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        
        # Game state
        self.board = GameBoard()
        self.ai_engine = AIEngine(max_depth=10, time_limit=0.5)
        self.game_mode = "ai_vs_human"  # "ai_vs_human" or "human_vs_human"
        self.ai_thinking = False
        self.ai_move_start_time = 0
        self.ai_thinking_time = 0
        self.suggested_move = None
        self.show_suggestion = False
        
        # Board display
        self.board_size = 19
        self.cell_size = min((height - 200) // self.board_size, (width - 400) // self.board_size)
        self.board_offset_x = (width - self.board_size * self.cell_size) // 2
        self.board_offset_y = (height - self.board_size * self.cell_size) // 2
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game state
        self.game_over = False
        self.winner = None
        
    def run(self):
        """Main game loop."""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)
            
            # AI move if it's AI's turn
            if (self.game_mode == "ai_vs_human" and 
                self.board.get_current_player() == Stone.WHITE and 
                not self.ai_thinking and 
                not self.game_over):
                self.make_ai_move()
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def handle_mouse_click(self, pos: Tuple[int, int]):
        """Handle mouse click events."""
        if self.game_over:
            return
        
        # Check if click is on the board
        board_x = (pos[0] - self.board_offset_x) // self.cell_size
        board_y = (pos[1] - self.board_offset_y) // self.cell_size
        
        if (0 <= board_x < self.board_size and 
            0 <= board_y < self.board_size and
            self.board.is_valid_move(board_y, board_x)):
            
            if self.game_mode == "ai_vs_human" and self.board.get_current_player() == Stone.BLACK:
                # Human player's turn
                self.board.make_move(board_y, board_x)
                self.check_game_end()
                
            elif self.game_mode == "human_vs_human":
                # Human vs Human mode
                self.board.make_move(board_y, board_x)
                self.check_game_end()
    
    def handle_key_press(self, key):
        """Handle keyboard events."""
        if key == pygame.K_r:
            self.reset_game()
        elif key == pygame.K_m:
            self.toggle_game_mode()
        elif key == pygame.K_s and self.game_mode == "human_vs_human":
            self.show_move_suggestion()
        elif key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    
    def make_ai_move(self):
        """Make AI move with timing."""
        self.ai_thinking = True
        self.ai_move_start_time = time.time()
        
        # Get AI move
        ai_move = self.ai_engine.get_best_move(self.board, Stone.WHITE)
        
        if ai_move:
            self.board.make_move(ai_move[0], ai_move[1])
            self.check_game_end()
        
        self.ai_thinking_time = time.time() - self.ai_move_start_time
        self.ai_thinking = False
    
    def show_move_suggestion(self):
        """Show move suggestion for human vs human mode."""
        if self.board.get_current_player() == Stone.BLACK:
            suggested_move = self.ai_engine.get_best_move(self.board, Stone.BLACK)
            if suggested_move:
                self.suggested_move = suggested_move
                self.show_suggestion = True
    
    def check_game_end(self):
        """Check if the game has ended."""
        if self.board.is_game_over():
            self.game_over = True
            self.winner = self.board.get_winner()
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board.reset()
        self.game_over = False
        self.winner = None
        self.ai_thinking = False
        self.ai_thinking_time = 0
        self.suggested_move = None
        self.show_suggestion = False
    
    def toggle_game_mode(self):
        """Toggle between AI vs Human and Human vs Human modes."""
        if self.game_mode == "ai_vs_human":
            self.game_mode = "human_vs_human"
        else:
            self.game_mode = "ai_vs_human"
        self.reset_game()
    
    def draw(self):
        """Draw the game interface."""
        self.screen.fill(self.BROWN)
        
        # Draw board
        self.draw_board()
        
        # Draw UI elements
        self.draw_ui()
        
        # Draw game info
        self.draw_game_info()
        
        # Draw suggested move
        if self.show_suggestion and self.suggested_move:
            self.draw_suggested_move()
        
        pygame.display.flip()
    
    def draw_board(self):
        """Draw the game board."""
        # Draw board background
        board_rect = pygame.Rect(
            self.board_offset_x - 10,
            self.board_offset_y - 10,
            self.board_size * self.cell_size + 20,
            self.board_size * self.cell_size + 20
        )
        pygame.draw.rect(self.screen, self.BLACK, board_rect)
        
        # Draw grid lines
        for i in range(self.board_size):
            # Vertical lines
            x = self.board_offset_x + i * self.cell_size
            pygame.draw.line(self.screen, self.GRAY, 
                           (x, self.board_offset_y), 
                           (x, self.board_offset_y + self.board_size * self.cell_size))
            
            # Horizontal lines
            y = self.board_offset_y + i * self.cell_size
            pygame.draw.line(self.screen, self.GRAY, 
                           (self.board_offset_x, y), 
                           (self.board_offset_x + self.board_size * self.cell_size, y))
        
        # Draw stones
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board.board[row, col] != Stone.EMPTY.value:
                    x = self.board_offset_x + col * self.cell_size
                    y = self.board_offset_y + row * self.cell_size
                    color = self.BLACK if self.board.board[row, col] == Stone.BLACK.value else self.WHITE
                    
                    # Draw stone
                    pygame.draw.circle(self.screen, color, (x, y), self.cell_size // 2 - 2)
                    
                    # Draw highlight for last move
                    if (row, col) == self.board.last_move:
                        pygame.draw.circle(self.screen, self.RED, (x, y), self.cell_size // 2 - 2, 3)
    
    def draw_ui(self):
        """Draw UI elements."""
        # Game mode button
        mode_text = "AI vs Human" if self.game_mode == "ai_vs_human" else "Human vs Human"
        mode_surface = self.font_medium.render(mode_text, True, self.WHITE)
        self.screen.blit(mode_surface, (20, 20))
        
        # Instructions
        instructions = [
            "R: Reset Game",
            "M: Toggle Mode",
            "S: Show Suggestion (Human vs Human)",
            "ESC: Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.font_small.render(instruction, True, self.WHITE)
            self.screen.blit(text_surface, (20, 60 + i * 25))
    
    def draw_game_info(self):
        """Draw game information."""
        # Current player
        current_player = "Black" if self.board.get_current_player() == Stone.BLACK else "White"
        player_text = f"Current Player: {current_player}"
        player_surface = self.font_medium.render(player_text, True, self.WHITE)
        self.screen.blit(player_surface, (self.width - 300, 20))
        
        # Captures
        black_captures = self.board.get_captures(Stone.BLACK)
        white_captures = self.board.get_captures(Stone.WHITE)
        captures_text = f"Captures - Black: {black_captures}, White: {white_captures}"
        captures_surface = self.font_small.render(captures_text, True, self.WHITE)
        self.screen.blit(captures_surface, (self.width - 300, 60))
        
        # AI thinking time
        if self.game_mode == "ai_vs_human":
            if self.ai_thinking:
                thinking_text = "AI Thinking..."
                thinking_surface = self.font_medium.render(thinking_text, True, self.RED)
                self.screen.blit(thinking_surface, (self.width - 300, 100))
            else:
                time_text = f"AI Move Time: {self.ai_thinking_time:.3f}s"
                time_surface = self.font_small.render(time_text, True, self.WHITE)
                self.screen.blit(time_surface, (self.width - 300, 100))
        
        # Game over message
        if self.game_over:
            if self.winner:
                winner_text = f"{'Black' if self.winner == Stone.BLACK else 'White'} Wins!"
                winner_surface = self.font_large.render(winner_text, True, self.GREEN)
                text_rect = winner_surface.get_rect(center=(self.width // 2, 50))
                self.screen.blit(winner_surface, text_rect)
            else:
                draw_text = "Game is a Draw!"
                draw_surface = self.font_large.render(draw_text, True, self.GRAY)
                text_rect = draw_surface.get_rect(center=(self.width // 2, 50))
                self.screen.blit(draw_surface, text_rect)
    
    def draw_suggested_move(self):
        """Draw the suggested move."""
        if self.suggested_move:
            row, col = self.suggested_move
            x = self.board_offset_x + col * self.cell_size
            y = self.board_offset_y + row * self.cell_size
            
            # Draw suggestion indicator
            pygame.draw.circle(self.screen, self.GREEN, (x, y), self.cell_size // 2, 3)
            
            # Draw suggestion text
            suggestion_text = "Suggested Move"
            suggestion_surface = self.font_small.render(suggestion_text, True, self.GREEN)
            self.screen.blit(suggestion_surface, (self.width - 300, 140))

