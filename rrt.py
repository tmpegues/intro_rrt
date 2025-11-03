from Domain import Domain
from tree import Tree
from obstacle import Obstacle

#from RRTBuilder import RRT_Builder
import numpy as np

#np.random.seed(0)

# Create domain (no args defaults to 100 x 100)
domain  = Domain([(0,100), (0,100), (0, 100)])

circ1 = Obstacle(domain, "circle", (50, 50, 50), [10])
domain.add_obstacle(circ1)

# Add random circles
num_circles = 30
min_dim = 5
max_dim = 10
for i in range(num_circles):
    new_obs = Obstacle(domain, "circle", dims=[np.random.rand() * (max_dim-min_dim) + min_dim])
    domain.add_obstacle(new_obs)

buffer = 1
start = domain.rand_point(True, buffer)
goal = domain.rand_point(True, buffer)
start = [1,1,1]
goal = [99, 99, 99]

max_steps_K = 150
tree = Tree(start, max_steps_K, 5, buffer, goal, True)


# Run the RRT

tree.run_rrt(domain)
tree.show_tree(domain)
