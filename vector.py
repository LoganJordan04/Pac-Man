import math


# A 2D vector class used for movement, direction, and positioning.
# Supports basic vector operations and precision-based comparisons.
class Vector2(object):
    # Initialize x and y coordinates of the vector
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        # Threshold for comparing floating-point equality
        self.thresh = 1e-6

    # Add two vectors component-wise
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    # Subtract two vectors component-wise
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    # Return a vector pointing in the opposite direction
    def __neg__(self):
        return Vector2(-self.x, -self.y)

    # Scale the vector by a scalar value
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    # Divide the vector by a scalar
    def __truediv__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / scalar, self.y / scalar)
        # Avoid division by zero
        return None

    # Compare two vectors with a tolerance to account for float inaccuracy
    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh:
            return True
        return False

    # Return the squared magnitude of the vector (faster than magnitude)
    def magnitude_squared(self):
        return self.x**2 + self.y**2

    # Return the Euclidean length of the vector
    def magnitude(self):
        return math.sqrt(self.magnitude_squared())

    # Return a copy of the vector
    def copy(self):
        return Vector2(self.x, self.y)

    # Return the vector as a (float, float) tuple
    def as_tuple(self):
        return self.x, self.y

    # Return the vector as a (int, int) tuple for grid-based use
    def as_int(self):
        return int(self.x), int(self.y)

    # Return a string representation of the vector
    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ">"
