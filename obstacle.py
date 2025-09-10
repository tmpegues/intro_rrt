import numpy as np

class Obstacle:
    """Obstacles to put in your RRT domain
       Written to work in 2 dimensions, but should work in more"""

    def __init__(self, domain, shape = None, dims = None, ):
        # Default to circles

        if not shape:
            shape = 'circle'

        if not dims:
            # Randomize center
            center = domain.rand_point()
            # Randomize other dimension (radius or side length), max 5
            dist = np.random.rand() * 5
        self.shape = shape
        self.dim = dist
