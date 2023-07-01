import pygame
from checkers.constants import Colors, Constants, Assets

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
