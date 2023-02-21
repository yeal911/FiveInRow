import threading
from tkinter import Canvas
from tkinter import ttk

from FiveInRow.Piece import Piece
from FiveInRow.Player import Player

from pydub import AudioSegment
from pydub.playback import play
import os


class CheckerBoard:
    def __init__(self, canvas: Canvas, p1: Player, p2: Player):
        self.canvas = canvas
        self.check_array = [[""] * 15 for i in range(15)]
        self.place_turn = "White"
        self.started = True
        self.player1 = p1
        self.player2 = p2
        self.winner_text = None
        self.turn_text = None
        self.gap = 100
        self.color = "#696969"
        self.song = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/Resource/place.wav"
        self.canvas.bind("<Button-1>", self.place_piece)

    def draw(self):
        for i in range(1, 16):
            # draw rows
            self.canvas.create_line(self.gap, self.gap * i, 15 * self.gap, self.gap * i, fill=self.color, width=4)
            # draw cols
            self.canvas.create_line(self.gap * i, self.gap, self.gap * i, 15 * self.gap, fill=self.color, width=4)
        # draw 5 dots
        self.canvas.create_rectangle(self.gap * 4 - 10, self.gap * 4 - 10, self.gap * 4 + 10, self.gap * 4 + 10, fill=self.color)
        self.canvas.create_rectangle(self.gap * 12 - 10, self.gap * 4 - 10, self.gap * 12 + 10, self.gap * 4 + 10, fill=self.color)
        self.canvas.create_rectangle(self.gap * 8 - 10, self.gap * 8 - 10, self.gap * 8 + 10, self.gap * 8 + 10, fill=self.color)
        self.canvas.create_rectangle(self.gap * 4 - 10, self.gap * 12 - 10, self.gap * 4 + 10, self.gap * 12 + 10, fill=self.color)
        self.canvas.create_rectangle(self.gap * 4 - 10, self.gap * 12 - 10, self.gap * 4 + 10, self.gap * 12 + 10, fill=self.color)
        self.canvas.create_rectangle(self.gap * 12 - 10, self.gap * 12 - 10, self.gap * 12 + 10, self.gap * 12 + 10, fill=self.color)
        self.canvas.create_rectangle(self.gap * 16, self.gap, self.gap * 21, self.gap * 15, outline=self.color, width=4)
        self.canvas.create_text(self.gap * 18, self.gap * 2, text="White: " + self.player1.name, fill='black', font=('Helvetica 15'))
        self.canvas.create_text(self.gap * 18, self.gap * 3, text="Black: " + self.player2.name, fill='black', font=('Helvetica 15'))
        self.turn_text = self.canvas.create_text(self.gap * 18, self.gap * 4, text="Turn: " + self.place_turn, fill='black', font=('Helvetica 15'))
        self.winner_text = self.canvas.create_text(self.gap * 18, self.gap * 6, text="Winner: ", fill='black', font=('Helvetica 16'))
        button = ttk.Button(self.canvas, text="Restart", command=self.restart)
        self.canvas.create_window(self.gap * 18.5, self.gap * 8, window=button)
        self.update_board()

    def place_piece(self, event):
        if not self.started:
            return
        col = round(event.x / self.gap - 1)
        row = round(event.y / self.gap - 1)
        if (col < 0 or col > 14) or (row < 0 or row > 14):
            return
        temp_piece = Piece(row, col, self.place_turn)
        if self.put_piece(temp_piece):
            if self.place_turn == "White":
                self.place_turn = "Black"
                self.canvas.itemconfig(self.turn_text, text="Turn: " + self.place_turn)
            else:
                self.place_turn = "White"
                self.canvas.itemconfig(self.turn_text, text="Turn: " + self.place_turn)

    def put_piece(self, piece: Piece):
        if self.check_array[piece.row][piece.col] == "":
            self.canvas.create_oval((piece.col + 1) * self.gap, (piece.row + 1) * self.gap,
                                    (piece.col + 1) * self.gap, (piece.row + 1) * self.gap,
                                    width=int(self.gap * 0.7), outline=piece.piece_type)
            self.check_array[piece.row][piece.col] = piece.piece_type
            self.update_board()
            t = threading.Thread(target=self.play_sound)
            t.start()
            if self.check_win(piece):
                self.started = False
                print(piece.piece_type + " wins!")
                self.canvas.itemconfig(self.winner_text, text="Winner: " + piece.piece_type)
            return True
        else:
            return False

    def update_board(self):
        self.canvas.update()

    def play_sound(self):
        song = AudioSegment.from_wav(self.song)
        play(song)

    def check_win(self, piece: Piece):
        win_counter:int = 1
        # check left
        for i in range(1,5):
            if (piece.col - i) >= 0 and self.check_array[piece.row][piece.col - i] == piece.piece_type:
                win_counter += 1
            else:
                break
        if win_counter >= 5:
            return True
        # check right
        for i in range(1,5):
            if (piece.col + i) <= 14 and self.check_array[piece.row][piece.col + i] == piece.piece_type:
                win_counter += 1
            else:
                break
        if win_counter >= 5:
            return True
        # Check vertical
        win_counter = 1
        # check up
        for i in range(1,5):
            if (piece.row - i) >= 0 and self.check_array[piece.row - i][piece.col] == piece.piece_type:
                win_counter += 1
            else:
                break
        if win_counter >= 5:
            return True
        # check down
        for i in range(1,5):
            if (piece.row + i) <= 14 and self.check_array[piece.row + i][piece.col] == piece.piece_type:
                win_counter += 1
            else:
                break
        if win_counter >= 5:
            return True

        win_counter = 1
        # check up + left
        for i in range(1, 5):
            if (piece.row - i) >= 0 and (piece.col - i) >= 0 and self.check_array[piece.row - i][piece.col - i] == piece.piece_type:
                win_counter += 1
            else:
                break
        if win_counter >= 5:
            return True
        # check down + right
        for i in range(1, 5):
            if (piece.row + i) <= 14 and (piece.col + i) <= 14 and self.check_array[piece.row + i][piece.col + i] == piece.piece_type:
                win_counter += 1
            else:
                break
        if win_counter >= 5:
            return True

        win_counter = 1
        # check up + right
        for i in range(1, 5):
            if (piece.row - i) >= 0 and (piece.col + i) <= 14 and self.check_array[piece.row - i][piece.col + i] == piece.piece_type:
                win_counter += 1
            else:
                break
        if win_counter >= 5:
            return True
        # check down + left
        for i in range(1, 5):
            if (piece.row + i) <= 14 and (piece.col - i) >= 0 and self.check_array[piece.row + i][piece.col - i] == piece.piece_type:
                win_counter += 1
            else:
                break
        if win_counter >= 5:
            return True

    def restart(self):
        self.canvas.delete("all")
        self.check_array = [[""] * 15 for i in range(15)]
        self.place_turn = "White"
        self.started = True
        self.draw()