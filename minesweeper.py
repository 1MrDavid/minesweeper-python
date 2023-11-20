import random
import tkinter as tk

#Game Settings
rows = 10
columns = 10
mines = 10

#Board, mines and values asignment
def create_board(rows, columns):
    board = []
    for row in range(rows):
        board.append([])
        for column in range(columns):
            board[row].append(0)
    return board

def place_mines(board, num_mines):
    for _ in range(num_mines):
        row, column = random.randint(0, len(board) - 1), random.randint(0, len(board[0]) - 1)
        while board[row][column] == "X":
            row, column = random.randint(0, len(board) - 1), random.randint(0, len(board[0]) - 1)
        board[row][column] = "X"

def increment_adjacent_cells(board, i, j):
    rows, columns = len(board), len(board[0])

    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(columns, j + 2)):
            if board[x][y] != "X":
                board[x][y] += 1

def set_value(board, rows, columns):
    for i in range(rows):
        for j in range(columns):
            if board[i][j] == "X":
                increment_adjacent_cells(board, i, j)

#Tkinter (UI) functions
class MinesweeperGUI:
    def __init__(self, master, board):
        self.master = master
        self.board = board
        self.buttons = []

        frame = tk.Frame(master)
        frame.grid(row=0, column=0, padx=10, pady=10)

        for i in range(rows):
            row_buttons = []
            for j in range(columns):
                button = tk.Button(frame, text="", width=3, height=2, command=lambda i=i, j=j: self.click_cell(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        restart_button = tk.Button(master, text="Restart", command=self.restart_game)
        restart_button.grid(row=1, column=0, pady=10)

    def click_cell(self, i, j):
        value = str(self.board[i][j])

        if value == "X":
            self.reveal_all_mines()
            self.disable_all_buttons()
        elif value == "0":
            self.reveal_adjacent_cells(i, j)
            self.buttons[i][j].config(state=tk.DISABLED)
        else:
            self.buttons[i][j].config(text=value, state=tk.DISABLED)

    def reveal_adjacent_cells(self, i, j):
        rows, columns = len(self.board), len(self.board[0])

        if self.buttons[i][j]['state'] == tk.DISABLED:
            return

        self.buttons[i][j].config(text=str(self.board[i][j]), state=tk.DISABLED)

        if self.board[i][j] == 0:
            for x in range(max(0, i - 1), min(rows, i + 2)):
                for y in range(max(0, j - 1), min(columns, j + 2)):
                    if self.board[x][y] != "X":
                        self.reveal_adjacent_cells(x, y)

    def reveal_all_mines(self):
        for i in range(rows):
            for j in range(columns):
                if self.board[i][j] == "X":
                    self.buttons[i][j].config(text="X")

    def disable_all_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)

    def restart_game(self):
        self.master.destroy()
        main()

def main():
    #Board setting calls
    board = create_board(rows, columns)
    place_mines(board, mines)
    set_value(board, rows, columns)
    #UI set
    root = tk.Tk()
    root.title("Minesweeper")
    root.geometry("350x500")
    gui = MinesweeperGUI(root, board)
    root.mainloop()

main()
