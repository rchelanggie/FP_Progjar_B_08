import pygame

FPS = 60

WIDTH = 600
HEIGHT = 600
    
SQUARE_SIZE = 75

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
font = pygame.font.Font(None, 50)

#constants buat game
class Constants: 
    WIDTH, HEIGHT = 600, 600 
    ROWS, COLS = 8, 8 
    SQUARE_SIZE = WIDTH // COLS 

#colors buat game
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)
    SADDLEBROWN = (139,69,19)
    YELLOW = (255, 255, 0)

#asset crown yang diperlukan
class Assets: 
    CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

#piece didalam board
class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = Constants.SQUARE_SIZE * self.col + Constants.SQUARE_SIZE // 2
        self.y = Constants.SQUARE_SIZE * self.row + Constants.SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = Constants.SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, Colors.GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(Assets.CROWN, (self.x - Assets.CROWN.get_width() // 2, self.y - Assets.CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

#board untuk game
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
    

#logic game
class Game:
    def __init__(self, win):
        self.win = win
        self._init()
   
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = Colors.SADDLEBROWN
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, Colors.YELLOW, (col * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2, row * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == Colors.SADDLEBROWN:
            self.turn = Colors.WHITE
        else:
            self.turn = Colors.SADDLEBROWN


#fungsi main
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    WIN.blit(text_surface, text_rect)

def draw_button(text, font, color, rect, action):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(WIN, color, rect, border_radius=5)

        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(WIN, color, rect)

    draw_text(text, font, (255,255,255), rect.centerx, rect.centery)

def empty():
    pass

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

if __name__ == '__main__':
    main()