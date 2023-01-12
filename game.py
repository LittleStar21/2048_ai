import pygame
import random
from constants import *

pygame.init()

class Game:
    def __init__(self):
        self.size = 4

        # Fonts
        self.small_font = pygame.font.SysFont("arial", FONT_SIZE_SMALL)
        self.medium_font = pygame.font.SysFont("arial", FONT_SIZE_MEDIUM)
        self.large_font = pygame.font.SysFont("arial", FONT_SIZE_LARGE)

        # Window
        win_width = self.size * TILE_SIZE + (self.size + 1) * PADDING
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((win_width, win_width))
        pygame.display.set_caption("2048 AI")

        self.reset()

    def reset(self):
        self.is_lose = False
        self.score = 0
        self.board = []
        for i in range(self.size):
            self.board.append([0] * self.size)

        self.generate_rand()
        self.print_board()

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        print("Move up")
                        self.board, changed = self.move_up()
                    elif event.key == pygame.K_DOWN:
                        print("Move down")
                        self.board, changed = self.move_down()
                    elif event.key == pygame.K_LEFT:
                        print("Move left")
                        self.board, changed = self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        print("Move right")
                        self.board, changed = self.move_right()
                    self.generate_rand()

            self.draw()
            self.clock.tick(FPS)

    def move_left(self, board=None):
        if board is None:
            board = self.copy_board()
        board, changed1 = self.compress(board)
        board, changed2 = self.merge(board)
        board, _ = self.compress(board)
        return board, changed1 or changed2


    def move_up(self):
        board = self.copy_board()
        board = self.transpose(board)
        board, changed = self.move_left(board)
        board = self.transpose(board)
        return board, changed

    def move_right(self, board=None):
        if board is None:
            board = self.copy_board()
        board = self.reverse(board)
        board, changed = self.move_left(board)
        board = self.reverse(board)
        return board, changed

    def move_down(self):
        board = self.copy_board()
        board = self.transpose(board)
        board, changed = self.move_right(board)
        board = self.transpose(board)
        return board, changed

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)

        for i in range(self.size):
            for j in range(self.size):
                background_rect = pygame.Rect(
                    (j + 1) * PADDING + j * TILE_SIZE,
                    (i + 1) * PADDING + i * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                tile_center = (
                    (j + 1) * PADDING + (j + 0.5) * TILE_SIZE,
                    (i + 1) * PADDING + (i + 0.5) * TILE_SIZE
                )

                # Tile background
                if self.board[i][j] <= 2048:
                    pygame.draw.rect(self.window, TILE_COLOR[self.board[i][j]], background_rect)
                else:
                    pygame.draw.rect(self.window, TILE_COLOR_OTHER, background_rect)

                # Tile text
                if self.board[i][j] > 0:
                    font_color = FONT_COLOR_LIGHT if self.board[i][j] >= 8 else FONT_COLOR_DARK
                    
                    if self.board[i][j] <= 64:
                        num_text = self.large_font.render(str(self.board[i][j]), True, font_color)
                    elif self.board[i][j] <= 512:
                        num_text = self.medium_font.render(str(self.board[i][j]), True, font_color)
                    else:
                        num_text = self.small_font.render(str(self.board[i][j]), True, font_color)
                    
                    self.window.blit(num_text, num_text.get_rect(center=tile_center))
                
        pygame.display.update()

    def generate_rand(self):
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            randomizer = random.randint(0, 9)
            if randomizer == 0:
                self.board[row][col] = 4
            else:
                self.board[row][col] = 2

    def check_lose(self):
        pass

    def copy_board(self):
        new_board = []
        for i in range(self.size):
            new_board.append([])
            for j in range(self.size):
                new_board[i].append(self.board[i][j])
        return new_board

    def compress(self, board):
        changed = False
        new_board = []
        for i in range(self.size):
            new_board.append([0] * 4)

        for i in range(self.size):
            pos = 0
            for j in range(self.size):
                if board[i][j] != 0:
                    new_board[i][pos] = board[i][j]
                    changed = j != pos
                    pos += 1
        return new_board, changed

    def merge(self, board):
        changed = False
        for i in range(self.size):
            for j in range(self.size - 1):
                if board[i][j] != 0 and board[i][j] == board[i][j + 1]:
                    board[i][j] *= 2
                    board[i][j + 1] = 0
                    changed = True
        return board, changed

    def transpose(self, board):
        new_board = []
        for i in range(self.size):
            new_board.append([])
            for j in range(self.size):
                new_board[i].append(board[j][i])
        return new_board

    def reverse(self, board):
        new_board = []
        for i in range(self.size):
            new_board.append([])
            for j in range(self.size):
                new_board[i].append(board[i][self.size - j - 1])
        return new_board

    def print_board(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j], end=" ")
            print()

if __name__ == "__main__":
    game = Game()
    game.play()