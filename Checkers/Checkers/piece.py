# Baris ini mengimpor modul pygame dan beberapa konstanta (Colors dan Constants) dari modul lain.
import pygame
from checkers.constants import Colors, Constants, Assets

# Kelas Piece merepresentasikan sebuah bidak dalam permainan.
# Atribut PADDING dan OUTLINE adalah konstanta yang digunakan untuk mengatur tampilan grafis bidak.
class Piece:
    PADDING = 15
    OUTLINE = 2


# Konstruktor __init__ digunakan untuk menginisialisasi atribut-atribut bidak.
# Atribut row dan col menyimpan posisi baris dan kolom bidak pada papan.
# Atribut color menyimpan warna bidak.
# Atribut king menyatakan apakah bidak sudah menjadi raja atau tidak.
# Atribut x dan y menyimpan koordinat piksel bidak pada layar.
# Metode calc_pos dipanggil untuk menghitung dan mengatur koordinat piksel bidak berdasarkan posisi baris dan kolom.
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

# Metode calc_pos menghitung dan mengatur koordinat piksel bidak berdasarkan posisi baris dan kolom pada papan.
# Atribut x dihitung sebagai posisi tengah kolom piksel bidak.
# Atribut y dihitung sebagai posisi tengah baris piksel bidak.
    def calc_pos(self):
        self.x = Constants.SQUARE_SIZE * self.col + Constants.SQUARE_SIZE // 2
        self.y = Constants.SQUARE_SIZE * self.row + Constants.SQUARE_SIZE // 2


# Metode make_king mengubah bidak menjadi raja dengan mengatur atribut king menjadi True.
    def make_king(self):
        self.king = True


# Metode draw digunakan untuk menggambar bidak pada layar.
# Sebuah lingkaran luar dengan warna abu-abu (GREY) digambar dengan menggunakan metode pygame.draw.circle.
# Lingkaran dalam dengan warna sesuai warna bidak (self.color) juga digambar.
# Jika bidak adalah raja, sebuah mahkota (gambar CROWN) ditampilkan pada posisi tengah bidak.
    def draw(self, win):
        radius = Constants.SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, Colors.GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(Assets.CROWN, (self.x - Assets.CROWN.get_width() // 2, self.y - Assets.CROWN.get_height() // 2))

# Metode move digunakan untuk memindahkan bidak ke posisi baris dan kolom yang baru pada papan
# Atribut row dan col diperbarui dengan nilai yang baru.
# Metode calc_pos dipanggil untuk menghitung dan mengatur ulang koordinat piksel bidak.
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()


# Metode __repr__ digunakan untuk menghasilkan representasi string dari objek bidak.
# Pada kasus ini, metode mengembalikan string yang merepresentasikan warna bidak.
    def __repr__(self):
        return str(self.color)
