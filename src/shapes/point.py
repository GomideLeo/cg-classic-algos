
class Point:
    def __init__(self, pos):
        self.pos = pos
    
    def __repr__(self) -> str:
        return f'Point pos: {self.pos}'
    
    def translate(self, x, y):
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        return self
    
    def plot(self, canvas, grid):
        grid.get_pixel(*self.pos).set_pixel(canvas, 1)
