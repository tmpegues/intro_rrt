import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

class Tree:
    """This will be the tree builder"""

    def __init__(self, q_init = None, K = None, qdot = None):
        if not q_init:
            # Randomize this, eventually
            q_init = [50, 50]
        if not K:
            K == 100
        if not qdot:
            qdot = 1
        
        # Each element in G will first include itself and then the point it came from 
        self.G = [(q_init,None)]
        self.K = K
        self.num_dims = len(q_init)
        self.qdot = qdot

    def get_nearest(self, point):
        best_point = None

        # Check the distance of every point
        for i in range(len(self.G)):
            ##### Begin_Citation [1] #####
            dist = np.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(self.G[i][0], point)))
            ##### End_Citation [1] #####
            # Update best_point if a point is found closer than current one
            # Automatically accept the first point though
            if not best_point or dist < best_point[1]:
                best_point = [self.G[i][0], dist]
        return best_point
    
    def new_config(self, domain, qrand, qnear, dist, want_print = False):
        """Adds a new configuration to the tree going from qnear toward qrand"""
        
        # 1. Get direction
        # 2. Normalize
        # 3. Calculate how far to step in each dimension
        # 4. Step

        direction = [randx - nearx for randx, nearx in zip(qrand, qnear)]
        unit_vector = [dim/dist for dim in direction]
        steps = [dim * self.qdot for dim in unit_vector]
        qnew = [dim + step for dim, step in zip(qnear,steps)]
        dist1 = np.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(qnear, qnew)))

        # Check if qnew is a valid point in the domain
        if not domain.in_domain(qnew):
            qnew = False

        if want_print:
            print(f"rand{qrand}\nnear{qnear}\ndist {dist}")
            print("")
            print(f"dir{direction}\nuv{unit_vector}\nsteps{steps}\nqnew{qnew}")
            print(f"dist1 {dist1}")

        return qnew
    
    def run_rrt(self, domain, want_print = False):
        while len(self.G) < self.K:
            # Produce random point in domain
            qrand = np.random.rand(self.num_dims)
            for i in range(self.num_dims):
                qrand[i] *= (domain.dims[i][1] - domain.dims[i][0])
            (qnear, dist) = self.get_nearest(qrand)
            qnew = self.new_config(domain, qrand, qnear, dist, want_print = False)
            if qnew != False:
                self.G.append((qnew,qnear))
                if want_print:
                    print(len(self.G))
                    for dot in self.G:
                        print(f"{dot[0]},{dot[1]}")

    def show_tree(self, domain):
        """Display the tree, but only if it's 2D"""
        if self.num_dims > 2:
            print("I'm not dealing with high dimensions right now")
        else:
            ##### Begin_Citation [2] #####
            fig, ax = plt.subplots()
            segs = []
            for point in self.G:
                (x, y) =  point[0]
                ax.scatter(x, y)
                ##### Begin_Citation [3] #####
                if point[1] != None:
                    segs.append([point[0],point[1]])
            line_segments = LineCollection(segs)   
            ax.add_collection(line_segments)
            ##### End_Citation [3] #####
            plt.show()
            ##### End_Citation [2] #####
