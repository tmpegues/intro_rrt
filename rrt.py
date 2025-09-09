from Domain import Domain
from tree import Tree
import numpy as np

#np.random.seed(0)
#from RRTBuilder import RRT_Builder

# Create domain (no args defaults to 100 x 100)
domain  = Domain()

# Create tree (defaults to the center of the 100 x 100 Domain)
# [qinit], K, qdot 
tree = Tree([50, 50], 250, 1)

# Run the RRT
tree.run_rrt(domain)
tree.show_tree(domain)
