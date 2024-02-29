import tkinter as tk
from .pixel import Pixel


class Grid:
    def __init__(self, height=100, width=100):
        self.height = height
        self.width = width
        # self.bg_color = bg_color
        # self.fg_color = fg_color

        self.board = [
            [Pixel(j, i) for j in range(self.width)] for i in range(self.height)
        ]

    def __repr__(self):
        return str(self.board)

    def get_pixel(self, x, y):
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
        pixel_size = min(height // self.height, width // self.width)

        canvas = tk.Canvas(
            root, width=self.width * pixel_size, height=self.height * pixel_size
        )
        canvas.pack()

        for row in self.board:
            for px in row:
                x1, y1 = px.x * pixel_size, px.y * pixel_size
                x2, y2 = x1 + pixel_size, y1 + pixel_size

                color = int(px.value * 255)
                colorCode = "#%02x%02x%02x" % (color, color, color)
                outline = "gray" if px.value < 0.3 else "black"

                # Draw the white rectangle with borders
                id = canvas.create_rectangle(
                    x1, y1, x2, y2, fill=colorCode, outline=outline
                )
                px.bind_id(id)

                # Bind click event to the rectangle object
                canvas.tag_bind(
                    id,
                    "<Button-1>",
                    lambda event, canvas=canvas, px=px: callback(event, canvas, px),
                )

        return canvas
