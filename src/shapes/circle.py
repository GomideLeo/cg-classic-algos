import math as maths
from math import sin, cos, radians


class Circle:
    def __init__(self, start_pos, end_pos):
        self.center = start_pos
        self.radius = round(
            maths.sqrt(
                (end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2
            )
        )

    def __repr__(self) -> str:
        return f'Cricle {self.center}, r: {self.radius}'

    def translate(self, x, y):
        self.center = (self.center[0] + x, self.center[1] + y)

    def reflect(self, reflect_x=True, reflect_y=True, reflect_origin=(0, 0)):
        # using Array here bc tuple is static
        temp_pos = [
            self.center[0] - reflect_origin[0],
            self.center[1] - reflect_origin[1],
        ]

        if reflect_x:
            temp_pos[1] = -temp_pos[1]

        if reflect_y:
            temp_pos[0] = -temp_pos[0]

        self.center = (
            int(temp_pos[0] + reflect_origin[0]),
            int(temp_pos[1] + reflect_origin[1]),
        )

    def rotate(self, angle, origin=(0, 0)):
        temp_pos = (self.center[0] - origin[0], self.center[1] - origin[1])

        theta = radians(angle)

        temp_pos = (
            temp_pos[0] * cos(theta) - temp_pos[1] * sin(theta),
            temp_pos[0] * sin(theta) + temp_pos[1] * cos(theta),
        )

        self.center = (
            int(temp_pos[0] + origin[0]),
            int(temp_pos[1] + origin[1]),
        )

    def scale(self, x, y, origin=(0, 0)):
        temp_pos = (self.center[0] - origin[0], self.center[1] - origin[1])

        temp_pos = (temp_pos[0] * x, temp_pos[1] * y)

        self.center = (
            int(temp_pos[0] + origin[0]),
            int(temp_pos[1] + origin[1]),
        )

    def crop(self, xy_min, xy_max):
        x_min, x_max = (
            self.center[0] - self.radius,
            self.center[0] + self.radius,
        )
        y_min, y_max = (
            self.center[1] - self.radius,
            self.center[1] + self.radius,
        )

        return (
            self
            if (
                (x_min < xy_max[0] and x_max >= xy_min[0])
                and (y_min < xy_max[1] and y_max >= xy_min[1])
            )
            else None
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
                p += 4 * x + 6
            else:
                p += 4 * (x - y) + 10
                y -= 1
            x += 1
            plot_points(x, y)
