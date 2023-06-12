# Baris ini mengimpor modul pygame dan beberapa konstanta (Colors dan Constants) serta kelas Board dari modul lain.
import pygame
from checkers.constants import Colors, Constants
from checkers.board import Board

# Kelas Game memiliki konstruktor __init__ yang menginisialisasi objek permainan.
# Objek win (window) dilewatkan sebagai argumen dan disimpan dalam atribut self.win.
# Metode _init dipanggil untuk menginisialisasi permainan.
class Game:
    def __init__(self, win):
        self.win = win
        self._init()
        self.score_brown = 0
        self.score_white = 0
    
    def draw_text(self):
        font = pygame.font.Font(None, 50)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self.win.blit(text_surface, text_rect)
    
    def update_score(self):
        self.text = f"Brown: {self.score_brown} - White: {self.score_white}"
    
    def update(self):
        self.win.fill(Colors.WHITE)
        self.board.draw(self.win)
        self.update_score()  # Tambahkan pemanggilan fungsi update_score di sini
        self.draw_text()
        pygame.display.update()

# Metode update menggambar papan permainan dan langkah-langkah yang valid pada layar.
# Metode draw_valid_moves dipanggil untuk menggambar lingkaran kecil pada langkah-langkah yang valid.
# Setelah itu, metode pygame.display.update() dipanggil untuk memperbarui tampilan layar.
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()


# Metode _init menginisialisasi beberapa atribut permainan.
# Atribut self.selected digunakan untuk menyimpan bidak yang dipilih oleh pemain.
# Atribut self.board adalah objek Board yang merepresentasikan papan permainan.
# Atribut self.turn menyimpan warna giliran saat ini.
# Atribut self.valid_moves adalah kamus yang menyimpan langkah-langkah yang valid untuk bidak yang dipilih.
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = Colors.SADDLEBROWN
        self.valid_moves = {}

# Metode winner mengembalikan pemenang permainan dengan memanggil metode winner dari objek Board.
    def winner(self):
        return self.board.winner()

# Metode reset menginisialisasi ulang permainan dengan memanggil metode _init.
    def reset(self):
        self._init()


# Metode select digunakan untuk memilih bidak pada posisi (row, col) yang diberikan.
# Jika sudah ada bidak yang dipilih sebelumnya, metode _move dipanggil untuk mencoba memindahkan bidak tersebut ke posisi yang dipilih.
# Jika langkah tidak valid, bidak yang dipilih diatur kembali menjadi None, dan metode select dipanggil kembali dengan posisi yang baru.
# Jika bidak yang dipilih memiliki warna yang sesuai dengan giliran saat ini, bidak tersebut diatur sebagai bidak yang dipilih, dan langkah-langkah yang valid untuk bidak tersebut diperoleh dari objek Board dan disimpan dalam atribut self.valid_moves.
# Jika pemilihan bidak berhasil, metode mengembalikan True, jika tidak, mengembalikan False.
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


# Metode _move digunakan untuk memindahkan bidak yang dipilih ke posisi (row, col) yang diberikan.
# Pertama, bidak pada posisi (row, col) diambil dari objek Board.
# Jika ada bidak yang dipilih dan posisi yang dipilih kosong, dan posisi yang dipilih ada dalam langkah-langkah yang valid, bidak dipindahkan ke posisi yang baru menggunakan metode move pada objek Board.
# Jika ada bidak yang dilewati selama pemindahan, bidak-bidak tersebut dihapus dari papan menggunakan metode remove pada objek Board.
# Gantian pemain diubah menggunakan metode change_turn.
# Jika langkah tidak valid, metode mengembalikan False, jika langkah berhasil dilakukan, mengembalikan True.
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

# Metode draw_valid_moves menggambar lingkaran kecil pada setiap langkah yang valid.
# Lingkaran digambar menggunakan metode pygame.draw.circle dengan warna kuning (YELLOW) dan koordinat yang sesuai dengan posisi langkah yang valid.
# Lingkaran kuning adalah petunjuk gerakan sah dari bidak
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, Colors.YELLOW, (col * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2, row * Constants.SQUARE_SIZE + Constants.SQUARE_SIZE // 2), 15)


# Metode change_turn mengganti giliran pemain.
# Atribut self.valid_moves dikosongkan, karena langkah-langkah yang valid hanya berlaku untuk giliran pemain sebelumnya.
# Jika giliran saat ini adalah coklat (SADDLEBROWN), giliran berikutnya adalah putih (WHITE), dan sebaliknya.
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == Colors.SADDLEBROWN:
            self.turn = Colors.WHITE
        else:
            self.turn = Colors.SADDLEBROWN
