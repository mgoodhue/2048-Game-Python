import tkinter as tk
from tkinter import font as tkFont
import gamelogic as gl

color_dict = {
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
        self.master.title('2048')
        self.master.bind("<Key>", self.key_event)
        self.difficulty = gl.Board.DIFFICULTY
        self.rules = "Press R to reset Board"
        if self.difficulty == "easy":
            self.board = gl.BoardEasy()
            self.rules += "\nPress C to clean up board\n"
        elif self.difficulty == "normal":
            self.board = gl.Board()
        elif self.difficulty == "hard":
            self.board = gl.BoardHard()
        else:
            raise ValueError("Difficulty must be Easy/Normal/Hard")
        
        self.draw_grid()
        self.win_displayed = False
        self.loss_displayed = False


    def draw_grid(self):

        for i in range(self.board.size):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)
            for j in range(self.board.size):
                frame = tk.Frame(
                    master=self,
                    relief=tk.RAISED,
                    borderwidth=int(40/self.board.size)
                )
                cell_value = self.board.board[i][j]
                number = str(cell_value) if cell_value != 0 else ""

                label_font_size = int(90 / self.board.size)
                cell_size = int(35 / self.board.size)
                label_font = tkFont.Font(
                    family='SimSun', 
                    size=label_font_size, 
                    weight='bold')
                cell_label = tk.Label(
                    master=frame,
                    width=cell_size,
                    height=int(cell_size / 1.8),
                    font=label_font,
                    text=number
                )
                bg_color = color_dict[cell_value]
                fg_color = "black" if cell_value <= 4 else "white"
                cell_label.config(
                    text=number, 
                    bg=bg_color, 
                    fg=fg_color)
                frame.grid(row=i, column=j)
                cell_label.pack() 

        # Scoreboard Initialization
        scoreboard = tk.Frame(
            master=self,
            relief=tk.SUNKEN,
            borderwidth=3
        )
        scoreboard.grid(
            row=self.board.size, 
            column=0, 
            columnspan=self.board.size, 
            sticky="ew")

        score_label = tk.Label(
            master=scoreboard,
            text="Score: 0",
            font=('SimSun', 20, 'bold')
        )
        score_label.pack(fill=tk.BOTH, expand=True)

        difficulty_label = tk.Label(
            master=scoreboard,
            text="Difficulty: " + self.difficulty.capitalize(),
            font=('SimSun', 20, 'bold')
        )
        difficulty_label.pack(fill=tk.BOTH, expand=True)

        self.rowconfigure(self.board.size, weight=1)
        # Side Panel
        side_panel = tk.Frame(self, bg='lightgray', relief=tk.SUNKEN)
        side_panel.grid(row=0, column=self.board.size, rowspan=self.board.size + 1, sticky='ns')

        rules_label = tk.Label(side_panel, text=self.rules, font=('SimSun', 25), bg='lightgray')
        rules_label.pack(pady=self.board.size * 65)
                   

    def update_grid(self):
        lose_window = None
        win_window = None
        for i in range(self.board.size):
            for j in range(self.board.size):
                grid_nums = self.grid_slaves(row=i, column=j)[0].winfo_children()[0]
                cell_value = self.board.board[i][j]
                if cell_value in color_dict:
                    bg_color = color_dict[cell_value]
                else:
                    bg_color = "gray"
                fg_color = "black" if cell_value <= 4 or cell_value >= 2048 else "white"
                text = str(cell_value) if cell_value != 0 else ""
                grid_nums.config(text=text, bg=bg_color, fg=fg_color)

        score_label = self.grid_slaves(row=self.board.size, column=0)[0].winfo_children()[0]
        score_label.config(text=f"Score: {self.board.score}")

        if self.board.has_lost() and not self.loss_displayed and self.difficulty != "easy":
            self.loss_displayed = True
            lose_window = tk.Toplevel(self.master)
            lose_window.title("Game Over")
            game_over_label = tk.Label(
                lose_window, 
                text="Game Over", 
                font=('SimSun', 100, 'bold'), 
                fg='red')
            game_over_label.pack()

            # Initialize button to restart the game
            retry_button = tk.Button(
                lose_window, 
                text="Restart", 
                font=('SimSun', 25), 
                command=lambda: [
                    self.board.reset_board(), 
                    self.update_grid(), 
                    setattr(self, 'loss_displayed', False), 
                    lose_window.destroy()])
            retry_button.pack()

            # Initialize button to quit and close the window
            quit_button = tk.Button(
                lose_window, 
                text="Quit", 
                font=('SimSun', 25), 
                command=lambda: self.master.destroy())
            quit_button.pack()

        if self.board.has_won() and not self.win_displayed:
            self.win_displayed = True
            win_window = tk.Toplevel(self.master)
            win_window.title("Congratulations")

            label = tk.Label(
                win_window, 
                text="You Win!", 
                font=('SimSun', 100, 'bold'), 
                fg='green')
            label.pack()

            continue_button = tk.Button(
                win_window, 
                text="Continue", 
                font=('SimSun', 25), 
                command=lambda: [
                    win_window.destroy()])
            continue_button.pack()

            retry_button = tk.Button(
                win_window, 
                text="Restart", 
                font=('SimSun', 25), 
                command=lambda: 
                [self.board.reset_board(), self.update_grid(), win_window.destroy(), setattr(self, 'win_displayed', False)])
            retry_button.pack()

            quit_button = tk.Button(
                win_window, 
                text="Quit", 
                font=('SimSun', 25), 
                command=lambda: self.master.destroy())
            quit_button.pack()

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

        # Instantly win
        elif event.keysym == "w":
            self.board.insta_win()
            self.update_grid()

        # Instantly Lose
        elif event.keysym == "l":
            self.board.insta_lose()
            self.update_grid()

        # Reset Board
        elif event.keysym == "r":
            self.board.reset_board()
            self.win_displayed = False
            self.loss_displayed = False
            self.update_grid()

        elif event.keysym == "c" and self.difficulty == "easy":
            self.board.clear_board()
            self.update_grid()

        elif event.keysym == "escape":
            self.master.destroy()

        if direction:
            self.board.move(direction)
            self.update_grid()

window = tk.Tk()
game_board = GameBoard(master=window)
min_height = 800
min_width = 1200
window.minsize(min_width, min_height)
window.geometry(f"{min_width}x{min_height}")
game_board.place(relx=0.5, rely=0.5, anchor="center")
window.mainloop()
