import tkinter as tk
from src.paintApp import PaintApp

if __name__ == "__main__":
    root = tk.Tk()

    paintApp = PaintApp(root, rows=32, cols=32, height=712, width=712)

    root.mainloop()
