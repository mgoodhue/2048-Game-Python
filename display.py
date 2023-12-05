import tkinter as tk
from tkinter import font as tkFont
import gamelogic as gl


class GameBoard(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('2048 Game')
        self.master.bind("<Key>", self.key_event)
        self.win_label = tk.Label(self, text='', font=('Calibri', 20, 'bold'), fg='green')
        self.win_label.grid(row=gl.Board.SIZE, column=0, columnspan=gl.Board.SIZE, sticky="ew")
        self.board = gl.Board()
        self.draw_grid()

    def draw_grid(self):

        for i in range(gl.Board.SIZE):
            self.columnconfigure(i, weight=1, minsize=50)
            self.rowconfigure(i, weight=1, minsize=50)
            for j in range(gl.Board.SIZE):
                frame = tk.Frame(
                    master=self,
                    relief=tk.RAISED,
                    borderwidth=10
                )
                label_font_size = int((1/gl.Board.SIZE) * 100)
                label_font = tkFont.Font(family='Calibri', size=label_font_size, weight='bold', )
                label = tk.Label(master=frame, bg="maroon", fg="white", width=10, height=4, font=label_font, text=self.board.board[i][j])
                frame.grid(row=i, column=j, padx=2, pady=2)
                label.pack() 


        scoreboard = tk.Frame(
            master=self,
            relief=tk.SUNKEN,
            borderwidth=3
        )
        scoreboard.grid(row=gl.Board.SIZE, column=0, columnspan=gl.Board.SIZE, sticky="ew")

        score_label = tk.Label(
            master=scoreboard,
            text="Score: 0",
            font=('Calibri', 20, 'bold')
        )
        score_label.pack(fill=tk.BOTH, expand=True)

                   

    def update_grid(self):
        for i in range(gl.Board.SIZE):
            for j in range(gl.Board.SIZE):
                label = self.grid_slaves(row=i, column=j)[0].winfo_children()[0]
                label.config(text=self.board.board[i][j])

        score_label = self.grid_slaves(row=gl.Board.SIZE, column=0)[0].winfo_children()[0]
        score_label.config(text=f"Score: {self.board.score}")

        if self.board.has_lost():
            label.config(text="You Lose!")
            self.master.destroy()

        if self.board.has_won():
            label.config(text="You Win!")
            self.master.destroy()
                

    def key_event(self, event):
        direction = ""
        if event.keysym == "Up":
            direction = "up"
        elif event.keysym == "Down":
            direction = "down"
        elif event.keysym == "Left":
            direction = "left"
        elif event.keysym == "Right":
            direction = "right"
        # Method to test win screen
        elif event.keysym == "m":
            self.board.insta_win()
            self.update_grid()
        # Method to test lose screen
        elif event.keysym == "l":
            self.board.insta_lose()
            self.update_grid()


        if direction:
            self.board.move(direction)
            self.update_grid()

window = tk.Tk()
game_board = GameBoard(master=window)
game_board.pack(fill=tk.BOTH, expand=True)
window.mainloop()


        
