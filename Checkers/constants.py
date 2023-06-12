import pygame  # Mengimpor modul pygame, yang digunakan untuk mengakses fungsi dan fitur pygame.

class Constants: # Mendefinisikan kelas Constants yang menyimpan beberapa konstanta terkait permainan.
    WIDTH, HEIGHT = 800, 800 # Mendefinisikan ukuran lebar dan tinggi layar permainan.
    ROWS, COLS = 8, 8 # Mendefinisikan jumlah baris dan kolom pada papan permainan.
    SQUARE_SIZE = WIDTH // COLS # Mendefinisikan ukuran persegi pada papan. Nilainya dihitung dengan membagi lebar layar dengan jumlah kolom.

class Colors: # Mendefinisikan kelas Colors yang menyimpan beberapa konstanta warna yang digunakan dalam permainan.
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)
    SADDLEBROWN = (139,69,19)
    YELLOW = (255, 255, 0)


class Assets: # Mendefinisikan kelas Assets yang menyimpan aset-aset grafis yang digunakan dalam permainan.
    
    # Memuat gambar mahkota dari file "checkers/assets/crown.png" menggunakan fungsi pygame.image.load(), 
    # dan kemudian mengubah ukurannya menjadi (44, 25) menggunakan fungsi pygame.transform.scale(). 
    # Gambar mahkota ini akan digunakan untuk menandai bidak yang telah menjadi "king" dalam permainan.
    CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44, 25))

#Kode ini menyediakan nilai-nilai yang dibutuhkan dalam permainan "Checkers", seperti ukuran layar, warna, dan aset grafis.