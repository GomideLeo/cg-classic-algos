from math import sin, cos, radians


class Point:
    def __init__(self, pos):
        """
        Initialize a Point object with the specified position.

        Args:
            pos (tuple): The position of the point as a tuple (x, y).
        """

        self.pos = pos

    def __repr__(self) -> str:
        """
        Return a string representation of the Point object.

        Returns:
            str: The string representation of the Point object.
        """

        return f'Point {self.pos}'

    def translate(self, x, y):
        """
        Translate the point by the specified x and y distances.

        Args:
            x (int): The distance to translate the point along the x-axis.
            y (int): The distance to translate the point along the y-axis.

        Returns:
            Point: The translated Point object.
        """

        self.pos = (self.pos[0] + x, self.pos[1] + y)
        return self

    def reflect(self, reflect_x=True, reflect_y=True, reflect_origin=(0, 0)):
        """
        Reflect the point over the x-axis, y-axis, or both, with respect to the specified origin.

        Args:
            reflect_x (bool): Whether to reflect the point over the x-axis. Default is True.
            reflect_y (bool): Whether to reflect the point over the y-axis. Default is True.
            reflect_origin (tuple): The origin point for reflection. Default is (0, 0).

        Returns:
            None
        """

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
        """
        Rotate the point by the specified angle around the specified origin.

        Args:
            angle (float): The angle to rotate the point, in degrees.
            origin (tuple): The origin point for rotation. Default is (0, 0).

        Returns:
            None
        """

        temp_pos = (self.pos[0] - origin[0], self.pos[1] - origin[1])

        theta = radians(angle)

        temp_pos = (
            temp_pos[0] * cos(theta) - temp_pos[1] * sin(theta),
            temp_pos[0] * sin(theta) + temp_pos[1] * cos(theta),
        )

        self.pos = (
            int(temp_pos[0] + origin[0]),
            int(temp_pos[1] + origin[1]),
        )

    def scale(self, x, y, origin=(0, 0)):
        """
        Scale the point by the specified factors along the x and y axes, with respect to the specified origin.

        Args:
            x (float): The scaling factor along the x-axis.
            y (float): The scaling factor along the y-axis.
            origin (tuple): The origin point for scaling. Default is (0, 0).

        Returns:
            None
        """

        temp_pos = (self.pos[0] - origin[0], self.pos[1] - origin[1])

        temp_pos = (temp_pos[0] * x, temp_pos[1] * y)

        self.pos = (
            int(temp_pos[0] + origin[0]),
            int(temp_pos[1] + origin[1]),
        )

    def crop(self, xy_min, xy_max):
        """
        Crop the point based on the specified minimum and maximum coordinates.

        Args:
            xy_min (tuple): The minimum x and y coordinates for cropping.
            xy_max (tuple): The maximum x and y coordinates for cropping.

        Returns:
            Point or None: The cropped Point object, or None if the point is outside the crop area.
        """

        return (
            self
            if (
                self.pos[0] >= xy_min[0]
                and self.pos[0] < xy_max[0]
                and self.pos[1] >= xy_min[1]
                and self.pos[1] < xy_max[1]
            )
            else None
        )

    def plot(self, canvas, grid):
        """
        Plot the point on the specified canvas using the given grid.

        Args:
            canvas: The canvas to plot the point on.
            grid: The grid object representing the canvas.

        Returns:
            None
        """

        grid.get_pixel(*self.pos).set_pixel(canvas, 1)
