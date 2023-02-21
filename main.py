from FiveInRow.CheckerBoard import CheckerBoard
from FiveInRow.Piece import Piece
from FiveInRow.Player import Player
from tkinter import *

tk = Tk()
tk.title("五子棋")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
game_canvas = Canvas(tk, width=2200, height=1600, bd=0, highlightthickness=0)
game_canvas.configure(bg='#EEC591')
game_canvas.pack()
tk.update()


player1 = Player("Michael")
player2 = Player("Zeng Xuezhi")
checkerboard = CheckerBoard(game_canvas, player1, player2)
checkerboard.draw()

# piece1 = Piece(4, 7, "black")
# piece2 = Piece(4, 7, "white")
# checkerboard.place_piece(piece1)
# checkerboard.place_piece(piece2)

game_canvas.mainloop()





# aList = [[" "] * 10 for i in range(10)]
# aList[0][0] = "Black"
# aList[1][3] = "White"
# aList[0][0] = "White"
# print(aList)
