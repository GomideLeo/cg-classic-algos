import math as maths


class Circle:
    def __init__(self, start_pos, end_pos):
        self.center = start_pos
        self.radius = round(
            maths.sqrt(
                (end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2
            )
        )

    def plot(self, canvas, grid):
        def plot_points(x, y):
            grid.get_pixel(self.center[0] + x, self.center[1] + y).set_pixel(canvas, 1)
            grid.get_pixel(self.center[0] - x, self.center[1] + y).set_pixel(canvas, 1)
            grid.get_pixel(self.center[0] + x, self.center[1] - y).set_pixel(canvas, 1)
            grid.get_pixel(self.center[0] - x, self.center[1] - y).set_pixel(canvas, 1)
            grid.get_pixel(self.center[0] + y, self.center[1] + x).set_pixel(canvas, 1)
            grid.get_pixel(self.center[0] - y, self.center[1] + x).set_pixel(canvas, 1)
            grid.get_pixel(self.center[0] + y, self.center[1] - x).set_pixel(canvas, 1)
            grid.get_pixel(self.center[0] - y, self.center[1] - x).set_pixel(canvas, 1)

        x, y = 0, self.radius
        p = 3 - 2 * self.radius
        plot_points(x, y)

        while x < y:
            if p < 0:
                p = p + 4 * x + 6
            else:
                y -= 1
                p = p + 4 * (x - y) + 10
            x += 1
            plot_points(x, y)
