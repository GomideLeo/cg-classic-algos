class Pixel:
    def __init__(self, x, y, value=0, id=None):
        self.id = id
        self.value = value
        self.y = y
        self.x = x
    
    def __repr__(self):
        return str(self.value)

    def bind_id(self, id):
        self.id = id

    def toggle_pixel(self, canvas):
        self.setPixel(canvas, 1 if self.value < 0.3 else 0)

    def set_pixel(self, canvas, value):
        if self.id is None: return

        self.value = max(min(value, 1), 0)

        color = int(self.value*255)
        colorCode = '#%02x%02x%02x' % (color, color, color)
        outline = 'gray' if self.value < 0.3 else 'black'

        canvas.itemconfig(self.id, fill=colorCode, outline=outline)