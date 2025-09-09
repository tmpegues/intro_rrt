

class RRT_Domain:
    """This will be the domain for the RRT Project
       At the beginning, with no obstacles, it'll be really simple"""

    def __init__(self, size_x = None, size_y = None):
        """Creates the domain with default size 100 x 100"""
        if size_x != None:
            size_x = (0, 100)
        if size_y != None:
            size_y = (0, 100)
        
        self.size_x = size_x
        self.size_y = size_y