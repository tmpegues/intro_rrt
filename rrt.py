from Domain import Domain
from tree import Tree
from obstacle import Obstacle

#from RRTBuilder import RRT_Builder
import numpy as np

#np.random.seed(0)

# Create domain (no args defaults to 100 x 100)
domain  = Domain([(50,100), (0,100)])
# Add 2 random circles
num_circles = 5
for i in range(num_circles):
    new_obs = Obstacle(domain)
    domain.add_obstacle(new_obs)


# Create tree (defaults to the center of the 100 x 100 Domain)
# [qinit], K, qdot 
tree = Tree([75, 50], 50, 5)

# Run the RRT
tree.run_rrt(domain)
tree.show_tree(domain)
