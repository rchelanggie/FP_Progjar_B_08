# Impor modul pygame yang digunakan untuk membuat permainan.
# Impor modul constants yang berisi definisi warna dan konstanta lain yang digunakan dalam permainan.
# Impor kelas Piece yang mendefinisikan objek permainan.
import pygame
from checkers.constants import Colors, Constants
from checkers.piece import Piece


# Membuat kelas Board yang merepresentasikan papan permainan.
# Di dalam metode __init__, inisialisasi atribut board sebagai sebuah list kosong, dan brown_left, white_left, brown_kings, white_kings sebagai variabel dengan nilai awal 12 dan 0.
# Panggil metode create_board untuk membuat papan permainan.
class Board:
    def __init__(self):
        self.board = []
        self.brown_left = self.white_left = 12
        self.brown_kings = self.white_kings = 0
        self.create_board()



# Metode create_board digunakan untuk membuat papan permainan.
# Dalam perulangan for, untuk setiap row dan col, dilakukan pengecekan kondisi untuk menentukan jenis bidak yang ditempatkan di setiap posisi pada papan.
# Jika col % 2 == ((row + 1) % 2), berarti posisi tersebut adalah kotak yang valid untuk bidak.
# Jika row < 3, maka bidak yang ditempatkan adalah bidak putih (WHITE) dan objek Piece dengan posisi dan warna yang sesuai ditambahkan ke self.board.
# Jika row > 4, maka bidak yang ditempatkan adalah bidak coklat (SADDLEBROWN) dan objek Piece dengan posisi dan warna yang sesuai ditambahkan ke self.board.
# Jika tidak, kotak tersebut tidak berisi bidak dan 0 ditambahkan ke self.board.
# Jika kondisi awal (col % 2 == ((row + 1) % 2)) tidak terpenuhi, maka kotak tersebut tidak berisi bidak dan 0 ditambahkan ke self.board.
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

# Metode draw_squares digunakan untuk menggambar kotak pada papan permainan.
# Metode ini mengisi layar dengan warna hitam (BLACK) menggunakan win.fill(BLACK).
# Dalam perulangan for, digambar kotak dengan warna coklat (SADDLEBROWN) pada posisi yang sesuai dengan row dan col menggunakan pygame.draw.rect.
    def draw_squares(self, win):
        win.fill(Colors.BLACK)
        for row in range(Constants.ROWS):
            for col in range(row % 2, Constants.COLS, 2):
                pygame.draw.rect(win, Colors.SADDLEBROWN, (row*Constants.SQUARE_SIZE, col*Constants.SQUARE_SIZE, Constants.SQUARE_SIZE, Constants.SQUARE_SIZE))


# Metode draw digunakan untuk menggambar seluruh papan permainan.
# Metode ini memanggil metode draw_squares untuk menggambar kotak pada papan.
# Dalam perulangan for, untuk setiap row dan col, digambar bidak (jika ada) menggunakan metode draw dari objek Piece.
    def draw(self, win):
        self.draw_squares(win)
        for row in range(Constants.ROWS):
            for col in range(Constants.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

# Metode move digunakan untuk memindahkan bidak ke posisi yang baru.
# Metode ini menukar posisi bidak di self.board dengan menggunakan assignment unpacking.
# Memanggil metode move pada objek piece untuk memperbarui posisinya.
# Jika bidak mencapai ujung lawan (row == ROWS - 1 untuk bidak putih atau row == 0 untuk bidak coklat), maka bidak tersebut diubah menjadi raja menggunakan metode make_king.Jika bidak putih menjadi raja, atribut white_kings ditambah 1. Jika bidak coklat menjadi raja, atribut brown_kings ditambah 1. python

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == Constants.ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == Colors.WHITE:
                self.white_kings += 1
            else:
                self.brown_kings += 1 

# Metode remove digunakan untuk menghapus bidak dari papan permainan.
# Metode ini mengubah nilai pada posisi bidak di self.board menjadi 0.
# Jika bidak yang dihapus bukan 0 (yaitu bidak valid), maka jumlah bidak yang tersisa (brown_left atau white_left) dikurangi 1, tergantung pada warna bidak yang dihapus.
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == Colors.SADDLEBROWN:
                    self.brown_left -= 1
                else:
                    self.white_left -= 1

# Metode get_piece digunakan untuk mendapatkan bidak pada posisi yang ditentukan oleh row dan col dari papan permainan.
    def get_piece(self, row, col):
        return self.board[row][col]


# Metode winner digunakan untuk menentukan pemenang permainan.
# Jika tidak ada bidak coklat yang tersisa (brown_left <= 0), maka putih (WHITE) menang.
# Jika tidak ada bidak putih yang tersisa (white_left <= 0), maka coklat (SADDLEBROWN) menang.
# Jika belum ada pemenang, mengembalikan None.
    def winner(self):
        if self.brown_left <= 0:
            print("WHITE WIN")
            return Colors.WHITE
        elif self.white_left <= 0:
            print("BROWN WIN")
            return Colors.SADDLEBROWN
        
        return None 


# Metode get_valid_moves digunakan untuk mendapatkan langkah-langkah yang valid untuk suatu bidak.
# Metode ini mengembalikan kamus moves yang berisi langkah-langkah yang valid.
# Dalam metode ini, langkah-langkah valid ditentukan dengan memanggil metode traverse_left dan traverse_right untuk mengeksplorasi kemungkinan langkah ke kiri dan ke kanan dari posisi bidak.
# Bergantung pada warna bidak atau apakah bidak adalah raja, langkah-langkah valid ditambahkan ke kamus moves.
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


# Metode traverse_left digunakan untuk mengeksplorasi langkah-langkah ke kiri dari posisi bidak.
# Metode ini mengembalikan kamus moves yang berisi langkah-langkah yang valid.
# Metode ini menggunakan rekursi untuk mencari langkah-langkah valid.
# Metode ini menerima beberapa parameter, termasuk start (baris awal), stop (baris akhir), step (langkah per baris), color (warna bidak), left (kolom kiri yang sedang diperiksa), dan skipped (bidak yang dilewati sebelumnya).
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


# Metode traverse_right mirip dengan metode traverse_left, tetapi digunakan untuk mengeksplorasi langkah-langkah ke kanan dari posisi bidak.
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
