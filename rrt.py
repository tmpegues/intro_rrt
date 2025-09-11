from Domain import Domain
from tree import Tree
from obstacle import Obstacle

#from RRTBuilder import RRT_Builder
import numpy as np

np.random.seed(0)

# Create domain (no args defaults to 100 x 100)
domain  = Domain([(0,100), (0,100)])

circ1 = Obstacle(domain, "circle", (50, 50), [10])
domain.add_obstacle(circ1)

# Add random circles
num_circles = 4
for i in range(num_circles):
    new_obs = Obstacle(domain)
    #domain.add_obstacle(new_obs)


start = domain.rand_point(True)
goal = domain.rand_point(True)
#
buffer = 0

tree = Tree(start, 750, 5, buffer, goal)


# Run the RRT
tree.run_rrt(domain)
tree.show_tree(domain)
