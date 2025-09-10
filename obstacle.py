import numpy as np

class Obstacle:
    """Obstacles to put in your RRT domain
       Written to work in 2 dimensions, but should work in more"""

    def __init__(self, domain, shape = None, center = None, dims = None):
        # Default to circles
        if not shape:
            shape = 'circle'
        if not center:
            # Randomize center
            center = domain.rand_point()
        if not dims:
            # Randomize other dimension (radius or side length), max 5
            dims = []
            dims.append(np.random.rand() * 5)
            """
            for i in range(domain.num_dims):
                dims.append(np.random.rand() * 5)
            """
        self.shape = shape
        self.center = center
        self.dims = dims

    def check_collision(self, point):
        if self.shape == "circle":
            # If distance from point to center < radius, fail the check
            d = np.sqrt(sum((x - y) ** 2.0 for x, y in zip(point, self.center)))
            if d <= self.dims:
                return False
            else:
                return True
