import numpy as np

class Domain:
    """This will be the domain for the RRT Project
       At the beginning, with no obstacles, it'll be really simple"""

    def __init__(self, dims = None):
        """Creates the domain with default size 100 x 100
           dims is a list of tuples of min and max values in each dimension
               [(0,100), (0,100)] as default for a 2D 100 x 100"""
        
        if not dims:
            dims = [(0,100), (0,100)]
        self.num_dims = len(dims)
        self.dims = dims
        self.obstacles = []
    
    def rand_point(self):
        """Generates a random point inside the domain"""
        p1 = np.random.rand(self.num_dims)
        point2 = [x*(top - bot) + bot for x, (bot, top) in zip(p1, self.dims)]

        return point2
    
    def in_domain(self, point):
        """Check if provided point is in the domain
           Does not currently check obstacles"""
        domain_status = True
        for i in range(self.num_dims):
            # Check if point is below lower bound or above upper bound
            # End immediately if outside of any dimension's bounds
            if point[i] < self.dims[i][0] or self.dims[i][1] < point[i]:
                return False
                
        return domain_status