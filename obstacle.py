import numpy as np
import distance as dt
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
            # Randomize other dimension (radius or side length)
            dims = []
            dims.append(np.random.rand() * 5)
            """
            for i in range(domain.num_dims):
                dims.append(np.random.rand() * 5)
            """
        self.shape = shape
        self.center = center
        self.dims = dims

    def check_collision(self, qnew, qnear, buffer):
        if self.shape == "line":
            for i in range(len(self.dims)):
                pass
        if self.shape == "circle":
            # Check if either point is in the circle
            dist_new = dt.eu_dist(qnew, self.center)
            dist_near = dt.eu_dist(qnear, self.center)
            if dist_new - self.dims[0] <= buffer or dist_near - self.dims[0] <= buffer:
                return False

            # Check if path intersects the circle
            # Find point on line closest to circle center
            dist = dt.eu_dist(qnear,qnew)
            #dist = np.linalg.norm([near-new for near, new in zip(qnear,qnew)])
            ##### Begin_Citation [4] #####
            if dist == 0:
                unit_vector = np.zeros(len(qnear))
            else:
                unit_vector = [(x2 - x1)/dist for x1, x2 in zip(qnear, qnew)]
            w = [(c - xnear) for c, xnear in zip(self.center, qnear)]
            prod = np.dot(unit_vector, w)
            close_point = [x * prod + x1 for x, x1 in zip(unit_vector, qnear)]
            ##### End_Citation [4] #####
            close_dist = dt.eu_dist(close_point, self.center)
            # Is that point actually on the segment?

            if dt.point_in_seg(close_point,qnear,qnew, buffer):
                # Is that point inside the radius?
                if close_dist - self.dims[0] <= buffer:
                    return False
            else:
                return True

    def check_point(self, point, buffer = None):
        if not buffer:
            buffer = 0
        if self.shape == "circle":
            dist = dt.eu_dist(point, self.center)
            if dist <= self.dims[0] + buffer:
                return False
