import pygame
from checkers.constants import Colors, Constants
from checkers.piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.brown_left = self.white_left = 12
        self.brown_kings = self.white_kings = 0
        self.create_board()

    def create_board(self):
        for row in range(Constants.ROWS):
            self.board.append([])
            for col in range(Constants.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, Colors.WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, Colors.SADDLEBROWN))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_squares(self, win):
        win.fill(Colors.BLACK)
        for row in range(Constants.ROWS):
            for col in range(row % 2, Constants.COLS, 2):
                pygame.draw.rect(win, Colors.SADDLEBROWN, (row*Constants.SQUARE_SIZE, col*Constants.SQUARE_SIZE, Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))

    def draw(self, win):
        self.draw_squares(win)
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
                    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == Constants.ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == Colors.WHITE:
                self.white_kings += 1
            else:
                self.brown_kings += 1 

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == Colors.SADDLEBROWN:
                    self.brown_left -= 1
                else:
                    self.white_left -= 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def winner(self):
        if self.brown_left <= 0:
            print("WHITE WIN")
            return Colors.WHITE
        elif self.white_left <= 0:
            print("BROWN WIN")
            return Colors.SADDLEBROWN
        
        return None 

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == Colors.SADDLEBROWN or piece.king:
            moves.update(self.traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self.traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == Colors.WHITE or piece.king:
            moves.update(self.traverse_left(row + 1, min(row + 3, Constants.ROWS), 1, piece.color, left))
            moves.update(self.traverse_right(row + 1, min(row + 3, Constants.ROWS), 1, piece.color, right))

        return moves

    def traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, Constants.ROWS)
                    moves.update(self.traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self.traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= Constants.COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, Constants.ROWS)
                    moves.update(self.traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self.traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
