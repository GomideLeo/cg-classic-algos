import math as maths
from math import sin, cos, radians


class Line:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def __repr__(self) -> str:
        return f'Line {self.start_pos} -> {self.end_pos}'

    def translate(self, x, y):
        self.start_pos = (self.start_pos[0] + x, self.start_pos[1] + y)
        self.end_pos = (self.end_pos[0] + x, self.end_pos[1] + y)

    def reflect(self, reflect_x=True, reflect_y=True, reflect_origin=(0, 0)):
        # using Array here bc tuple is static
        temp_pos1 = [
            self.start_pos[0] - reflect_origin[0],
            self.start_pos[1] - reflect_origin[1],
        ]
        temp_pos2 = [
            self.end_pos[0] - reflect_origin[0],
            self.end_pos[1] - reflect_origin[1],
        ]

        if reflect_x:
            temp_pos1[1] = -temp_pos1[1]
            temp_pos2[1] = -temp_pos2[1]

        if reflect_y:
            temp_pos1[0] = -temp_pos1[0]
            temp_pos2[0] = -temp_pos2[0]

        self.start_pos = (
            int(temp_pos1[0] + reflect_origin[0]),
            int(temp_pos1[1] + reflect_origin[1]),
        )

        self.end_pos = (
            int(temp_pos2[0] + reflect_origin[0]),
            int(temp_pos2[1] + reflect_origin[1]),
        )

    def rotate(self, angle, origin=(0, 0)):
        temp_pos1 = (self.start_pos[0] - origin[0], self.start_pos[1] - origin[1])
        temp_pos2 = (self.end_pos[0] - origin[0], self.end_pos[1] - origin[1])

        theta = radians(angle)

        temp_pos1 = (
            temp_pos1[0] * cos(theta) - temp_pos1[1] * sin(theta),
            temp_pos1[0] * sin(theta) + temp_pos1[1] * cos(theta),
        )
        temp_pos2 = (
            temp_pos2[0] * cos(theta) - temp_pos2[1] * sin(theta),
            temp_pos2[0] * sin(theta) + temp_pos2[1] * cos(theta),
        )

        self.start_pos = (
            int(temp_pos1[0] + origin[0]),
            int(temp_pos1[1] + origin[1]),
        )

        self.end_pos = (
            int(temp_pos2[0] + origin[0]),
            int(temp_pos2[1] + origin[1]),
        )

    def scale(self, x, y, origin=(0, 0)):
        temp_pos1 = (self.start_pos[0] - origin[0], self.start_pos[1] - origin[1])
        temp_pos2 = (self.end_pos[0] - origin[0], self.end_pos[1] - origin[1])

        temp_pos1 = (temp_pos1[0] * x, temp_pos1[1] * y)
        temp_pos2 = (temp_pos2[0] * x, temp_pos2[1] * y)

        self.start_pos = (
            int(temp_pos1[0] + origin[0]),
            int(temp_pos1[1] + origin[1]),
        )

        self.end_pos = (
            int(temp_pos2[0] + origin[0]),
            int(temp_pos2[1] + origin[1]),
        )

    def plot_dda(self, canvas, grid, round_func=round):
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]

        steps = max(abs(dx), abs(dy))

        x, y = self.start_pos

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

    def crop_cohen(self, xy_min, xy_max):
        def region_code(point):
            x, y = point
            code = 0

            if x < xy_min[0]:
                code |= 1
            if x > xy_max[0]:
                code |= 2
            if y < xy_min[1]:
                code |= 4
            if y > xy_max[1]:
                code |= 8

            return code

        bit = lambda cod, bit: cod >> bit & 1

        c1, c2 = region_code(self.start_pos), region_code(self.end_pos)

        if c1 == 0 and c2 == 0:
            return self
        elif (c1 & c2) != 0:
            return None
        else:
            cout = c1 if c1 != 0 else c2
            m = (
                (self.end_pos[1] - self.start_pos[1])
                / (self.end_pos[0] - self.start_pos[0])
                if self.end_pos[0] != self.start_pos[0]
                else 0
            )
            if bit(cout, 0) == 1:
                x_int = xy_min[0]
                y_int = self.start_pos[1] + (xy_min[0] - self.start_pos[0]) * m
            elif bit(cout, 1) == 1:
                x_int = xy_max[0]
                y_int = self.start_pos[1] + (xy_max[0] - self.start_pos[0]) * m
            elif bit(cout, 2) == 1:
                y_int = xy_min[1]
                x_int = (
                    self.start_pos[0] + (xy_min[1] - self.start_pos[1]) / m
                    if m != 0
                    else self.start_pos[0]
                )
            elif bit(cout, 3) == 1:
                y_int = xy_max[1]
                x_int = (
                    self.start_pos[0] + (xy_max[1] - self.start_pos[1]) / m
                    if m != 0
                    else self.start_pos[0]
                )

            if c1 == cout:
                return Line((round(x_int), round(y_int)), self.end_pos).crop_cohen(
                    xy_min, xy_max
                )
            else:
                return Line(self.start_pos, (round(x_int), round(y_int))).crop_cohen(
                    xy_min, xy_max
                )

    def crop_liang(self, xy_min, xy_max):
        u1, u2 = 0, 1

        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]

        def clip_test(p, q):
            nonlocal u1, u2
            if p < 0:
                r = q / p
                if r > u2:
                    return False
                elif r > u1:
                    u1 = r
            elif p > 0:
                r = q / p
                if r < u1:
                    return False
                elif r < u2:
                    u2 = r
            else:
                if q < 0:
                    return False

            return True

        if (
            clip_test(-dx, self.start_pos[0] - xy_min[0])
            and clip_test(dx, xy_max[0] - self.start_pos[0])
            and clip_test(-dy, self.start_pos[1] - xy_min[1])
            and clip_test(dx, xy_max[1] - self.start_pos[1])
        ):
            p1, p2 = self.start_pos, self.end_pos
            if u2 < 1:
                p2 = (round(p1[0] + u2 * dx), round(p1[1] + u2 * dy))
            if u1 > 0:
                p1 = (round(p1[0] + u1 * dx), round(p1[1] + u1 * dy))

            return Line(p1, p2)

    def crop(self, xy_min, xy_max, algo='cohen-sutherland'):
        if algo != 'cohen-sutherland' and algo != 'liang-barsky':
            raise Exception(f'Algorithim {algo} not implemented')

        if algo == 'cohen-sutherland':
            return self.crop_cohen(xy_min, xy_max)
        elif algo == 'liang-barsky':
            return self.crop_liang(xy_min, xy_max)
