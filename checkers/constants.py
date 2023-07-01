import pygame  

class Constants: 
    WIDTH, HEIGHT = 600, 600 
    ROWS, COLS = 8, 8 
    SQUARE_SIZE = WIDTH // COLS 

class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)
    SADDLEBROWN = (139,69,19)
    YELLOW = (255, 255, 0)


class Assets: 
    CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44, 25))

