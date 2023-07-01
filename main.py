import pygame
from checkers.constants import Colors, Constants
from checkers.game import Game

FPS = 60

WIDTH = 600
HEIGHT = 600
    
SQUARE_SIZE = 75

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
font = pygame.font.Font(None, 50)

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
