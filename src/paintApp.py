import tkinter as tk
from .shapes import Point, Line, Circle
from .gui import Grid


class PaintApp:
    def make_point(self, canvas, px):
        p = Point((px.x, px.y))
        self.shapes.append(p)
        p.plot(canvas, self.grid)

    def make_line(self, canvas, px):
        if not hasattr(self, "start_pos"):
            self.start_pos = None
        if self.start_pos is None:
            self.prev_value = px.value
            px.set_pixel(canvas, 0.5)
            self.start_pos = (px.x, px.y)
        else:
            self.grid.get_pixel(*self.start_pos).set_pixel(canvas, self.prev_value)
            self.prev_value = None
            l = Line(self.start_pos, (px.x, px.y))
            self.shapes.append(l)
            l.plot(canvas, self.grid, self.line_algo.get())
            self.start_pos = None

    def make_circle(self, canvas, px):
        if not hasattr(self, "start_pos"):
            self.start_pos = None
        if self.start_pos is None:
            self.prev_value = px.value
            px.set_pixel(canvas, 0.5)
            self.start_pos = (px.x, px.y)
        else:
            self.grid.get_pixel(*self.start_pos).set_pixel(canvas, self.prev_value)
            self.prev_value = None
            c = Circle(self.start_pos, (px.x, px.y))
            self.shapes.append(c)
            c.plot(canvas, self.grid)
            self.start_pos = None

    def make_shape(self, ev, canvas, px):
        if self.draw_shape.get() == "point":
            self.make_point(canvas, px)
        elif self.draw_shape.get() == "line":
            self.make_line(canvas, px)
        elif self.draw_shape.get() == "circle":
            self.make_circle(canvas, px)

    def reset_canvas(self, destroy_shapes=True):
        if hasattr(self, "canvas"):
            self.canvas.destroy()


        self.grid = Grid(self.rows, self.cols)
        self.canvas = self.grid.make_canvas(
            self.root, self.height, self.width, self.make_shape
        )

        if destroy_shapes or not hasattr(self, "shapes"):
            self.shapes = []
        else:
            for s in self.shapes: s.plot(self.canvas, self.grid)

    def resize_dialog(self):
        dialog = tk.Toplevel()

        tk.Label(dialog, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        rows = tk.Entry(dialog, width=10)
        rows.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Cols:").grid(row=0, column=2, padx=5, pady=5)
        cols = tk.Entry(dialog, width=10)
        cols.grid(row=0, column=3, padx=5, pady=5)
        height = tk.Entry(dialog, width=10)
        height.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Height:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(dialog, text="Width:").grid(row=2, column=2, padx=5, pady=5)
        width = tk.Entry(dialog, width=10)
        width.grid(row=2, column=3, padx=5, pady=5)

        rows.insert(0, str(self.rows))
        cols.insert(0, str(self.cols))
        height.insert(0, str(self.height))
        width.insert(0, str(self.width))

        def close():
            if (
                (rows.get().isdigit() == False or int(rows.get()) < 0)
                or (cols.get().isdigit() == False or int(cols.get()) < 0)
                or (height.get().isdigit() == False or int(height.get()) < 0)
                or (width.get().isdigit() == False or int(width.get()) < 0)
            ):
                tk.Label(
                    dialog, text="Warning: All data must be positive integer!"
                ).grid(row=3, column=0, padx=5, pady=5, columnspan=2)
                return

            self.rows, self.cols, self.height, self.width = (
                int(rows.get()),
                int(cols.get()),
                int(height.get()),
                int(width.get()),
            )

            self.reset_canvas()

            dialog.destroy()

        tk.Button(dialog, text="Reset and Resize", command=close).grid(
            row=3, column=0, columnspan=2, pady=10
        )

    def __init__(self, root, title="PaintApp", rows=25, cols=25, height=500, width=500):
        root.title(title)

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        self.root = root
        self.rows, self.cols, self.height, self.width = rows, cols, height, width
        self.reset_canvas()

        configs_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Configs", menu=configs_menu)

        configs_menu.add_command(label="Resize", command=lambda: self.resize_dialog())
        configs_menu.add_command(label="Reset", command=lambda: self.reset_canvas())
        configs_menu.add_separator()
        configs_menu.add_command(label="Exit", command=root.destroy)

        draw_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Draw", menu=draw_menu)

        self.draw_shape = tk.StringVar(value="point")
        self.line_algo = tk.StringVar(value="dda")

        draw_menu.add_checkbutton(
            label="Point", onvalue="point", variable=self.draw_shape
        )
        draw_menu.add_checkbutton(
            label="Line", onvalue="line", variable=self.draw_shape
        )
        draw_menu.add_checkbutton(
            label="Circle", onvalue="circle", variable=self.draw_shape
        )

        draw_menu.add_separator()

        line_menu = tk.Menu(draw_menu, tearoff=0)
        draw_menu.add_cascade(label="Line Algorithim", menu=line_menu)
        line_menu.add_checkbutton(label="DDA", onvalue="dda", variable=self.line_algo)
        line_menu.add_checkbutton(
            label="Bresenham", onvalue="bresenham", variable=self.line_algo
        )
