# Gomoku Makefile
# Implements all required rules: $(NAME), all, clean, fclean, re

NAME = Gomoku
PYTHON = python3
PIP = pip3

# Directories
SRC_DIR = src
CORE_DIR = $(SRC_DIR)/core
APP_DIR = $(SRC_DIR)/app

# Python files
MAIN_FILE = $(APP_DIR)/main.py
REQUIREMENTS = requirements.txt

# Default target
all: $(NAME)

# Main target - installs dependencies and creates executable
$(NAME): install_deps
	@echo "Building $(NAME)..."
	@chmod +x $(MAIN_FILE)
	@echo "Build complete! Run with: $(PYTHON) $(MAIN_FILE)"

# Install Python dependencies
install_deps:
	@echo "Installing dependencies..."
	@$(PIP) install -r $(REQUIREMENTS)

# Clean Python cache files
clean:
	@echo "Cleaning Python cache files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Full clean - removes all generated files
fclean: clean
	@echo "Full clean complete"

# Rebuild - clean and rebuild
re: fclean all

# Run the game
run: $(NAME)
	@echo "Starting $(NAME)..."
	@$(PYTHON) $(MAIN_FILE)

# Install dependencies only
deps: install_deps

# Show help
help:
	@echo "Available targets:"
	@echo "  all        - Build the project (default)"
	@echo "  $(NAME)    - Build the project"
	@echo "  clean      - Remove Python cache files"
	@echo "  fclean     - Full clean"
	@echo "  re         - Rebuild (clean + build)"
	@echo "  run        - Build and run the game"
	@echo "  deps       - Install dependencies only"
	@echo "  help       - Show this help message"

.PHONY: all $(NAME) install_deps clean fclean re run deps help

