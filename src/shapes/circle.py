import math as maths
from math import sin, cos, radians


class Circle:
    def __init__(self, start_pos, end_pos):
        """
        Initialize a Circle object with the specified start and end positions.

        Args:
            start_pos (tuple): The starting position of the circle.
            end_pos (tuple): The ending position of the circle.
        """

        self.center = start_pos
        self.radius = round(
            maths.sqrt(
                (end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2
            )
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the Circle object.

        Returns:
            str: The string representation of the Circle object.
        """

        return f'Cricle {self.center}, r: {self.radius}'

    def translate(self, x, y):
        """
        Translate the circle by the specified x and y distances.

        Args:
            x (int): The distance to translate the circle along the x-axis.
            y (int): The distance to translate the circle along the y-axis.

        Returns:
            None
        """

        self.center = (self.center[0] + x, self.center[1] + y)

    def reflect(self, reflect_x=True, reflect_y=True, reflect_origin=(0, 0)):
        """
        Reflect the circle over the x-axis, y-axis, or both, with respect to the specified origin.

        Args:
            reflect_x (bool): Whether to reflect the circle over the x-axis. Default is True.
            reflect_y (bool): Whether to reflect the circle over the y-axis. Default is True.
            reflect_origin (tuple): The origin point for reflection. Default is (0, 0).

        Returns:
            None
        """

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
        """
        Rotate the circle by the specified angle around the specified origin.

        Args:
            angle (float): The angle to rotate the circle, in degrees.
            origin (tuple): The origin point for rotation. Default is (0, 0).

        Returns:
            None
        """

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
        """
        Scale the circle by the specified factors along the x and y axes, with respect to the specified origin.
        Obs.: The radius is not scaled

        Args:
            x (float): The scaling factor along the x-axis.
            y (float): The scaling factor along the y-axis.
            origin (tuple): The origin point for scaling. Default is (0, 0).

        Returns:
            None
        """

        temp_pos = (self.center[0] - origin[0], self.center[1] - origin[1])

        temp_pos = (temp_pos[0] * x, temp_pos[1] * y)

        self.center = (
            int(temp_pos[0] + origin[0]),
            int(temp_pos[1] + origin[1]),
        )

    def crop(self, xy_min, xy_max):
        """
        Crop the circle based on the specified minimum and maximum coordinates.

        Args:
            xy_min (tuple): The minimum x and y coordinates for cropping.
            xy_max (tuple): The maximum x and y coordinates for cropping.

        Returns:
            Circle or None: The cropped Circle object, or None if the circle is completely outside the crop area.
        """

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
        """
        Plot the circle on the specified canvas using the given grid.

        Args:
            canvas: The canvas to plot the circle on.
            grid: The grid object representing the canvas.

        Returns:
            None
        """

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
