from time import sleep
import tkinter as tk
from src.grid import Grid

if __name__ == "__main__":
    root = tk.Tk()
    root.title("NxM Clickable Grid")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # create a menu
    file_menu = tk.Menu(menubar, tearoff=False)

    # add a menu item to the menu
    file_menu.add_command(
        label='Exit',
        command=root.destroy
    )

    menubar.add_cascade(
        label="Configs",
        menu=file_menu
    )

    rows = 20
    cols = 20

    grid = Grid(rows, cols)
    canvas = grid.make_canvas(root, 700, 700)

    file_menu.add_command(
        label='Reset',
        command=canvas.destroy
    )

    root.mainloop()
