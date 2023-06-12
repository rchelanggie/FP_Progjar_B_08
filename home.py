import pygame
import subprocess

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
WIDTH = 800
HEIGHT = 600

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Inisialisasi layar permainan
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

# Background
background = pygame.image.load("background.jpg")  # Ganti "background.jpg" dengan path file gambar latar belakang Anda
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Font
font = pygame.font.Font(None, 50)

p = subprocess.Popen("echo 'Game Started'", shell=True) 

# Fungsi untuk menggambar teks di tengah layar
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Fungsi untuk menggambar tombol
def draw_button(text, font, color, rect, action):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, color, rect, border_radius=5)

        if click[0] == 1:
            action()
            
    else:
        pygame.draw.rect(screen, color, rect)

    draw_text(text, font, WHITE, rect.centerx, rect.centery)

# Fungsi untuk tombol play
def play_game():
    # Di sini, Anda dapat memanggil fungsi untuk memulai permainan catur
    print("Game started")
    p = subprocess.Popen(["python", "main.py"])  # Ganti "main.py" dengan nama file dan path yang sesuai
    
def find_game():
    print("Find Room")
    
def friend_game():
    print("Option")

# Fungsi untuk tombol quit
def quit_game():
    pygame.quit()
    p.kill()
    quit()

# Loop utama permainan
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tampilan halaman utama
    screen.blit(background, (0, 0))
    # play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    # quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    
    play_button = pygame.Rect(WIDTH // 2 - 100 + 100 + 100, HEIGHT // 2 - 100, 200, 30)
    find_button = pygame.Rect(WIDTH // 2 - 100 + 100 + 100, HEIGHT // 2 - 50, 200, 30)
    friend_button = pygame.Rect(WIDTH // 2 - 100 + 100 + 100, HEIGHT // 2 + 50, 200, 30)
    quit_button = pygame.Rect(WIDTH // 2 - 100 + 100 + 100, HEIGHT // 2 + 100, 200, 30)


    draw_button("Play", font, BLACK, play_button, play_game)
    draw_button("Find Room", font, BLACK, find_button, find_game)
    draw_button("Find Friend", font, BLACK, friend_button, friend_game)
    draw_button("Quit", font, BLACK, quit_button, quit_game)

    # Update tampilan layar
    pygame.display.flip()

# Keluar dari Pygame
pygame.quit()
