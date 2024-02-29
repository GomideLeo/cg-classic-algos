from time import sleep
import tkinter as tk
from tkinter import ttk
from src.shapes import Point, Line, Circle
from src.gui import Grid


def reset_canvas(rows=25, cols=25, height=1000, width=1000):
    global grid, canvas, shapes
    if "canvas" in globals():
        canvas.destroy()
    if "shapes" in globals():
        shapes = []

    grid = Grid(rows, cols)
    canvas = grid.make_canvas(root, height, width, make_shape)

    return grid, canvas

def make_point(canvas, px):
    global shapes, grid

    p = Point((px.x, px.y))
    shapes.append(p)
    p.plot(canvas, grid)

def make_line(canvas, px):
    global start_pos, prev_value, line_algo, shapes, grid

    if "start_pos" not in globals(): start_pos = None
    start_pos = None
    if start_pos is None:
        prev_value = px.value
        px.set_pixel(canvas, 0.5)
        start_pos = (px.x, px.y)
    else:
        grid.get_pixel(*start_pos).set_pixel(canvas, prev_value)
        prev_value = None
        l = Line(start_pos, (px.x, px.y))
        shapes.append(l)
        l.plot(canvas, grid, line_algo.get())
        start_pos = None

def make_circle(canvas, px):
    global start_pos, prev_value, shapes, grid

    if "start_pos" not in globals(): start_pos = None
    if start_pos is None:
        prev_value = px.value
        px.set_pixel(canvas, 0.5)
        start_pos = (px.x, px.y)
    else:
        grid.get_pixel(*start_pos).set_pixel(canvas, prev_value)
        prev_value = None
        c = Circle(start_pos, (px.x, px.y))
        shapes.append(c)
        c.plot(canvas, grid)
        start_pos = None

def make_shape(ev, canvas, px):
    global draw_shape

    if draw_shape.get() == 'point':
        make_point(canvas, px)
    elif draw_shape.get() == 'line':
        make_line(canvas, px)
    elif draw_shape.get() == 'circle':
        make_circle(canvas, px)

if __name__ == "__main__":
    shapes = []

    root = tk.Tk()
    root.title("Grid")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    rows = 20
    cols = 20
    height = 500
    width = 500

    grid, canvas = reset_canvas(rows, cols, height, width)

    # create a menu
    configs_menu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Configs", menu=configs_menu)

    configs_menu.add_command(label="Exit", command=root.destroy)

    configs_menu.add_command(
        label="Reset", command=lambda: reset_canvas(rows, cols, height, width)
    )

    draw_menu = tk.Menu(menubar, tearoff=False)
    
    menubar.add_cascade(label="Draw", menu=draw_menu)

    draw_shape = tk.StringVar(value='point')
    line_algo = tk.StringVar(value='dda')

    draw_menu.add_checkbutton(label="Point", onvalue="point", variable=draw_shape)
    draw_menu.add_checkbutton(label="Line", onvalue="line", variable=draw_shape)
    draw_menu.add_checkbutton(label="Circle", onvalue="circle", variable=draw_shape)

    draw_menu.add_separator()

    line_menu = tk.Menu(draw_menu, tearoff=0)
    draw_menu.add_cascade(label="Line Algorithim", menu=line_menu)
    line_menu.add_checkbutton(label="DDA", onvalue="dda", variable=line_algo)
    line_menu.add_checkbutton(
        label="Bresenham", onvalue="bresenham", variable=line_algo
    )

    root.mainloop()
