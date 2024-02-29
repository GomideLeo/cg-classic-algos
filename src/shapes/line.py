import math as maths 

class Line:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        
    
    def plot_dda(self, canvas, grid, round_func=round):
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]

        steps = max(abs(dx), abs(dy))

        x, y = self.start_pos[0], self.start_pos[1]
        grid.get_pixel(round_func(x), round_func(y)).set_pixel(canvas, 1)
        
        if steps > 0:
            x_step = dx / steps
            y_step = dy / steps
            
            for _ in range(steps):
                x, y = x + x_step, y + y_step
                grid.get_pixel(round_func(x), round_func(y)).set_pixel(canvas, 1)

    def plot_bresenham(self, canvas, grid):
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]
        
        incrx = 1 if dx >= 0 else -1
        incry = 1 if dy >= 0 else -1

        dx, dy = abs(dx), abs(dy)

        x, y = self.start_pos[0], self.start_pos[1]
        grid.get_pixel(x, y).set_pixel(canvas, 1)

        if dy < dx:
            p = 2 * dy - dx
            c1, c2 = 2 * dy, 2 * (dy - dx)

            for _ in range(dx):
                x += incrx

                if p < 0:
                    p += c1
                else:
                    p += c2
                    y += incry

                grid.get_pixel(x, y).set_pixel(canvas, 1)
        else:
            p = 2 * dx - dy
            c1, c2 = 2 * dx, 2 * (dx - dy)

            for _ in range(dy):
                y += incry

                if p < 0:
                    p += c1
                else:
                    p += c2
                    x += incrx

                grid.get_pixel(x, y).set_pixel(canvas, 1)

    def plot(self, canvas, grid, algo='dda'):
        if algo != 'dda' and algo != 'bresenham':
            raise Exception(f'Algorithim {algo} not implemented')
        
        if algo == 'dda':
            self.plot_dda(canvas, grid)
        elif algo == 'bresenham':
            self.plot_bresenham(canvas, grid)


