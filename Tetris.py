import pygame
import random


pygame.init()

# Rozmiar okna
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]


SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]


class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {"shape": shape, "color": color, "x": 3, "y": 0}

    def rotate_piece(self):
        self.current_piece["shape"] = list(zip(*self.current_piece["shape"][::-1]))

    def can_move(self, dx, dy):
        shape = self.current_piece["shape"]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.current_piece["x"] + x + dx
                    ny = self.current_piece["y"] + y + dy
                    if nx < 0 or nx >= 10 or ny >= 20 or (ny >= 0 and self.grid[ny][nx]):
                        return False
        return True

    def place_piece(self):
        shape = self.current_piece["shape"]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece["y"] + y][self.current_piece["x"] + x] = self.current_piece["color"]
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.can_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = len(self.grid) - len(new_grid)
        self.score += lines_cleared ** 2 * 100
        self.grid = [[0 for _ in range(10)] for _ in range(lines_cleared)] + new_grid

    def move(self, dx, dy):
        if self.can_move(dx, dy):
            self.current_piece["x"] += dx
            self.current_piece["y"] += dy
        elif dy > 0:
            self.place_piece()


def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(screen, piece):
    shape = piece["shape"]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece["color"], 
                                 ((piece["x"] + x) * BLOCK_SIZE, (piece["y"] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, 
                                 ((piece["x"] + x) * BLOCK_SIZE, (piece["y"] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris by Dominik")
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0

    running = True
    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick(60)

        if fall_time > 500:  
            if not game.can_move(0, 1):
                game.place_piece()
            else:
                game.move(0, 1)
            fall_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.can_move(-1, 0):
                    game.move(-1, 0)
                if event.key == pygame.K_RIGHT and game.can_move(1, 0):
                    game.move(1, 0)
                if event.key == pygame.K_DOWN:
                    game.move(0, 1)
                if event.key == pygame.K_UP:
                    game.rotate_piece()

        draw_grid(screen, game.grid)
        draw_piece(screen, game.current_piece)

        if game.game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, WHITE)
            screen.blit(text, (30, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
