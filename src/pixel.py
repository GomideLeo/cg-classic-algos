class Pixel:
    def __init__(self, value, x, y, id=None):
        self.id = id
        self.value = value
        self.y = y
        self.x = x
    
    def __repr__(self):
        return str(self.value)

    def bind_id(self, id):
        self.id = id

    def togglePixel(self, event, canvas):
        # Modify this function to perfo rm your desired action on click
        self.value = 1 if self.value < 0.8 else 0

        color = int(self.value*255)
        colorCode = "#%02x%02x%02x" % (color, color, color)
        outline = "gray" if self.value < 0.3 else "black"

        canvas.itemconfig(self.id, fill=colorCode, outline=outline)