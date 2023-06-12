# Baris ini mengimpor modul pygame, konstanta (Colors dan Constants) dari modul constants, dan kelas Game dari modul game.
import pygame
from checkers.constants import Colors, Constants
from checkers.game import Game


# Variabel FPS menentukan jumlah frame per detik dalam permainan.
# Variabel WIDTH dan HEIGHT menentukan lebar dan tinggi layar permainan.
# Variabel WIN merupakan objek layar permainan yang diinisialisasi dengan ukuran yang ditentukan menggunakan pygame.display.set_mode.
# Metode pygame.display.set_caption digunakan untuk mengatur judul jendela permainan.
FPS = 60

WIDTH = 800
HEIGHT = 800

SQUARE_SIZE = 100

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
font = pygame.font.Font(None, 50)

# Fungsi get_row_col_from_mouse digunakan untuk mendapatkan posisi baris dan kolom dari koordinat piksel pada layar yang diperoleh dari input mouse.
# Fungsi ini menghitung nilai row dan col dengan membagi koordinat x dan y dengan ukuran kotak (SQUARE_SIZE).
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Fungsi untuk menggambar teks di tengah layar
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    WIN.blit(text_surface, text_rect)

# Fungsi untuk menggambar tombol
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

# Fungsi main merupakan titik masuk utama program.
# Variabel run diatur sebagai True untuk menjalankan permainan.
# Objek clock dibuat menggunakan pygame.time.Clock untuk mengontrol kecepatan frame dalam permainan.
# Objek game dibuat sebagai objek dari kelas Game yang ditentukan sebelumnya, dengan menggunakan objek layar WIN sebagai argumennya.
# Perulangan while digunakan untuk menjalankan permainan.
# Metode clock.tick digunakan untuk mengatur kecepatan frame per detik.
# Jika permainan telah memiliki pemenang, maka perulangan dihentikan dengan mengubah nilai run menjadi False.
# Perulangan for digunakan untuk menghandle event-event yang terjadi dalam permainan.
# Jika event QUIT terjadi (jendela ditutup), maka perulangan dihentikan dengan mengubah nilai run menjadi False.
# Jika event MOUSEBUTTONDOWN terjadi (tombol mouse ditekan), maka posisi mouse diambil, dan baris dan kolom diperoleh menggunakan fungsi get_row_col_from_mouse. Metode game.select dipanggil dengan argumen baris dan kolom tersebut.
# Metode game.update dipanggil untuk mengupdate tampilan permainan.
# Setelah perulangan berakhir, pemanggilan pygame.quit() dilakukan untuk keluar dari permainan.


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

# Blok ini memastikan bahwa fungsi main akan dieksekusi hanya ketika file ini dijalankan secara langsung, bukan ketika diimpor sebagai modul.
if __name__ == '__main__':
    main()
