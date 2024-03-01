from math import sin, cos, radians

class Point:
    def __init__(self, pos):
        self.pos = pos

    def __repr__(self) -> str:
        return f'Point pos: {self.pos}'

    def translate(self, x, y):
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        return self

    def reflect(self, reflect_x=True, reflect_y=True, reflect_origin=(0, 0)):
        # using Array here bc tuple is static
        temp_pos = [self.pos[0] - reflect_origin[0], self.pos[1] - reflect_origin[1]]

        if reflect_x:
            temp_pos[1] = -temp_pos[1]

        if reflect_y:
            temp_pos[0] = -temp_pos[0]

        self.pos = (
            int(temp_pos[0] + reflect_origin[0]),
            int(temp_pos[1] + reflect_origin[1]),
        )

    def rotate(self, angle, origin=(0, 0)):
        temp_pos = (self.pos[0] - origin[0], self.pos[1] - origin[1])

        theta = radians(angle)

        temp_pos = (
            temp_pos[0] * cos(theta) - temp_pos[1] * sin(theta),
            temp_pos[0] * sin(theta) + temp_pos[1] * cos(theta)
        )

        self.pos = (
            int(temp_pos[0] + origin[0]),
            int(temp_pos[1] + origin[1]),
        )

    def plot(self, canvas, grid):
        grid.get_pixel(*self.pos).set_pixel(canvas, 1)
