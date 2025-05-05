import math

class Vector2(object):
    """
    A class to represent a 2D vector with x and y components.
    Supports basic vector arithmetic, comparison, and utility methods.
    """

    def __init__(self, x=0, y=0):
        """
        Initialize a Vector2 instance.
        :param x: X component of the vector (default 0)
        :param y: Y component of the vector (default 0)
        """
        self.x = x
        self.y = y
        self.thresh = 1e-6  # Threshold for comparing floating-point values

    def __add__(self, other):
        """
        Vector addition: self + other
        :param other: Another Vector2 instance
        :return: New Vector2 that is the sum
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Vector subtraction: self - other
        :param other: Another Vector2 instance
        :return: New Vector2 that is the difference
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        """
        Negation: -self
        :return: New Vector2 with both components negated
        """
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        """
        Scalar multiplication: self * scalar
        :param scalar: A number to scale the vector
        :return: New Vector2 scaled by the scalar
        """
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        """
        Scalar division: self / scalar (Python 2 style)
        :param scalar: A number to divide the vector
        :return: New Vector2 scaled down by scalar or None if scalar is 0
        """
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None  # Avoid division by zero

    def __truediv__(self, scalar):
        """
        Scalar division: self / scalar (Python 3 style)
        Delegates to __div__ for actual computation.
        """
        return self.__div__(scalar)

    def __eq__(self, other):
        """
        Equality check (with a small threshold to account for float imprecision).
        :param other: Another Vector2 instance
        :return: True if components are approximately equal, else False
        """
        if abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh:
            return True
        return False

    def magnitudeSquared(self):
        """
        Compute the squared magnitude of the vector (faster than magnitude).
        :return: x² + y²
        """
        return self.x**2 + self.y**2

    def magnitude(self):
        """
        Compute the actual magnitude (length) of the vector.
        :return: √(x² + y²)
        """
        return math.sqrt(self.magnitudeSquared())

    def copy(self):
        """
        Create a copy of the vector.
        :return: New Vector2 with same x and y
        """
        return Vector2(self.x, self.y)

    def asTuple(self):
        """
        Represent the vector as a tuple of floats.
        :return: (x, y)
        """
        return self.x, self.y

    def asInt(self):
        """
        Represent the vector as a tuple of integers (truncated).
        :return: (int(x), int(y))
        """
        return int(self.x), int(self.y)

    def __str__(self):
        """
        String representation of the vector.
        :return: String in format <x, y>
        """
        return "<" + str(self.x) + ", " + str(self.y) + ">"
