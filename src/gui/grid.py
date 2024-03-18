import tkinter as tk
from .pixel import Pixel


class Grid:
    def __init__(self, height=32, width=32, origin=(0, 0)):
        """
        Initialize a grid of Pixel objects with the specified height, width, and origin.

        Args:
            height (int): The height of the grid. Default is 32.
            width (int): The width of the grid. Default is 32.
            origin (tuple): The origin coordinates of the grid. Default is (0, 0).
        """

        self.height = height
        self.width = width
        self.origin = origin

        self.board = [
            [Pixel(j + origin[0], i + origin[1]) for j in range(self.width)] for i in range(self.height)
        ]

    def __repr__(self):
        """
        Return a string representation of the Grid object.

        Returns:
            str: The string representation of the Grid object.
        """

        return str(self.board)

    def get_pixel(self, x, y):
        """
        Get the Pixel object at the specified coordinates. 
        If no pixel is found in the specified position, a fake one is created.

        Args:
            x (int): The x-coordinate of the pixel.
            y (int): The y-coordinate of the pixel.

        Returns:
            Pixel: The Pixel object at the specified coordinates.
        """

        x, y = x - self.origin[0], y - self.origin[1]

        if x >= 0 and y >= 0 and y < len(self.board) and x < len(self.board[y]):
            return self.board[y][x]
        else:
            return Pixel(x, y)

    def make_canvas(
        self,
        root,
        height=1000,
        width=1000,
        callback=lambda ev, canvas, px: px.togglePixel(canvas),
    ):
        """
        Create a tkinter canvas representing the grid of pixels. Each Pixel is a Button with
        its comportament defined by the callback function

        Args:
            root: The tkinter root window or frame to which the canvas will be added.
            height (int): The height of the canvas. Default is 1000.
            width (int): The width of the canvas. Default is 1000.
            callback (function): The callback function to be called when a pixel is clicked. 
                Default is lambda ev, canvas, px: px.toggle_pixel(canvas).

        Returns:
            tk.Canvas: The tkinter canvas representing the grid of pixels.
        """

        pixel_size = min(height // self.height, width // self.width)

        canvas = tk.Canvas(
            root, width=self.width * pixel_size, height=self.height * pixel_size
        )
        canvas.pack()

        for row in self.board:
            for px in row:
                x1, y1 = (px.x - self.origin[0]) * pixel_size, (px.y - self.origin[1]) * pixel_size
                x2, y2 = x1 + pixel_size, y1 + pixel_size

                color = int(px.value * 255)
                colorCode = '#%02x%02x%02x' % (color, color, color)
                outline = 'gray' if px.value < 0.3 else 'black'

                # Draw the white rectangle with borders
                id = canvas.create_rectangle(
                    x1, y1, x2, y2, fill=colorCode, outline=outline
                )
                px.bind_id(id)

                # Bind click event to the rectangle object
                canvas.tag_bind(
                    id,
                    '<Button-1>',
                    lambda event, canvas=canvas, px=px: callback(event, canvas, px),
                )

        return canvas
