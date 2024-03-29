import tkinter as tk
import tkinter.ttk as ttk
from .shapes import Point, Line, Circle
from .gui import Grid


class PaintApp:
    def make_point(self, canvas, px):
        """
        Create a Point object at the given pixel coordinates and plot it on the canvas.

        Args:
            canvas: The canvas to plot the Point on.
            px: The Pixel object representing the coordinates of the Point.

        Returns:
            None
        """

        p = Point((px.x, px.y))
        self.shapes.append(p)
        p.plot(canvas, self.grid)

    def make_line(self, canvas, px):
        """
        Create a Line object from the starting pixel coordinates to the given pixel coordinates
        and plot it on the canvas using the specified line algorithm.

        Args:
            canvas: The canvas to plot the Line on.
            px: The Pixel object representing the ending coordinates of the Line.

        Returns:
            None
        """
        
        if not hasattr(self, 'start_pos'):
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
        """
        Create a Circle object with the center at the starting pixel coordinates and the radius
        determined by the ending pixel coordinates, then plot it on the canvas.

        Args:
            canvas: The canvas to plot the Circle on.
            px: The Pixel object representing the ending coordinates of the Circle's radius.

        Returns:
            None
        """

        if not hasattr(self, 'start_pos'):
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

    def crop(self, canvas, px):
        """
        Crop the canvas based on the starting and ending pixel coordinates.

        Args:
            canvas: The canvas to crop.
            px: The Pixel object representing the ending coordinates of the crop area.

        Returns:
            None
        """

        if not hasattr(self, 'start_pos'):
            self.start_pos = None
        if self.start_pos is None:
            self.prev_value = px.value
            px.set_pixel(canvas, 0.5)
            self.start_pos = (px.x, px.y)
        else:
            self.grid.get_pixel(*self.start_pos).set_pixel(canvas, self.prev_value)
            self.prev_value = None
            self.crop_canvas(self.start_pos, (px.x, px.y))
            self.start_pos = None

    def make_shape(self, ev, canvas, px):
        """
        Determine the shape to draw based on the user's selection and call the respective
        make_* method to create and plot the shape.

        Args:
            ev: The event that triggered the shape creation.
            canvas: The canvas to plot the shape on.
            px: The Pixel object representing the coordinates of the shape.

        Returns:
            None
        """

        if self.draw_shape.get() == 'point':
            self.make_point(canvas, px)
        elif self.draw_shape.get() == 'line':
            self.make_line(canvas, px)
        elif self.draw_shape.get() == 'circle':
            self.make_circle(canvas, px)
        elif self.draw_shape.get() == 'crop':
            self.crop(canvas, px)

    def crop_canvas(self, corner1, corner2):
        """
        Crop the canvas to the specified area defined by the two corner points.
        Updates the canvas size and origin accordingly.

        Args:
            corner1: Tuple representing the (x, y) coordinates of one corner of the crop area.
            corner2: Tuple representing the (x, y) coordinates of the opposite corner of the crop area.

        Returns:
            None
        """

        if not hasattr(self, 'original_shape'):
            self.original_shape = (self.cols, self.rows)

        self.cols, self.rows = (
            abs(corner1[0] - corner2[0]) + 1,
            abs(corner1[1] - corner2[1]) + 1,
        )
        self.origin = (min(corner1[0], corner2[0]), min(corner1[1], corner2[1]))

        self.reset_canvas(False)

    def reset_crop(self):
        """
        Reset the canvas crop to its original size and position.
        If the canvas was not previously cropped, this method has no effect.

        Returns:
            None
        """

        if hasattr(self, 'original_shape'):
            self.cols, self.rows = self.original_shape
            del self.original_shape

        self.origin = (0, 0)

        self.reset_canvas(False)

    def reset_canvas(self, destroy_shapes=True):
        """
        Reset the canvas, optionally destroying all shapes drawn on it.

        Args:
            destroy_shapes (bool): If True, all shapes drawn on the canvas will be destroyed. Default is True.

        Returns:
            None
        """

        if hasattr(self, 'canvas'):
            self.canvas.destroy()

        self.grid = Grid(self.rows, self.cols, self.origin)
        self.canvas = self.grid.make_canvas(
            self.root, self.height, self.width, self.make_shape
        )

        if destroy_shapes or not hasattr(self, 'shapes'):
            self.shapes = []
        else:
            max_pos = (self.origin[0] + self.cols - 1, self.origin[1] + self.rows - 1)
            for s in self.shapes:
                s_draw = (
                    s.crop(self.origin, max_pos, self.crop_algo.get())
                    if isinstance(s, Line)
                    else s.crop(self.origin, max_pos)
                )
                if s_draw is not None:
                    print(f'{str(s_draw)} drawn')
                    (
                        s_draw.plot(self.canvas, self.grid, self.line_algo.get())
                        if isinstance(s_draw, Line)
                        else s_draw.plot(self.canvas, self.grid)
                    )
                else:
                    print(f'{str(s)} ignored')

    def resize_dialog(self):
        dialog = tk.Toplevel()

        tk.Label(dialog, text='Rows:').grid(row=0, column=0, padx=5, pady=5)
        rows = tk.Entry(dialog, width=10)
        rows.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dialog, text='Cols:').grid(row=0, column=2, padx=5, pady=5)
        cols = tk.Entry(dialog, width=10)
        cols.grid(row=0, column=3, padx=5, pady=5)
        height = tk.Entry(dialog, width=10)
        height.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(dialog, text='Height:').grid(row=2, column=0, padx=5, pady=5)
        tk.Label(dialog, text='Width:').grid(row=2, column=2, padx=5, pady=5)
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
                    dialog, text='Warning: All data must be positive integer!'
                ).grid(row=3, column=0, padx=5, pady=5, columnspan=2)
                return

            self.rows, self.cols, self.height, self.width = (
                int(rows.get()),
                int(cols.get()),
                int(height.get()),
                int(width.get()),
            )

            if hasattr(self, 'original_shape'):
                del self.original_shape
            self.reset_canvas()

            dialog.destroy()

        tk.Button(dialog, text='Reset and Resize', command=close).grid(
            row=4, column=0, columnspan=2, pady=10
        )
        tk.Button(dialog, text='Cancel', command=dialog.destroy).grid(
            row=4, column=2, columnspan=2, pady=10
        )

    def translate_dialog(self):
        dialog = tk.Toplevel()
        label = tk.Label(dialog, text='')
        label.grid(row=3, column=0, padx=5, pady=5, columnspan=4)

        tk.Label(dialog, text='X Factor:').grid(row=0, column=0, padx=5, pady=5)
        x_translate = tk.Entry(dialog, width=10)
        x_translate.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dialog, text='Y Factor:').grid(row=0, column=2, padx=5, pady=5)
        y_translate = tk.Entry(dialog, width=10)
        y_translate.grid(row=0, column=3, padx=5, pady=5)

        shape_val = tk.StringVar(value='All')
        tk.Label(dialog, text='Shape:').grid(row=1, column=0, padx=5, pady=5)
        shape = ttk.Combobox(dialog, textvariable=shape_val)
        shape.config(values=('All', *[str(s) for s in self.shapes]))
        shape['state'] = 'readonly'
        shape.grid(row=1, column=1, padx=5, pady=5, columnspan=3)

        x_translate.insert(0, '0')
        y_translate.insert(0, '0')

        def close():
            if (x_translate.get().lstrip('-+').isnumeric() == False) or (
                y_translate.get().lstrip('-+').isnumeric() == False
            ):
                label.config(text='Warning: Translate values must be integer!"')
                return
            elif shape.current() < 0:
                label.config(text='Select an option!')
                return

            x_t, y_t = (
                int(x_translate.get()),
                int(y_translate.get()),
            )

            if shape.current() == 0:
                for s in self.shapes:
                    s.translate(x_t, y_t)
            else:
                self.shapes[shape.current() - 1].translate(x_t, y_t)

            self.reset_canvas(destroy_shapes=False)

            dialog.destroy()

        tk.Button(dialog, text='Translate', command=close).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        tk.Button(dialog, text='Cancel', command=dialog.destroy).grid(
            row=4, column=2, columnspan=2, pady=10
        )

    def rotation_dialog(self):
        dialog = tk.Toplevel()
        label = tk.Label(dialog, text='')
        label.grid(row=3, column=0, padx=5, pady=5, columnspan=4)

        tk.Label(dialog, text='Rotation (θ°):').grid(row=0, column=0, padx=5, pady=5)
        theta = tk.Entry(dialog, width=10)
        theta.grid(row=0, column=1, padx=5, pady=5)

        shape_val = tk.StringVar(value='All')
        tk.Label(dialog, text='Shape:').grid(row=1, column=0, padx=5, pady=5)
        shape = ttk.Combobox(dialog, textvariable=shape_val)
        shape.config(values=('All', *[str(s) for s in self.shapes]))
        shape['state'] = 'readonly'
        shape.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(dialog, text='Origin X:').grid(row=2, column=0, padx=5, pady=5)
        x_origin = tk.Entry(dialog, width=10)
        x_origin.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(dialog, text='Origin Y:').grid(row=2, column=2, padx=5, pady=5)
        y_origin = tk.Entry(dialog, width=10)
        y_origin.grid(row=2, column=3, padx=5, pady=5)

        x_origin.insert(0, str((self.origin[0] + self.origin[0] + self.cols - 1) / 2))
        y_origin.insert(0, str((self.origin[1] + self.origin[1] + self.rows - 1) / 2))

        def close():
            if theta.get().lstrip('-+').isnumeric() == False:
                label.config(text='Warning: Theta value must be integer!"')
                return
            elif (x_origin.get().replace('.', '', 1).isnumeric() == False) or (
                y_origin.get().replace('.', '', 1).isnumeric() == False
            ):
                label.config(text='Warning: Origin values must be positive numbers!"')
                return
            elif shape.current() < 0:
                label.config(text='Select an option!')
                return

            origin = (
                float(x_origin.get()),
                float(y_origin.get()),
            )

            if shape.current() == 0:
                for s in self.shapes:
                    s.rotate(int(theta.get()), origin)
            else:
                self.shapes[shape.current() - 1].rotate(int(theta.get()), origin)

            self.reset_canvas(destroy_shapes=False)

            dialog.destroy()

        tk.Button(dialog, text='Rotate', command=close).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        tk.Button(dialog, text='Cancel', command=dialog.destroy).grid(
            row=4, column=2, columnspan=2, pady=10
        )

    def scale_dialog(self):
        dialog = tk.Toplevel()
        label = tk.Label(dialog, text='')
        label.grid(row=3, column=0, padx=5, pady=5, columnspan=4)

        tk.Label(dialog, text='X Factor:').grid(row=0, column=0, padx=5, pady=5)
        x_scale = tk.Entry(dialog, width=10)
        x_scale.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dialog, text='Y Factor:').grid(row=0, column=2, padx=5, pady=5)
        y_scale = tk.Entry(dialog, width=10)
        y_scale.grid(row=0, column=3, padx=5, pady=5)

        shape_val = tk.StringVar(value='All')
        tk.Label(dialog, text='Shape:').grid(row=1, column=0, padx=5, pady=5)
        shape = ttk.Combobox(dialog, textvariable=shape_val)
        shape.config(values=('All', *[str(s) for s in self.shapes]))
        shape['state'] = 'readonly'
        shape.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(dialog, text='Origin X:').grid(row=2, column=0, padx=5, pady=5)
        x_origin = tk.Entry(dialog, width=10)
        x_origin.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(dialog, text='Origin Y:').grid(row=2, column=2, padx=5, pady=5)
        y_origin = tk.Entry(dialog, width=10)
        y_origin.grid(row=2, column=3, padx=5, pady=5)

        x_origin.insert(0, str((self.origin[0] + self.origin[0] + self.cols - 1) / 2))
        y_origin.insert(0, str((self.origin[1] + self.origin[1] + self.rows - 1) / 2))

        def close():
            if (
                x_scale.get().lstrip('-+').replace('.', '', 1).isnumeric() == False
                or y_scale.get().lstrip('-+').replace('.', '', 1).isnumeric() == False
            ):
                label.config(text='Warning: Scale factor must be numeric!"')
                return
            elif (x_origin.get().replace('.', '', 1).isnumeric() == False) or (
                y_origin.get().replace('.', '', 1).isnumeric() == False
            ):
                label.config(text='Warning: Origin values must be positive numbers!"')
                return
            elif shape.current() < 0:
                label.config(text='Select an option!')
                return

            origin = (
                float(x_origin.get()),
                float(y_origin.get()),
            )

            x_s, y_s = (
                float(x_scale.get()),
                float(y_scale.get()),
            )

            if shape.current() == 0:
                for s in self.shapes:
                    s.scale(x_s, y_s, origin)
            else:
                self.shapes[shape.current() - 1].scale(x_s, y_s, origin)

            self.reset_canvas(destroy_shapes=False)

            dialog.destroy()

        tk.Button(dialog, text='Scale', command=close).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        tk.Button(dialog, text='Cancel', command=dialog.destroy).grid(
            row=4, column=2, columnspan=2, pady=10
        )

    def reflection_dialog(self):
        dialog = tk.Toplevel()
        label = tk.Label(dialog, text='')
        label.grid(row=3, column=0, padx=5, pady=5, columnspan=4)

        flip_x = tk.BooleanVar(value=False)
        flip_y = tk.BooleanVar(value=False)

        tk.Label(dialog, text='Reflect Axis:').grid(row=0, column=0, padx=5, pady=5)
        tk.Checkbutton(
            dialog, text='X', variable=flip_x, onvalue=True, offvalue=False
        ).grid(row=0, column=1, padx=5, pady=5)
        tk.Checkbutton(
            dialog, text='Y', variable=flip_y, onvalue=True, offvalue=False
        ).grid(row=0, column=2, padx=5, pady=5)

        shape_val = tk.StringVar(value='All')
        tk.Label(dialog, text='Shape:').grid(row=1, column=0, padx=5, pady=5)
        shape = ttk.Combobox(dialog, textvariable=shape_val)
        shape.config(values=('All', *[str(s) for s in self.shapes]))
        shape['state'] = 'readonly'
        shape.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        tk.Label(dialog, text='Origin X:').grid(row=2, column=0, padx=5, pady=5)
        x_origin = tk.Entry(dialog, width=10)
        x_origin.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(dialog, text='Origin Y:').grid(row=2, column=2, padx=5, pady=5)
        y_origin = tk.Entry(dialog, width=10)
        y_origin.grid(row=2, column=3, padx=5, pady=5)

        x_origin.insert(0, str((self.origin[0] + self.origin[0] + self.cols - 1) / 2))
        y_origin.insert(0, str((self.origin[1] + self.origin[1] + self.rows - 1) / 2))

        def close():
            if (x_origin.get().replace('.', '', 1).isnumeric() == False) or (
                y_origin.get().replace('.', '', 1).isnumeric() == False
            ):
                label.config(text='Warning: Origin values must be positive numbers!"')
                return
            elif shape.current() < 0:
                label.config(text='Select an option!')
                return

            origin = (
                float(x_origin.get()),
                float(y_origin.get()),
            )

            if shape.current() == 0:
                for s in self.shapes:
                    s.reflect(flip_x.get(), flip_y.get(), origin)
            else:
                self.shapes[shape.current() - 1].reflect(
                    flip_x.get(), flip_y.get(), origin
                )

            self.reset_canvas(destroy_shapes=False)

            dialog.destroy()

        tk.Button(dialog, text='Reflect', command=close).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        tk.Button(dialog, text='Cancel', command=dialog.destroy).grid(
            row=4, column=2, columnspan=2, pady=10
        )

    def __init__(self, root, title='PaintApp', rows=25, cols=25, height=500, width=500):
        root.title(title)

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        self.root = root
        self.rows, self.cols, self.height, self.width = rows, cols, height, width
        self.origin = (0, 0)
        self.reset_canvas()

        # make Configs Menu
        configs_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Configs', menu=configs_menu)

        configs_menu.add_command(label='Resize', command=self.resize_dialog)
        configs_menu.add_command(label='Reset', command=self.reset_canvas)
        configs_menu.add_separator()
        configs_menu.add_command(label='Exit', command=root.destroy)

        # make Transformations Menu
        transf_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Transformations', menu=transf_menu)

        transf_menu.add_command(label='Translate', command=self.translate_dialog)
        transf_menu.add_command(label='Rotate', command=self.rotation_dialog)
        transf_menu.add_command(label='Scale', command=self.scale_dialog)
        transf_menu.add_command(label='Reflection', command=self.reflection_dialog)

        # make Draw Menu
        draw_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Draw', menu=draw_menu)

        # saves states for shapes methods
        self.draw_shape = tk.StringVar(value='point')
        self.line_algo = tk.StringVar(value='dda')
        self.crop_algo = tk.StringVar(value='cohen-sutherland')

        draw_menu.add_checkbutton(
            label='Point', onvalue='point', variable=self.draw_shape
        )
        draw_menu.add_checkbutton(
            label='Line', onvalue='line', variable=self.draw_shape
        )
        draw_menu.add_checkbutton(
            label='Circle', onvalue='circle', variable=self.draw_shape
        )
        draw_menu.add_checkbutton(
            label='Crop', onvalue='crop', variable=self.draw_shape
        )

        draw_menu.add_separator()

        draw_menu.add_command(label='Reset Crop', command=self.reset_crop)

        draw_menu.add_separator()

        line_menu = tk.Menu(draw_menu, tearoff=0)
        draw_menu.add_cascade(label='Line Algorithim', menu=line_menu)
        line_menu.add_checkbutton(label='DDA', onvalue='dda', variable=self.line_algo)
        line_menu.add_checkbutton(
            label='Bresenham', onvalue='bresenham', variable=self.line_algo
        )

        crop_menu = tk.Menu(draw_menu, tearoff=0)
        draw_menu.add_cascade(label='Crop Algorithim', menu=crop_menu)
        crop_menu.add_checkbutton(
            label='Cohen-Sutherland',
            onvalue='cohen-sutherland',
            variable=self.crop_algo,
        )
        crop_menu.add_checkbutton(
            label='Liang-Barsky', onvalue='liang-barsky', variable=self.crop_algo
        )
