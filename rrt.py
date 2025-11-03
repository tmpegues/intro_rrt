from Domain import Domain
from tree import Tree
from obstacle import Obstacle

#from RRTBuilder import RRT_Builder
import numpy as np

np.random.seed(1)

# Create domain (no args defaults to 100 x 100)
# domain  = Domain([(0,100), (0,100), (0, 100)])
domain  = Domain([(0,100), (0,100)])

circ1 = Obstacle(domain, "circle", (50, 40), [9])
domain.add_obstacle(circ1)
circ2 = Obstacle(domain, "circle", (50, 60), [9])
domain.add_obstacle(circ2)
circ3 = Obstacle(domain, "circle", (50, 80), [9])
domain.add_obstacle(circ3)
circ4 = Obstacle(domain, "circle", (50, 100), [9])
domain.add_obstacle(circ4)
circ5 = Obstacle(domain, "circle", (50, 20), [9])
domain.add_obstacle(circ5)
circ6 = Obstacle(domain, "circle", (50, 0), [9])
domain.add_obstacle(circ6)

circ1 = Obstacle(domain, "circle", (70, 40), [9])
domain.add_obstacle(circ1)
circ2 = Obstacle(domain, "circle", (70, 60), [9])
domain.add_obstacle(circ2)
circ3 = Obstacle(domain, "circle", (70, 80), [9])
domain.add_obstacle(circ3)
circ4 = Obstacle(domain, "circle", (70, 100), [9])
domain.add_obstacle(circ4)
circ5 = Obstacle(domain, "circle", (70, 20), [9])
domain.add_obstacle(circ5)
circ6 = Obstacle(domain, "circle", (70, 0), [9])
domain.add_obstacle(circ6)


# Add random circles
num_circles = 25
min_dim = 5
max_dim = 5
for i in range(num_circles):
    new_obs = Obstacle(domain, "circle", dims=[np.random.rand() * (max_dim-min_dim) + min_dim])
    domain.add_obstacle(new_obs)

buffer = .5
# start = domain.rand_point(True, buffer)
# goal = domain.rand_point(True, buffer)
start = [1,1]
goal = [99, 99]

max_steps_K = 300
step_size = 5
tree = Tree(start, max_steps_K, step_size, buffer, goal)



# Run the RRT

tree.run_rrt(domain)
#tree.path = [[99,99], [90, 90], [40,90],[1,90], [1,1]]
tree.optimize_path(domain)
tree.show_tree(domain)
