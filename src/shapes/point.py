
class Point:
    def __init__(self, pos):
        self.pos = pos
    
    def plot(self, canvas, grid):
        grid.get_pixel(*self.pos).set_pixel(canvas, 1)
