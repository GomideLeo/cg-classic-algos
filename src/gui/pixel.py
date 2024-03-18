class Pixel:
    def __init__(self, x, y, value=0, id=None):
        """
        Initialize a Pixel object with the specified coordinates, value, and optional ID.

        Args:
            x (int): The x-coordinate of the pixel.
            y (int): The y-coordinate of the pixel.
            value (float): The value of the pixel, ranging from 0 to 1. Default is 0.
            id (int): Optional ID for the pixel, used for binding to a canvas item. Default is None.
        """

        self.id = id
        self.value = value
        self.y = y
        self.x = x
    
    def __repr__(self):
        """
        Return a string representation of the Pixel object.

        Returns:
            str: The string representation of the Pixel object.
        """

        return str(self.value)

    def bind_id(self, id):
        """
        Bind an ID to the Pixel object, used for associating it with a canvas item.

        Args:
            id: The ID to bind to the Pixel object.

        Returns:
            None
        """

        self.id = id

    def toggle_pixel(self, canvas):
        """
        Toggle the pixel's value and update its appearance on the canvas.

        Args:
            canvas: The canvas on which the pixel is displayed.

        Returns:
            None
        """

        self.setPixel(canvas, 1 if self.value < 0.3 else 0)

    def set_pixel(self, canvas, value):
        """
        Set the pixel's value to the specified value and update its appearance on the canvas.

        Args:
            canvas: The canvas on which the pixel is displayed.
            value (float): The new value for the pixel, ranging from 0 to 1.

        Returns:
            None
        """

        if self.id is None: return

        self.value = max(min(value, 1), 0)

        color = int(self.value*255)
        colorCode = '#%02x%02x%02x' % (color, color, color)
        outline = 'gray' if self.value < 0.3 else 'black'

        canvas.itemconfig(self.id, fill=colorCode, outline=outline)