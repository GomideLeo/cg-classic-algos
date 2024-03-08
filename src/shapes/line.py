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
        temp_pos1 = [self.start_pos[0] - reflect_origin[0], self.start_pos[1] - reflect_origin[1]]
        temp_pos2 = [self.end_pos[0] - reflect_origin[0], self.end_pos[1] - reflect_origin[1]]

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
            temp_pos1[0] * sin(theta) + temp_pos1[1] * cos(theta)
        )
        temp_pos2 = (
            temp_pos2[0] * cos(theta) - temp_pos2[1] * sin(theta),
            temp_pos2[0] * sin(theta) + temp_pos2[1] * cos(theta)
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

        temp_pos1 = (
            temp_pos1[0] * x,
            temp_pos1[1] * y
        )
        temp_pos2 = (
            temp_pos2[0] * x,
            temp_pos2[1] * y
        )

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
        
        x_step = dx / steps
        y_step = dy / steps
        grid.get_pixel(round_func(x), round_func(y)).set_pixel(canvas, 1)
        if steps > 0:
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
            if x >= xy_max[0]:
                code |= 2
            if y < xy_min[1]:
                code |= 4
            if y >= xy_max[1]:
                code |= 8
            
            return code

        inside = lambda c: c ^ 8 != 0
        reject = lambda c1, c2: c1 & c2 != 0
        # doing a bitwise xor with 8 represents inverting all relevant bits
        accept = lambda c1, c2: (c1 | c2) == 0 

        c1, c2 = region_code(self.start_pos), region_code(self.end_pos)
        if c1 == 0 and c2 == 0:
            return True
        elif (c1 & c2) != 0:
            return False
        else:
            cout = c1 if c1 != 0 else c2
            return False



    def crop(self, xy_min, xy_max, algo='cohen-sutherland'):
        if algo != 'cohen-sutherland' and algo != 'liang-barsky':
            raise Exception(f'Algorithim {algo} not implemented')
        
        if algo == 'cohen-sutherland':
            return self.crop_cohen(xy_min, xy_max)
        elif algo == 'liang-barsky':
            raise Exception(f'Algorithim {algo} not implemented yet')
            # self.plot_bresenham(canvas, grid)

