import tkinter as tk
from tkinter import font as tkFont
import gamelogic as gl

color_map = {
            0: "#A7A1A0",
            2: "#F7F1F0",
            4: "#F1E4BA",
            8: "#F2B771",
            16: "#F29071",
            32: "#F3645B",
            64: "#E7372B",
            128: "#B4E72B",
            256: "#39E72B",
            512: "#27DB69",
            1024: "#27DBB2",
            2048: "#5627DB"
        }


class GameBoard(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('2048 Game')
        self.master.bind("<Key>", self.key_event)
        self.board = gl.Board()
        self.draw_grid()
        self.win_displayed = False
        self.loss_displayed = False


    def draw_grid(self):

        for i in range(self.board.size):
            self.columnconfigure(i)
            self.rowconfigure(i)
            for j in range(self.board.size):
                frame = tk.Frame(
                    master=self,
                    relief=tk.RAISED,
                    borderwidth=int(40/gl.Board.SIZE)
                )
                cell_value = self.board.board[i][j]
                label_font_size = int(90 / gl.Board.SIZE)
                label_font = tkFont.Font(family='SimSun', size=label_font_size, weight='bold')
                label = tk.Label(master=frame, bg="maroon", fg="white", width=int(1.8 * label_font_size/gl.Board.SIZE), height=int(label_font_size/gl.Board.SIZE), font=label_font, text=cell_value)
                bg_color = color_map[cell_value]
                fg_color = "black" if cell_value <= 4 else "white"
                text = str(cell_value) if cell_value != 0 else ""
                label.config(text=text, bg=bg_color, fg=fg_color)
                frame.grid(row=i, column=j)
                label.pack() 


        scoreboard = tk.Frame(
            master=self,
            relief=tk.SUNKEN,
            borderwidth=3
        )
        scoreboard.grid(row=self.board.size, column=0, columnspan=self.board.size, sticky="ew")

        score_label = tk.Label(
            master=scoreboard,
            text="Score: 0",
            font=('SimSun', 20, 'bold')
        )
        score_label.pack(fill=tk.BOTH, expand=True)
                   

    def update_grid(self):
        self.lose_window = None
        self.win_window = None
        for i in range(self.board.size):
            for j in range(self.board.size):
                label = self.grid_slaves(row=i, column=j)[0].winfo_children()[0]
                cell_value = self.board.board[i][j]
                if cell_value in color_map:
                    bg_color = color_map[cell_value]
                else:
                    bg_color = "black"
                fg_color = "black" if cell_value <= 4 else "white"
                text = str(cell_value) if cell_value != 0 else ""
                label.config(text=text, bg=bg_color, fg=fg_color)

        score_label = self.grid_slaves(row=self.board.size, column=0)[0].winfo_children()[0]
        score_label.config(text=f"Score: {self.board.score}")

        if self.board.has_lost() and not self.loss_displayed:
            self.loss_displayed = True
            lose_window = tk.Toplevel(self.master)
            lose_window.title("Game Over")
            label = tk.Label(lose_window, text="Game Over", font=('SimSun', 100, 'bold'), fg='red')
            label.pack()

            # Initialize button to restart the game
            retry_button = tk.Button(lose_window, text="Restart", font=('SimSun', 25), command=lambda: [self.reset_board(), lose_window.destroy()])
            retry_button.pack()

            # Initialize button to quit and close the window
            quit_button = tk.Button(lose_window, text="Quit", font=('SimSun', 25), command=lambda: self.master.destroy())
            quit_button.pack()
            

        if self.board.has_won() and not self.win_displayed:
            self.win_displayed = True
            win_window = tk.Toplevel(self.master)
            win_window.title("Congratulations")
            label = tk.Label(win_window, text="You Win!", font=('SimSun', 100, 'bold'), fg='green')
            label.pack()
            continue_button = tk.Button(win_window, text="Continue", font=('SimSun', 25), command=lambda: [win_window.destroy()])
            continue_button.pack()
            retry_button = tk.Button(win_window, text="Restart", font=('SimSun', 25), command=lambda: [self.reset_board(), win_window.destroy()])
            retry_button.pack()
            quit_button = tk.Button(win_window, text="Quit", font=('SimSun', 25), command=lambda: self.master.destroy())
            quit_button.pack()

    def reset_board(self):
        self.board = gl.Board()
        self.loss_displayed = False
        self.win_displayed = False
        self.update_grid()

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
        elif event.keysym == "l":
            self.board.insta_lose()
            self.update_grid()
        elif event.keysym == "r":
            self.reset_board()

        if direction:
            self.board.move(direction)
            self.update_grid()

window = tk.Tk()
game_board = GameBoard(master=window)
min_side_size = 800
window.minsize(min_side_size, min_side_size)
window.geometry(f"{min_side_size}x{min_side_size}")
game_board.place(relx=0.5, rely=0.5, anchor="center")
window.mainloop()
